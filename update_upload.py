import re

with open("src/features.tsx", "r") as f:
    content = f.read()

# Update imports
content = content.replace("import { ref, uploadBytes, getDownloadURL } from 'firebase/storage';", "import { ref, uploadBytes, getDownloadURL, uploadBytesResumable, UploadTask } from 'firebase/storage';")

start_idx = content.find("export function CourseMaterialsAdminTab")
end_idx = content.find("export function CourseMaterialsStudentView")
component_str = content[start_idx:end_idx]

# Replace state and handleFileUpload
new_state = """  const [filterUnit, setFilterUnit] = useState<number | 'all'>('all');
  const [uploadingFiles, setUploadingFiles] = useState<{name: string, progress: number, task: UploadTask}[]>([]);"""

component_str = component_str.replace("  const [filterUnit, setFilterUnit] = useState<number | 'all'>('all');\n  const [uploading, setUploading] = useState(false);", new_state)

old_upload = """  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;
    setUploading(true);
    try {
      const newAttachments = [...(newMat.attachments || [])];
      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const fileRef = ref(storage, `materials/${subjectId}/${Date.now()}_${file.name}`);
        await uploadBytes(fileRef, file);
        const url = await getDownloadURL(fileRef);
        newAttachments.push({ name: file.name, url });
      }
      setNewMat({ ...newMat, attachments: newAttachments });
      toast('檔案上傳成功');
    } catch (error) {
      console.error(error);
      toast('檔案上傳失敗');
    } finally {
      setUploading(false);
    }
  };"""

new_upload = """  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;
    
    Array.from(files).forEach(file => {
      const fileRef = ref(storage, `materials/${subjectId}/${Date.now()}_${file.name}`);
      const uploadTask = uploadBytesResumable(fileRef, file);
      
      setUploadingFiles(prev => [...prev, { name: file.name, progress: 0, task: uploadTask }]);

      uploadTask.on('state_changed', 
        (snapshot) => {
          const progress = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
          setUploadingFiles(prev => prev.map(f => f.task === uploadTask ? { ...f, progress } : f));
        }, 
        (error) => {
          console.error(error);
          toast(`上傳失敗: ${file.name}`);
          setUploadingFiles(prev => prev.filter(f => f.task !== uploadTask));
        }, 
        async () => {
          const url = await getDownloadURL(uploadTask.snapshot.ref);
          setNewMat(prev => ({ ...prev, attachments: [...(prev.attachments || []), { name: file.name, url }] }));
          setUploadingFiles(prev => prev.filter(f => f.task !== uploadTask));
          toast(`上傳成功: ${file.name}`);
        }
      );
    });
    
    // Clear input
    e.target.value = '';
  };

  const cancelUpload = (task: UploadTask) => {
    task.cancel();
    setUploadingFiles(prev => prev.filter(f => f.task !== task));
    toast('已取消上傳');
  };"""

component_str = component_str.replace(old_upload, new_upload)

old_ui = """              <div className="space-y-3 bg-[#F5F5F0] p-4 rounded-2xl border border-[#EAE6DF]">
                <div className="flex justify-between items-center">
                  <label className="text-sm font-bold text-[#4A3F35] flex items-center gap-2">
                    <Paperclip size={16} /> 附加檔案 ({newMat.attachments?.length || 0})
                  </label>
                  <label className={`cursor-pointer px-4 py-1.5 rounded-lg text-sm font-bold flex items-center gap-2 transition-all ${uploading ? 'bg-gray-200 text-gray-500' : 'bg-white text-[#4A3F35] border border-[#EAE6DF] hover:bg-[#EAE6DF]'}`}>
                    {uploading ? '上傳中...' : <><Upload size={14} /> 上傳本地檔案</>}
                    <input type="file" multiple className="hidden" onChange={handleFileUpload} disabled={uploading} />
                  </label>
                </div>
                
                {newMat.attachments && newMat.attachments.length > 0 ? (
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mt-2">
                    {newMat.attachments.map((att, i) => (
                      <div key={i} className="flex items-center justify-between bg-white p-2 px-3 rounded-lg border border-[#EAE6DF] text-sm">
                        <span className="truncate flex-1 text-[#4A3F35] mr-2" title={att.name}>{att.name}</span>
                        <button onClick={() => removeAttachment(i)} className="text-red-400 hover:text-red-600 p-1 rounded-md hover:bg-red-50">
                          <X size={14} />
                        </button>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-4 text-sm text-[#A69B8F] border-2 border-dashed border-[#D1CCC5] rounded-xl">
                    尚未上傳任何附件
                  </div>
                )}
              </div>"""

new_ui = """              <div className="space-y-3 bg-[#F5F5F0] p-4 rounded-2xl border border-[#EAE6DF]">
                <div className="flex justify-between items-center">
                  <label className="text-sm font-bold text-[#4A3F35] flex items-center gap-2">
                    <Paperclip size={16} /> 附加檔案 ({(newMat.attachments?.length || 0) + uploadingFiles.length})
                  </label>
                  <label className={`cursor-pointer px-4 py-1.5 rounded-lg text-sm font-bold flex items-center gap-2 transition-all bg-white text-[#4A3F35] border border-[#EAE6DF] hover:bg-[#EAE6DF]`}>
                    <Upload size={14} /> 上傳本地檔案
                    <input type="file" multiple className="hidden" onChange={handleFileUpload} />
                  </label>
                </div>
                
                {(newMat.attachments && newMat.attachments.length > 0) || uploadingFiles.length > 0 ? (
                  <div className="flex flex-col gap-2 mt-2">
                    {newMat.attachments?.map((att, i) => (
                      <div key={`att-${i}`} className="flex items-center justify-between bg-white p-2 px-3 rounded-lg border border-[#EAE6DF] text-sm">
                        <span className="truncate flex-1 text-[#4A3F35] mr-2" title={att.name}>{att.name}</span>
                        <button onClick={() => removeAttachment(i)} className="text-red-400 hover:text-red-600 p-1 rounded-md hover:bg-red-50">
                          <X size={14} />
                        </button>
                      </div>
                    ))}
                    {uploadingFiles.map((upf, i) => (
                      <div key={`upf-${i}`} className="flex items-center justify-between bg-white p-2 px-3 rounded-lg border border-[#EAE6DF] text-sm">
                        <div className="flex-1 min-w-0 mr-4">
                          <div className="flex justify-between text-xs mb-1">
                            <span className="truncate text-[#8C7A6B]">{upf.name}</span>
                            <span className="text-[#C2A878] font-bold">{Math.round(upf.progress)}%</span>
                          </div>
                          <div className="w-full bg-[#EAE6DF] rounded-full h-1.5">
                            <div className="bg-[#C2A878] h-1.5 rounded-full transition-all duration-300" style={{ width: `${upf.progress}%` }}></div>
                          </div>
                        </div>
                        <button onClick={() => cancelUpload(upf.task)} className="text-red-400 hover:text-red-600 p-1 rounded-md hover:bg-red-50" title="取消上傳">
                          <X size={14} />
                        </button>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-4 text-sm text-[#A69B8F] border-2 border-dashed border-[#D1CCC5] rounded-xl">
                    尚未上傳任何附件
                  </div>
                )}
              </div>"""

component_str = component_str.replace(old_ui, new_ui)

content = content[:start_idx] + component_str + content[end_idx:]

with open("src/features.tsx", "w") as f:
    f.write(content)
