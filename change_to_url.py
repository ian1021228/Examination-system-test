import re

with open("src/features.tsx", "r") as f:
    content = f.read()

# 1. Remove uploadingFiles state
content = content.replace("  const [uploadingFiles, setUploadingFiles] = useState<{name: string, progress: number, task: UploadTask, id?: string}[]>([]);", "")
content = content.replace("  const [uploadingFiles, setUploadingFiles] = useState<{name: string, progress: number, task: UploadTask}[]>([]);", "")
content = content.replace("  const [uploadingFiles, setUploadingFiles] = useState<any[]>([]);", "")

# 2. Replace handleFileUpload and cancelUpload with a new state for URL input
new_funcs = """  const [newAttName, setNewAttName] = useState('');
  const [newAttUrl, setNewAttUrl] = useState('');

  const handleAddAttachmentLink = () => {
    if (!newAttName || !newAttUrl) {
      toast('請填寫檔案名稱與連結');
      return;
    }
    setNewMat(prev => ({ ...prev, attachments: [...(prev.attachments || []), { name: newAttName, url: newAttUrl }] }));
    setNewAttName('');
    setNewAttUrl('');
    toast('已加入附件連結');
  };"""

start_func = content.find("  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {")
end_func = content.find("  const removeAttachment = (index: number) => {")

if start_func != -1 and end_func != -1:
    content = content[:start_func] + new_funcs + "\n\n" + content[end_func:]
    
# 3. Replace the UI block for attachments
old_ui_start = content.find("              <div className=\"space-y-3 bg-[#F5F5F0] p-4 rounded-2xl border border-[#EAE6DF]\">")
old_ui_end = content.find("              {/* Description */}")

new_ui = """              <div className="space-y-3 bg-[#F5F5F0] p-4 rounded-2xl border border-[#EAE6DF]">
                <div className="flex flex-col gap-2">
                  <label className="text-sm font-bold text-[#4A3F35] flex items-center gap-2">
                    <Paperclip size={16} /> 附加外部檔案連結 ({newMat.attachments?.length || 0})
                  </label>
                  <p className="text-xs text-[#8C7A6B]">由於未使用付費方案，請將檔案上傳至 Google Drive 等空間，再將連結貼至此處。</p>
                  
                  <div className="flex flex-col sm:flex-row gap-2 mt-2">
                    <input 
                      type="text" 
                      placeholder="檔案名稱 (例如：講義 PDF)" 
                      className="px-3 py-2 rounded-xl border border-[#D1CCC5] flex-1 text-sm bg-white"
                      value={newAttName}
                      onChange={e => setNewAttName(e.target.value)}
                    />
                    <input 
                      type="text" 
                      placeholder="檔案連結 (URL)" 
                      className="px-3 py-2 rounded-xl border border-[#D1CCC5] flex-1 text-sm bg-white"
                      value={newAttUrl}
                      onChange={e => setNewAttUrl(e.target.value)}
                    />
                    <button 
                      onClick={handleAddAttachmentLink}
                      className="px-4 py-2 bg-[#4A3F35] text-white rounded-xl text-sm font-bold flex items-center justify-center gap-1 hover:bg-[#3A3129]"
                    >
                      <Plus size={16} /> 加入
                    </button>
                  </div>
                </div>
                
                {newMat.attachments && newMat.attachments.length > 0 ? (
                  <div className="flex flex-col gap-2 mt-2">
                    {newMat.attachments.map((att, i) => (
                      <div key={`att-${i}`} className="flex items-center justify-between bg-white p-2 px-3 rounded-lg border border-[#EAE6DF] text-sm">
                        <div className="flex-1 min-w-0 mr-2 flex flex-col">
                          <span className="truncate text-[#4A3F35] font-bold" title={att.name}>{att.name}</span>
                          <span className="truncate text-xs text-[#8C7A6B]" title={att.url}>{att.url}</span>
                        </div>
                        <button onClick={() => removeAttachment(i)} className="text-red-400 hover:text-red-600 p-2 rounded-md hover:bg-red-50">
                          <X size={16} />
                        </button>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-4 text-sm text-[#A69B8F] border-2 border-dashed border-[#D1CCC5] rounded-xl mt-2">
                    尚未加入任何附件
                  </div>
                )}
              </div>
"""

if old_ui_start != -1 and old_ui_end != -1:
    content = content[:old_ui_start] + new_ui + "\n" + content[old_ui_end:]

# We need to make sure uploadingFiles state declaration is removed correctly
content = re.sub(r"  const \[uploadingFiles.*?\] = useState<.*?>\(\[\]\);\n", "", content)

with open("src/features.tsx", "w") as f:
    f.write(content)
print("Success")
