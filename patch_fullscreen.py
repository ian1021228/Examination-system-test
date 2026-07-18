import re

with open("src/features.tsx", "r") as f:
    content = f.read()

# Add state for fullscreen
state_decl = """  const [materials, setMaterials] = useState<CourseMaterial[]>([]);
  const [activeMat, setActiveMat] = useState<CourseMaterial | null>(null);
  const [isFullscreen, setIsFullscreen] = useState(false);"""

content = content.replace("""  const [materials, setMaterials] = useState<CourseMaterial[]>([]);
  const [activeMat, setActiveMat] = useState<CourseMaterial | null>(null);""", state_decl)

# Update onClick to set isFullscreen
content = content.replace("onClick={() => setActiveMat(m)}", "onClick={() => { setActiveMat(m); setIsFullscreen(true); }}")

# Add the fullscreen view return logic right after `const units = ...`
fullscreen_return = """
  if (isFullscreen && activeMat) {
    return (
      <div className="fixed inset-0 z-50 bg-[#FDFBF7] flex flex-col h-screen overflow-hidden">
        {/* Top Header */}
        <div className="flex items-center p-4 bg-white border-b border-[#EAE6DF] shadow-sm shrink-0">
          <button 
            onClick={() => setIsFullscreen(false)} 
            className="bg-[#4A3F35] text-white px-5 py-2.5 rounded-xl font-bold flex items-center gap-2 hover:bg-[#3A3129] shadow-md transition-all"
          >
            <ChevronLeft size={20} />
            返回總覽
          </button>
          <div className="ml-6 flex-1 min-w-0 flex items-center gap-3">
            <span className="bg-[#F5F5F0] text-[#8C7A6B] text-xs font-bold px-2 py-1 rounded-md shrink-0">
              Unit {activeMat.unit}
            </span>
            <h1 className="font-bold text-lg text-[#4A3F35] truncate">
              {activeMat.title}
            </h1>
          </div>
        </div>
        
        {/* Main Content Area */}
        <div className="flex-1 overflow-y-auto">
          <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 md:px-8 space-y-10">
            {activeMat.description && (
              <p className="text-[#8C7A6B] text-lg leading-relaxed">{activeMat.description}</p>
            )}

            {/* Media Content */}
            {activeMat.contentUrl && (
              <div className="rounded-2xl overflow-hidden shadow-lg border border-[#EAE6DF] bg-black">
                {activeMat.contentUrl.includes('youtube.com') || activeMat.contentUrl.includes('youtu.be') ? (
                  <div className="aspect-video">
                    <iframe 
                      className="w-full h-full" 
                      src={`https://www.youtube.com/embed/${activeMat.contentUrl.split('v=')[1]?.split('&')[0] || activeMat.contentUrl.split('/').pop()}`} 
                      title="YouTube video player" 
                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                      allowFullScreen>
                    </iframe>
                  </div>
                ) : activeMat.contentUrl.endsWith('.pdf') ? (
                  <div className="h-[80vh] w-full">
                    <iframe src={activeMat.contentUrl} className="w-full h-full bg-white" title="PDF Viewer" />
                  </div>
                ) : (
                  <div className="aspect-video flex items-center justify-center bg-[#F5F5F0]">
                    <a href={activeMat.contentUrl} target="_blank" rel="noopener noreferrer" className="flex flex-col items-center gap-3 text-[#C2A878] hover:text-[#B39969] transition-colors">
                      <Play size={48} className="drop-shadow-md" />
                      <span className="font-bold text-lg">開啟外部教材連結</span>
                    </a>
                  </div>
                )}
              </div>
            )}

            {/* Markdown Notes */}
            {activeMat.markdownNotes && (
              <div className="prose prose-stone prose-h1:font-serif prose-h1:text-[#4A3F35] prose-h2:text-[#4A3F35] prose-a:text-[#C2A878] max-w-none bg-white p-8 md:p-12 rounded-3xl border border-[#EAE6DF] shadow-sm">
                <Markdown>{activeMat.markdownNotes}</Markdown>
              </div>
            )}

            {/* Attachments */}
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
            )}
          </div>
        </div>
      </div>
    );
  }
"""

content = content.replace("  const units = Array.from(new Set(materials.map(m => m.unit))).sort((a, b) => a - b);\n", "  const units = Array.from(new Set(materials.map(m => m.unit))).sort((a, b) => a - b);\n" + fullscreen_return)

# Also we need to make sure ChevronLeft is imported in features.tsx
if "ChevronLeft" not in content[:content.find("from 'lucide-react'")]:
    content = content.replace("import { ", "import { ChevronLeft, ")

with open("src/features.tsx", "w") as f:
    f.write(content)
print("Success")
