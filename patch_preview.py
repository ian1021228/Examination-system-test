import re

with open("src/features.tsx", "r") as f:
    content = f.read()

# Add previewAtt state
state_decl = """  const [materials, setMaterials] = useState<CourseMaterial[]>([]);
  const [activeMat, setActiveMat] = useState<CourseMaterial | null>(null);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [previewAtt, setPreviewAtt] = useState<{name: string, url: string} | null>(null);"""

content = content.replace("""  const [materials, setMaterials] = useState<CourseMaterial[]>([]);
  const [activeMat, setActiveMat] = useState<CourseMaterial | null>(null);
  const [isFullscreen, setIsFullscreen] = useState(false);""", state_decl)

old_attachments = """            {/* Attachments */}
            {activeMat.attachments && activeMat.attachments.length > 0 && (
              <div className="space-y-4">
                <h3 className="text-xl font-bold text-[#4A3F35] flex items-center gap-2">
                  <Paperclip size={20} className="text-[#C2A878]" /> 
                  課程附件下載
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                  {activeMat.attachments.map((att, i) => (
                    <a 
                      key={i} 
                      href={att.url} 
                      target="_blank" 
                      rel="noopener noreferrer" 
                      className="flex items-center gap-3 bg-white p-4 rounded-2xl border border-[#EAE6DF] hover:border-[#C2A878] hover:shadow-md transition-all group"
                    >
                      <div className="bg-[#FDFBF7] p-3 rounded-xl text-[#C2A878] group-hover:bg-[#C2A878] group-hover:text-white transition-colors">
                        <Download size={20} />
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="font-bold text-sm text-[#4A3F35] truncate">{att.name}</p>
                        <p className="text-xs text-[#8C7A6B] mt-0.5">點擊下載</p>
                      </div>
                    </a>
                  ))}
                </div>
              </div>
            )}"""

new_attachments = """            {/* Attachments */}
            {activeMat.attachments && activeMat.attachments.length > 0 && (
              <div className="space-y-4">
                <h3 className="text-xl font-bold text-[#4A3F35] flex items-center gap-2">
                  <Paperclip size={20} className="text-[#C2A878]" /> 
                  課程附件
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                  {activeMat.attachments.map((att, i) => {
                    const isPdf = att.url.toLowerCase().split('?')[0].endsWith('.pdf');
                    const isVideo = att.url.toLowerCase().split('?')[0].endswith('.mp4') if hasattr(att.url, 'endswith') else False # Wait, this is JS in python script... let's just do regex
                    return ""; // We'll replace this properly below
                  })}
                </div>
              </div>
            )}"""

