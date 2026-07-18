with open("src/features.tsx", "r") as f:
    content = f.read()

import re

mats_admin_code = """export function CourseMaterialsAdminTab({ subjectId }: { subjectId: string }) {
  const [materials, setMaterials] = useState<CourseMaterial[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [newMat, setNewMat] = useState<Partial<CourseMaterial>>({ type: 'video', unit: 1, title: '', contentUrl: '', description: '' });
  const [filterUnit, setFilterUnit] = useState<number | 'all'>('all');

  const fetchMats = async () => {
    const q = query(collection(db, 'materials'), where('subjectId', '==', subjectId), orderBy('createdAt', 'desc'));
    const snap = await getDocs(q);
    const data = snap.docs.map(d => ({ id: d.id, ...d.data() } as CourseMaterial));
    data.sort((a, b) => a.unit - b.unit || b.createdAt - a.createdAt);
    setMaterials(data);
  };

  useEffect(() => { fetchMats(); }, [subjectId]);

  const handleSave = async () => {
    if (!newMat.title || !newMat.contentUrl) return toast('請填寫完整資訊');
    if (editingId) {
      await updateDoc(doc(db, 'materials', editingId), {
        ...newMat
      });
      toast('更新成功');
    } else {
      await addDoc(collection(db, 'materials'), {
        ...newMat, subjectId, createdAt: Date.now()
      });
      toast('新增成功');
    }
    setShowForm(false);
    setEditingId(null);
    setNewMat({ type: 'video', unit: filterUnit === 'all' ? 1 : filterUnit, title: '', contentUrl: '', description: '' });
    fetchMats();
  };

  const handleEdit = (m: CourseMaterial) => {
    setNewMat(m);
    setEditingId(m.id!);
    setShowForm(true);
  };

  const handleDelete = async (id: string) => {
    if (confirm('確定刪除此教材？無法復原。')) {
      await deleteDoc(doc(db, 'materials', id));
      toast('刪除成功');
      fetchMats();
    }
  };

  const units = Array.from(new Set(materials.map(m => m.unit))).sort((a, b) => a - b);
  const filteredMats = filterUnit === 'all' ? materials : materials.filter(m => m.unit === filterUnit);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h3 className="font-serif font-black text-2xl text-[#4A3F35]">教材編輯系統</h3>
          <p className="text-[#8C7A6B] mt-1 text-sm">管理此科目的所有線上影音、文件教材。</p>
        </div>
        <button onClick={() => {
          if (showForm) {
            setShowForm(false); setEditingId(null);
          } else {
            setNewMat({ type: 'video', unit: filterUnit === 'all' ? 1 : filterUnit, title: '', contentUrl: '', description: '' });
            setShowForm(true);
          }
        }} className="bg-[#C2A878] text-[#4A3F35] px-6 py-2 rounded-lg font-bold hover:bg-[#B39969] transition-all shadow-sm">
          {showForm ? '取消編輯' : '➕ 新增教材'}
        </button>
      </div>

      {showForm && (
        <div className="bg-white p-8 rounded-3xl border border-[#EAE6DF] shadow-md space-y-6 animate-in slide-in-from-top-4">
          <div className="flex items-center gap-2 mb-4">
            <BookOpen className="text-[#C2A878]" />
            <h4 className="font-bold text-lg text-[#4A3F35]">{editingId ? '編輯教材' : '新增教材'}</h4>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <label className="text-sm font-bold text-[#8C7A6B]">所屬單元</label>
              <input type="number" min="1" value={newMat.unit} onChange={e => setNewMat({...newMat, unit: parseInt(e.target.value)||1})} className="w-full bg-[#FDFBF7] border border-[#D5CFC4] rounded-xl px-4 py-3 focus:outline-none focus:border-[#C2A878]" />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-bold text-[#8C7A6B]">教材類型</label>
              <select value={newMat.type} onChange={e => setNewMat({...newMat, type: e.target.value as any})} className="w-full bg-[#FDFBF7] border border-[#D5CFC4] rounded-xl px-4 py-3 focus:outline-none focus:border-[#C2A878]">
                <option value="video">🎥 影片 (YouTube/MP4)</option>
                <option value="pdf">📄 PDF 講義</option>
                <option value="article">🔗 外部文章/網頁</option>
              </select>
            </div>
            <div className="space-y-2 md:col-span-2">
              <label className="text-sm font-bold text-[#8C7A6B]">教材標題</label>
              <input type="text" placeholder="例如：第一課 恆星的奧秘" value={newMat.title || ''} onChange={e => setNewMat({...newMat, title: e.target.value})} className="w-full bg-[#FDFBF7] border border-[#D5CFC4] rounded-xl px-4 py-3 focus:outline-none focus:border-[#C2A878]" />
            </div>
            <div className="space-y-2 md:col-span-2">
              <label className="text-sm font-bold text-[#8C7A6B]">內容連結 (URL)</label>
              <input type="text" placeholder="https://..." value={newMat.contentUrl || ''} onChange={e => setNewMat({...newMat, contentUrl: e.target.value})} className="w-full bg-[#FDFBF7] border border-[#D5CFC4] rounded-xl px-4 py-3 focus:outline-none focus:border-[#C2A878]" />
              <p className="text-xs text-[#A69B8F]">影片請貼 YouTube 網址，PDF 請貼公開可存取之網址。</p>
            </div>
            <div className="space-y-2 md:col-span-2">
              <label className="text-sm font-bold text-[#8C7A6B]">詳細說明 / 教學指引</label>
              <textarea placeholder="寫下這份教材的學習重點..." rows={4} value={newMat.description || ''} onChange={e => setNewMat({...newMat, description: e.target.value})} className="w-full bg-[#FDFBF7] border border-[#D5CFC4] rounded-xl px-4 py-3 focus:outline-none focus:border-[#C2A878]" />
            </div>
            <div className="md:col-span-2 flex justify-end pt-4">
              <button onClick={handleSave} className="bg-[#4A3F35] text-white px-8 py-3 rounded-xl font-bold shadow-md hover:bg-[#3A3025] transition-all">
                {editingId ? '儲存變更' : '確定新增'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Unit Filter */}
      {!showForm && units.length > 0 && (
        <div className="flex items-center gap-2 overflow-x-auto pb-2">
          <button 
            onClick={() => setFilterUnit('all')} 
            className={`px-4 py-2 rounded-full text-sm font-bold whitespace-nowrap transition-colors ${filterUnit === 'all' ? 'bg-[#4A3F35] text-white' : 'bg-white text-[#8C7A6B] hover:bg-[#FDFBF7] border border-[#EAE6DF]'}`}
          >
            全部單元
          </button>
          {units.map(u => (
            <button 
              key={u} 
              onClick={() => setFilterUnit(u)} 
              className={`px-4 py-2 rounded-full text-sm font-bold whitespace-nowrap transition-colors ${filterUnit === u ? 'bg-[#4A3F35] text-white' : 'bg-white text-[#8C7A6B] hover:bg-[#FDFBF7] border border-[#EAE6DF]'}`}
            >
              單元 {u}
            </button>
          ))}
        </div>
      )}

      {!showForm && (
        <div className="space-y-4">
          {filteredMats.map(m => (
            <div key={m.id} className="bg-white p-5 rounded-2xl border border-[#EAE6DF] shadow-sm flex flex-col md:flex-row gap-6 items-start group hover:border-[#C2A878] transition-colors relative">
              <div className="absolute top-4 right-4 flex opacity-0 group-hover:opacity-100 transition-opacity gap-2">
                <button onClick={() => handleEdit(m)} className="bg-[#EAE2D3] text-[#4A3F35] px-3 py-1.5 rounded-lg text-xs font-bold hover:bg-[#D5CFC4]">編輯</button>
                <button onClick={() => handleDelete(m.id!)} className="bg-[#BC7665] text-white px-3 py-1.5 rounded-lg text-xs font-bold hover:bg-[#A35D4C]">刪除</button>
              </div>
              
              <div className={`w-16 h-16 rounded-2xl flex items-center justify-center shrink-0 ${m.type === 'video' ? 'bg-red-50 text-red-500' : m.type === 'pdf' ? 'bg-blue-50 text-blue-500' : 'bg-green-50 text-green-500'}`}>
                {m.type === 'video' ? <Video size={32} /> : m.type === 'pdf' ? <FileText size={32} /> : <BookOpen size={32} />}
              </div>
              <div className="flex-1 pr-24">
                <div className="flex items-center gap-3 mb-1">
                  <span className="bg-[#F5F5F0] text-[#8C7A6B] text-[10px] font-bold px-2 py-0.5 rounded-full border border-[#EAE6DF]">單元 {m.unit}</span>
                  <span className="text-[10px] font-bold text-[#A69B8F] uppercase tracking-wider">{m.type}</span>
                </div>
                <h4 className="text-xl font-bold text-[#4A3F35] mb-2">{m.title}</h4>
                <p className="text-sm text-[#8C7A6B] leading-relaxed">{m.description}</p>
                <a href={m.contentUrl} target="_blank" rel="noreferrer" className="inline-block mt-3 text-sm font-bold text-[#C2A878] hover:text-[#B39969] underline underline-offset-4">測試連結 ↗</a>
              </div>
            </div>
          ))}
          {filteredMats.length === 0 && (
            <div className="text-center py-20 bg-white border border-[#EAE6DF] rounded-3xl">
              <BookOpen className="mx-auto text-[#D5CFC4] mb-4" size={48} />
              <p className="text-[#A69B8F] font-bold">此區間目前沒有教材</p>
              <p className="text-sm text-[#D5CFC4] mt-1">點擊上方「新增教材」開始建立教學內容</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}"""

pattern = re.compile(r"export function CourseMaterialsAdminTab.*?^}$", re.MULTILINE | re.DOTALL)
content = pattern.sub(mats_admin_code, content)

with open("src/features.tsx", "w") as f:
    f.write(content)
