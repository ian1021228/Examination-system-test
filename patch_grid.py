import re

with open("src/features.tsx", "r") as f:
    content = f.read()

# Replace the layout from dual-pane to single pane (just the list of chapters)
start_str = """  return (
    <div className="flex flex-col lg:flex-row gap-6 items-start h-[calc(100vh-140px)]">
      {/* Sidebar Navigation */}
      <div className="w-full lg:w-80 shrink-0 bg-white rounded-3xl border border-[#EAE6DF] shadow-sm overflow-hidden flex flex-col h-full max-h-full">"""

end_str = """            <h2 className="text-2xl font-serif font-black text-[#4A3F35]">歡迎來到課程中心</h2>
            <p className="text-[#8C7A6B] mt-2 max-w-sm">請從左側目錄選擇一個章節開始學習。所有的影音、筆記與講義都在這裡為你準備好了。</p>
          </div>
        )}
      </div>
    </div>
  );
}"""

new_layout = """  return (
    <div className="bg-white rounded-3xl border border-[#EAE6DF] shadow-sm overflow-hidden flex flex-col p-6">
      <div className="mb-6">
        <h3 className="font-serif font-black text-2xl text-[#4A3F35]">課程目錄</h3>
        <p className="text-[#8C7A6B] mt-1">共 {materials.length} 個章節，請選擇章節進入全螢幕閱讀</p>
      </div>
      
      {materials.length === 0 ? (
        <div className="text-center py-16 text-[#A69B8F] bg-[#FDFBF7] rounded-2xl border-2 border-dashed border-[#EAE6DF]">
          <Layout size={48} className="mx-auto text-[#D1CCC5] mb-4" />
          <p className="font-medium">尚未發布任何教材</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {units.map(u => {
            const unitMats = materials.filter(m => m.unit === u);
            return (
              <div key={u} className="space-y-3 bg-[#FDFBF7] p-5 rounded-2xl border border-[#EAE6DF]">
                <h4 className="font-bold text-[#4A3F35] flex items-center gap-2 border-b border-[#EAE6DF] pb-2 mb-3">
                  <div className="bg-[#C2A878] text-white text-xs px-2 py-0.5 rounded">Unit {u}</div>
                </h4>
                <div className="space-y-2">
                  {unitMats.map(m => (
                    <button 
                      key={m.id} 
                      onClick={() => { setActiveMat(m); setIsFullscreen(true); }} 
                      className="w-full text-left px-4 py-3 rounded-xl transition-all flex items-start gap-3 bg-white border border-[#EAE6DF] hover:border-[#C2A878] hover:shadow-md group"
                    >
                      <div className="mt-0.5 text-[#C2A878] group-hover:scale-110 transition-transform">
                        {m.type === 'video' ? <Video size={18} /> : m.type === 'pdf' ? <FileText size={18} /> : m.type === 'lesson' ? <Layout size={18} /> : <BookOpen size={18} />}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="font-bold text-sm text-[#4A3F35] truncate group-hover:text-[#C2A878] transition-colors">{m.title}</p>
                        <p className="text-xs text-[#8C7A6B] truncate mt-0.5">{m.description}</p>
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}"""

content = content[:content.find(start_str)] + new_layout + content[content.find(end_str) + len(end_str):]

with open("src/features.tsx", "w") as f:
    f.write(content)
print("Success")