# Let's just write the full replacement string
new_attachments = """            {/* Attachments */}
            {activeMat.attachments && activeMat.attachments.length > 0 && (
              <div className="space-y-4">
                <h3 className="text-xl font-bold text-[#4A3F35] flex items-center gap-2">
                  <Paperclip size={20} className="text-[#C2A878]" /> 
                  課程附件
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                  {activeMat.attachments.map((att, i) => {
                    const isPdf = att.url.toLowerCase().split('?')[0].endsWith('.pdf');
                    const isVideo = att.url.toLowerCase().match(/\.(mp4|webm|ogg)$/) || att.url.includes('youtube.com') || att.url.includes('youtu.be');
                    const isPreviewable = isPdf || isVideo;
                    
                    return (
                      <div key={i} className="flex items-center bg-white rounded-2xl border border-[#EAE6DF] hover:border-[#C2A878] hover:shadow-md transition-all group overflow-hidden">
                        {isPreviewable ? (
                          <button 
                            onClick={() => setPreviewAtt(att)}
                            className="flex-1 flex items-center gap-3 p-4 min-w-0 text-left hover:bg-[#FDFBF7] transition-colors"
                          >
                            <div className="bg-[#F5F5F0] p-3 rounded-xl text-[#C2A878] group-hover:bg-[#C2A878] group-hover:text-white transition-colors shrink-0">
                              <Play size={20} />
                            </div>
                            <div className="flex-1 min-w-0">
                              <p className="font-bold text-sm text-[#4A3F35] truncate">{att.name}</p>
                              <p className="text-xs text-[#8C7A6B] mt-0.5">點擊線上預覽</p>
                            </div>
                          </button>
                        ) : (
                          <a 
                            href={att.url} 
                            target="_blank" 
                            rel="noopener noreferrer" 
                            className="flex-1 flex items-center gap-3 p-4 min-w-0 text-left hover:bg-[#FDFBF7] transition-colors"
                          >
                            <div className="bg-[#F5F5F0] p-3 rounded-xl text-[#C2A878] group-hover:bg-[#C2A878] group-hover:text-white transition-colors shrink-0">
                              <Download size={20} />
                            </div>
                            <div className="flex-1 min-w-0">
                              <p className="font-bold text-sm text-[#4A3F35] truncate">{att.name}</p>
                              <p className="text-xs text-[#8C7A6B] mt-0.5">點擊下載</p>
                            </div>
                          </a>
                        )}
                        {isPreviewable && (
                           <a 
                             href={att.url} 
                             target="_blank" 
                             rel="noopener noreferrer" 
                             className="p-4 text-[#8C7A6B] hover:text-[#C2A878] border-l border-[#EAE6DF] hover:bg-[#FDFBF7] transition-colors h-full flex items-center justify-center shrink-0"
                             title="下載附件"
                           >
                             <Download size={20} />
                           </a>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
            )}"""

content = content.replace(old_attachments, new_attachments)

modal_ui = """
        {/* Attachment Preview Modal */}
        {previewAtt && (
          <div className="fixed inset-0 z-[60] bg-black/90 flex flex-col h-screen">
            <div className="flex items-center p-4 bg-black text-white shrink-0">
              <button 
                onClick={() => setPreviewAtt(null)} 
                className="bg-white/10 hover:bg-white/20 text-white px-5 py-2.5 rounded-xl font-bold flex items-center gap-2 transition-all"
              >
                <ChevronLeft size={20} />
                返回課程
              </button>
              <h3 className="ml-6 font-bold text-lg truncate flex-1 min-w-0">{previewAtt.name}</h3>
              <a 
                href={previewAtt.url} 
                target="_blank" 
                rel="noopener noreferrer" 
                className="ml-4 p-2.5 bg-white/10 hover:bg-white/20 rounded-xl transition-colors"
                title="下載"
              >
                <Download size={20} />
              </a>
            </div>
            <div className="flex-1 overflow-hidden flex items-center justify-center p-4 sm:p-8">
              {previewAtt.url.includes('youtube.com') || previewAtt.url.includes('youtu.be') ? (
                <iframe 
                  className="w-full h-full max-w-6xl aspect-video rounded-2xl shadow-2xl" 
                  src={`https://www.youtube.com/embed/${previewAtt.url.split('v=')[1]?.split('&')[0] || previewAtt.url.split('/').pop()}`} 
                  allowFullScreen>
                </iframe>
              ) : previewAtt.url.toLowerCase().split('?')[0].endsWith('.pdf') ? (
                <iframe src={previewAtt.url} className="w-full h-full max-w-6xl bg-white rounded-2xl shadow-2xl" />
              ) : previewAtt.url.toLowerCase().match(/\.(mp4|webm|ogg)$/) ? (
                <video src={previewAtt.url} controls className="max-w-full max-h-full rounded-2xl shadow-2xl" />
              ) : (
                <div className="text-white text-center">
                  <p className="mb-4">預覽錯誤或不支援此格式</p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    );
  }
"""

content = content.replace("      </div>\n    );\n  }\n  const filteredMats", modal_ui + "\n  const filteredMats")


with open("src/features.tsx", "w") as f:
    f.write(content)

print("Success")
