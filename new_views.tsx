export function CourseMaterialsAdminTab({ subjectId }: { subjectId: string }) {
  const [materials, setMaterials] = useState<CourseMaterial[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [newMat, setNewMat] = useState<Partial<CourseMaterial>>({ type: 'lesson', unit: 1, title: '', contentUrl: '', description: '', markdownNotes: '', attachments: [] });
  const [filterUnit, setFilterUnit] = useState<number | 'all'>('all');
  const [uploading, setUploading] = useState(false);

  const fetchMats = async () => {
    const q = query(collection(db, 'materials'), where('subjectId', '==', subjectId));
    const snap = await getDocs(q);
    const data = snap.docs.map(d => ({ id: d.id, ...d.data() } as CourseMaterial));
    data.sort((a, b) => a.unit - b.unit || b.createdAt - a.createdAt);
    setMaterials(data);
  };

  useEffect(() => { fetchMats(); }, [subjectId]);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
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
  };

  const removeAttachment = (index: number) => {
    const newAtt = [...(newMat.attachments || [])];
    newAtt.splice(index, 1);
    setNewMat({ ...newMat, attachments: newAtt });
  };

  const handleSave = async () => {
    if (!newMat.title) return toast('請填寫教材標題');
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
    setNewMat({ type: 'lesson', unit: filterUnit === 'all' ? 1 : filterUnit as number, title: '', contentUrl: '', description: '', markdownNotes: '', attachments: [] });
    fetchMats();
  };

  const handleEdit = (m: CourseMaterial) => {
    setNewMat({ ...m, attachments: m.attachments || [], markdownNotes: m.markdownNotes || '' });
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
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
        <div>
          <h3 className="font-serif font-black text-2xl text-[#4A3F35]">綜合教材編輯系統</h3>
          <p className="text-[#8C7A6B] mt-1 text-sm">支援影片、Markdown 筆記、多檔案上傳，打造豐富的線上課程體驗。</p>
        </div>
        <button onClick={() => {
          if (showForm) {
            setShowForm(false); setEditingId(null);
          } else {
            setNewMat({ type: 'lesson', unit: filterUnit === 'all' ? 1 : filterUnit as number, title: '', contentUrl: '', description: '', markdownNotes: '', attachments: [] });
            setShowForm(true);
          }
        }} className="bg-[#C2A878] text-[#4A3F35] px-6 py-2 rounded-lg font-bold hover:bg-[#B39969] transition-all shadow-sm flex items-center gap-2 shrink-0">
          {showForm ? <X size={18} /> : <Plus size={18} />}
          {showForm ? '取消編輯' : '新增課程單元'}
        </button>
      </div>

      {showForm && (
        <div className="bg-white p-6 md:p-8 rounded-3xl border border-[#EAE6DF] shadow-xl space-y-6 animate-in slide-in-from-top-4 relative z-10">
          <div className="flex items-center gap-2 border-b border-[#EAE6DF] pb-4">
            <BookOpen className="text-[#C2A878]" />
            <h4 className="font-bold text-xl text-[#4A3F35]">{editingId ? '編輯單元內容' : '新增單元內容'}</h4>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="space-y-4 md:col-span-1 border-r-0 md:border-r border-[#EAE6DF] pr-0 md:pr-6">
              <div className="space-y-2">
                <label className="text-sm font-bold text-[#8C7A6B]">所屬單元 (Unit)</label>
                <input type="number" value={newMat.unit} onChange={e => setNewMat({ ...newMat, unit: Number(e.target.value) })} className="w-full border border-[#EAE6DF] rounded-xl p-3 bg-[#FDFBF7] focus:ring-2 focus:ring-[#C2A878] outline-none" min="1" />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-bold text-[#8C7A6B]">教材類型</label>
                <select value={newMat.type} onChange={e => setNewMat({ ...newMat, type: e.target.value as any })} className="w-full border border-[#EAE6DF] rounded-xl p-3 bg-[#FDFBF7] focus:ring-2 focus:ring-[#C2A878] outline-none">
                  <option value="lesson">綜合課程 (推薦)</option>
                  <option value="video">純影片</option>
                  <option value="pdf">純PDF</option>
                  <option value="article">純文章</option>
                </select>
              </div>
              <div className="space-y-2">
                <label className="text-sm font-bold text-[#8C7A6B]">主標題</label>
                <input type="text" placeholder="例如：CH1-1 宇宙的起源" value={newMat.title} onChange={e => setNewMat({ ...newMat, title: e.target.value })} className="w-full border border-[#EAE6DF] rounded-xl p-3 bg-[#FDFBF7] focus:ring-2 focus:ring-[#C2A878] outline-none" />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-bold text-[#8C7A6B]">簡短描述</label>
                <textarea rows={3} placeholder="課程大綱或摘要..." value={newMat.description} onChange={e => setNewMat({ ...newMat, description: e.target.value })} className="w-full border border-[#EAE6DF] rounded-xl p-3 bg-[#FDFBF7] focus:ring-2 focus:ring-[#C2A878] outline-none resize-none" />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-bold text-[#8C7A6B]">主要影片 / 連結 URL (選填)</label>
                <input type="text" placeholder="YouTube 網址或雲端連結" value={newMat.contentUrl} onChange={e => setNewMat({ ...newMat, contentUrl: e.target.value })} className="w-full border border-[#EAE6DF] rounded-xl p-3 bg-[#FDFBF7] focus:ring-2 focus:ring-[#C2A878] outline-none" />
              </div>
            </div>

            <div className="space-y-6 md:col-span-2">
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <label className="text-sm font-bold text-[#8C7A6B]">Markdown 課程筆記</label>
                  <span className="text-xs text-[#A69B8F]">支援 Markdown 語法</span>
                </div>
                <textarea 
                  rows={8} 
                  placeholder="在此輸入豐富的課程內容...支援 **粗體**, # 標題, - 列表 等 Markdown 語法" 
                  value={newMat.markdownNotes || ''} 
                  onChange={e => setNewMat({ ...newMat, markdownNotes: e.target.value })} 
                  className="w-full border border-[#EAE6DF] rounded-xl p-4 bg-[#FDFBF7] focus:ring-2 focus:ring-[#C2A878] outline-none resize-y font-mono text-sm leading-relaxed" 
                />
              </div>

              <div className="space-y-3 bg-[#F5F5F0] p-4 rounded-2xl border border-[#EAE6DF]">
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
              </div>
            </div>
          </div>

          <div className="flex justify-end gap-3 pt-4 border-t border-[#EAE6DF]">
            <button onClick={() => { setShowForm(false); setEditingId(null); }} className="px-6 py-2 rounded-lg text-[#8C7A6B] font-bold hover:bg-[#F5F5F0]">取消</button>
            <button onClick={handleSave} className="bg-[#4A3F35] text-white px-8 py-2 rounded-lg font-bold hover:bg-[#2A241E] shadow-md transition-all">
              儲存發布
            </button>
          </div>
        </div>
      )}

      {!showForm && (
        <div className="space-y-4">
          <div className="flex gap-2 overflow-x-auto pb-2">
            <button onClick={() => setFilterUnit('all')} className={`px-4 py-1.5 rounded-full text-sm font-bold whitespace-nowrap transition-all ${filterUnit === 'all' ? 'bg-[#4A3F35] text-white shadow-md' : 'bg-white text-[#8C7A6B] border border-[#EAE6DF] hover:bg-[#F5F5F0]'}`}>全部單元</button>
            {units.map(u => (
              <button key={u} onClick={() => setFilterUnit(u)} className={`px-4 py-1.5 rounded-full text-sm font-bold whitespace-nowrap transition-all ${filterUnit === u ? 'bg-[#4A3F35] text-white shadow-md' : 'bg-white text-[#8C7A6B] border border-[#EAE6DF] hover:bg-[#F5F5F0]'}`}>Unit {u}</button>
            ))}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredMats.map(m => (
              <div key={m.id} className="bg-white p-5 rounded-2xl border border-[#EAE6DF] shadow-sm hover:shadow-md transition-all group flex flex-col h-full">
                <div className="flex justify-between items-start mb-3">
                  <span className="bg-[#F5F5F0] text-[#8C7A6B] text-xs font-bold px-2 py-1 rounded-md">Unit {m.unit}</span>
                  <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button onClick={() => handleEdit(m)} className="p-1.5 text-[#8C7A6B] hover:text-[#4A3F35] hover:bg-[#F5F5F0] rounded-md transition-colors"><BookOpen size={16} /></button>
                    <button onClick={() => handleDelete(m.id!)} className="p-1.5 text-red-400 hover:text-red-600 hover:bg-red-50 rounded-md transition-colors"><Trash size={16} /></button>
                  </div>
                </div>
                <div className="flex items-start gap-3 flex-1">
                  <div className="mt-1 bg-[#FDFBF7] p-2 rounded-lg border border-[#EAE6DF] text-[#C2A878]">
                    {m.type === 'video' ? <Video size={20} /> : m.type === 'pdf' ? <FileText size={20} /> : m.type === 'lesson' ? <Layout size={20} /> : <BookOpen size={20} />}
                  </div>
                  <div>
                    <h5 className="font-bold text-[#4A3F35] leading-tight">{m.title}</h5>
                    <p className="text-sm text-[#8C7A6B] mt-1 line-clamp-2">{m.description}</p>
                    
                    <div className="flex gap-3 mt-3 text-xs text-[#A69B8F] font-medium">
                      {m.attachments && m.attachments.length > 0 && (
                        <span className="flex items-center gap-1"><Paperclip size={12}/> {m.attachments.length} 個附件</span>
                      )}
                      {m.markdownNotes && (
                        <span className="flex items-center gap-1"><FileText size={12}/> 筆記</span>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
            {filteredMats.length === 0 && (
              <div className="col-span-full py-12 text-center bg-[#FDFBF7] rounded-3xl border border-dashed border-[#D1CCC5]">
                <BookOpen className="mx-auto text-[#D1CCC5] mb-2" size={32} />
                <p className="text-[#8C7A6B] font-bold">此單元目前沒有教材</p>
                <p className="text-sm text-[#A69B8F] mt-1">點擊右上方新增教材按鈕開始建立</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export function CourseMaterialsStudentView({ subjectId, user }: { subjectId: string, user: UserProfile }) {
  const [materials, setMaterials] = useState<CourseMaterial[]>([]);
  const [activeMat, setActiveMat] = useState<CourseMaterial | null>(null);

  useEffect(() => {
    const fetchMats = async () => {
      const q = query(collection(db, 'materials'), where('subjectId', '==', subjectId));
      const snap = await getDocs(q);
      const data = snap.docs.map(d => ({ id: d.id, ...d.data() } as CourseMaterial));
      data.sort((a, b) => a.unit - b.unit || b.createdAt - a.createdAt);
      setMaterials(data);
      if (data.length > 0 && !activeMat) {
        setActiveMat(data[0]);
      }
    };
    fetchMats();
  }, [subjectId]);

  const units = Array.from(new Set(materials.map(m => m.unit))).sort((a, b) => a - b);

  return (
    <div className="flex flex-col lg:flex-row gap-6 items-start h-[calc(100vh-140px)]">
      {/* Sidebar Navigation */}
      <div className="w-full lg:w-80 shrink-0 bg-white rounded-3xl border border-[#EAE6DF] shadow-sm overflow-hidden flex flex-col h-full max-h-full">
        <div className="p-5 border-b border-[#EAE6DF] bg-[#FDFBF7]">
          <h3 className="font-serif font-black text-xl text-[#4A3F35]">課程目錄</h3>
          <p className="text-sm text-[#8C7A6B] mt-1">共 {materials.length} 個章節</p>
        </div>
        <div className="overflow-y-auto flex-1 p-3 space-y-4">
          {units.map(u => {
            const unitMats = materials.filter(m => m.unit === u);
            return (
              <div key={u} className="space-y-1">
                <h4 className="text-xs font-bold text-[#A69B8F] uppercase tracking-wider px-3 mb-2">Unit {u}</h4>
                {unitMats.map(m => (
                  <button 
                    key={m.id} 
                    onClick={() => setActiveMat(m)} 
                    className={`w-full text-left px-4 py-3 rounded-xl transition-all flex items-start gap-3 group ${activeMat?.id === m.id ? 'bg-[#4A3F35] text-white shadow-md' : 'hover:bg-[#F5F5F0] text-[#4A3F35]'}`}
                  >
                    <div className={`mt-0.5 ${activeMat?.id === m.id ? 'text-[#C2A878]' : 'text-[#8C7A6B] group-hover:text-[#4A3F35]'}`}>
                      {m.type === 'video' ? <Video size={18} /> : m.type === 'pdf' ? <FileText size={18} /> : m.type === 'lesson' ? <Layout size={18} /> : <BookOpen size={18} />}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className={`font-bold text-sm truncate ${activeMat?.id === m.id ? 'text-white' : 'text-[#4A3F35]'}`}>{m.title}</p>
                      <p className={`text-xs truncate mt-0.5 ${activeMat?.id === m.id ? 'text-white/70' : 'text-[#8C7A6B]'}`}>{m.description}</p>
                    </div>
                  </button>
                ))}
              </div>
            );
          })}
          {materials.length === 0 && (
            <div className="text-center py-8 text-[#A69B8F] text-sm font-medium">
              尚未發布任何教材
            </div>
          )}
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 w-full bg-white rounded-3xl border border-[#EAE6DF] shadow-sm overflow-hidden h-full max-h-full flex flex-col">
        {activeMat ? (
          <div className="overflow-y-auto flex-1 bg-[#FDFBF7]">
            {/* Header */}
            <div className="p-6 md:p-10 border-b border-[#EAE6DF] bg-white sticky top-0 z-10">
              <div className="flex items-center gap-2 text-sm text-[#C2A878] font-bold mb-3">
                <span className="bg-[#FDFBF7] border border-[#EAE6DF] px-2 py-0.5 rounded-md">Unit {activeMat.unit}</span>
                <span>•</span>
                <span className="uppercase tracking-wider">{activeMat.type}</span>
              </div>
              <h1 className="text-3xl font-serif font-black text-[#4A3F35]">{activeMat.title}</h1>
              {activeMat.description && (
                <p className="text-[#8C7A6B] mt-3 text-lg leading-relaxed">{activeMat.description}</p>
              )}
            </div>

            <div className="p-6 md:p-10 space-y-10">
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
                    <div className="aspect-[1/1.4] w-full">
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
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center bg-[#FDFBF7] text-center p-10">
            <div className="bg-white p-6 rounded-full shadow-sm border border-[#EAE6DF] mb-6">
              <Layout size={48} className="text-[#D1CCC5]" />
            </div>
            <h2 className="text-2xl font-serif font-black text-[#4A3F35]">歡迎來到課程中心</h2>
            <p className="text-[#8C7A6B] mt-2 max-w-sm">請從左側目錄選擇一個章節開始學習。所有的影音、筆記與講義都在這裡為你準備好了。</p>
          </div>
        )}
      </div>
    </div>
  );
}
