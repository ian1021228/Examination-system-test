import re

with open("src/features.tsx", "r") as f:
    content = f.read()

# 1. First, let's fix the CourseMaterialsStudentView createPortal
# We find:
student_view_start = "export function CourseMaterialsStudentView"
student_view_index = content.find(student_view_start)

if student_view_index != -1:
    # Find the end of the isFullscreen return block in CourseMaterialsStudentView
    end_of_return_idx = content.find("      </div>\n    );\n  }\n\n  return (", student_view_index)
    if end_of_return_idx != -1:
        # We need to inject the preview modal and document.body
        preview_modal = """
        {/* Attachment Preview Modal */}
        {previewAtt && (
          <div className="fixed inset-0 z-[110] bg-black/90 flex flex-col h-screen">
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
        )}"""
        
        replacement = preview_modal + "\n      </div>,\n      document.body\n    );\n  }\n\n  return ("
        content = content[:end_of_return_idx] + replacement + content[end_of_return_idx + len("      </div>\n    );\n  }\n\n  return ("):]

with open("src/features.tsx", "w") as f:
    f.write(content)
print("Success fix_all")
