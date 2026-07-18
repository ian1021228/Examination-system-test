with open("src/features.tsx", "w") as f:
    f.write("""import React, { useState, useEffect } from 'react';
import { collection, query, where, getDocs, addDoc, deleteDoc, doc, updateDoc, orderBy, limit, onSnapshot } from 'firebase/firestore';
import { db, auth } from './App';
import type { UserProfile, Subject } from './App';
import { useNavigate, useParams, Link } from 'react-router-dom';
import { BookOpen, Video, FileText, MessageCircle, Send, Award, Trash, Star, Play, CheckCircle, ChevronRight, Layout, Info, User, Volume2, Calendar } from 'lucide-react';
import { toast } from './toast';

export interface Announcement {
  id?: string;
  title: string;
  content: string;
  author: string;
  createdAt: number;
}

export interface CourseMaterial {
  id?: string;
  subjectId: string;
  unit: number;
  type: 'video' | 'pdf' | 'article';
  title: string;
  contentUrl: string;
  description: string;
  createdAt: number;
}

export interface DiscussionMsg {
  id?: string;
  targetId: string; // can be a taskId, subjectId, or specific materialId
  authorId: string;
  authorName: string;
  content: string;
  createdAt: number;
}

const SUBJECT_LABELS: Record<string, string> = {
  chinese: '國語',
  math: '數學',
  science: '自然',
  social_studies: '社會',
  ket: '英文檢定'
};

export function LandingPage() {
  const navigate = useNavigate();
  const [announcements, setAnnouncements] = useState<Announcement[]>([]);

  useEffect(() => {
    const q = query(collection(db, 'announcements'), orderBy('createdAt', 'desc'), limit(5));
    const unsub = onSnapshot(q, (snap) => {
      setAnnouncements(snap.docs.map(d => ({ id: d.id, ...d.data() } as Announcement)));
    });
    return unsub;
  }, []);

  return (
    <div className="w-full">
      {/* Hero Section */}
      <div className="bg-[#4A3F35] text-[#FDFBF7] py-20 px-6 sm:px-12 rounded-b-[3rem] shadow-xl">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between">
          <div className="md:w-1/2 space-y-6">
            <h1 className="text-5xl font-black font-serif leading-tight">
              探索知識的宇宙<br/><span className="text-[#C2A878]">數位學習平台</span>
            </h1>
            <p className="text-[#D5CFC4] text-lg max-w-md">
              結合最新多媒體教材與遊戲化測驗，先看課、後測驗。與同儕一起討論，獲取學習成就，讓學習不再枯燥！
            </p>
            <div className="flex gap-4">
              <button onClick={() => navigate('/select-subject')} className="bg-[#C2A878] text-[#4A3F35] px-8 py-3 rounded-full font-bold hover:bg-[#B39969] transition-all flex items-center gap-2">
                開始學習 <ChevronRight size={20} />
              </button>
            </div>
          </div>
          <div className="md:w-1/2 mt-12 md:mt-0 flex justify-center">
            <div className="relative">
              <div className="absolute inset-0 bg-[#C2A878] blur-3xl opacity-20 rounded-full"></div>
              <img src="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" alt="Students learning" className="relative rounded-3xl shadow-2xl border-4 border-[#5A4F45] object-cover w-full h-[300px] md:h-[400px]" />
            </div>
          </div>
        </div>
      </div>

      {/* Announcements */}
      <div className="max-w-6xl mx-auto py-16 px-6">
        <div className="flex items-center gap-2 mb-8">
          <Calendar className="text-[#C2A878]" size={28} />
          <h2 className="text-3xl font-bold text-[#4A3F35] font-serif">最新公告</h2>
        </div>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {announcements.map(a => (
            <div key={a.id} className="bg-white border border-[#EAE6DF] rounded-2xl p-6 shadow-sm hover:shadow-md transition-all group">
              <div className="flex justify-between items-start mb-4">
                <h3 className="font-bold text-lg text-[#4A3F35] group-hover:text-[#B39969] transition-colors">{a.title}</h3>
              </div>
              <p className="text-[#8C7A6B] text-sm line-clamp-3">{a.content}</p>
              <div className="mt-4 pt-4 border-t border-[#EAE6DF] flex justify-between text-xs text-[#A69B8F]">
                <span>{a.author}</span>
                <span>{new Date(a.createdAt).toLocaleDateString()}</span>
              </div>
            </div>
          ))}
          {announcements.length === 0 && (
            <div className="col-span-full text-center py-10 text-[#A69B8F]">目前沒有最新公告</div>
          )}
        </div>
      </div>

      {/* Features */}
      <div className="bg-[#FDFBF7] py-16 px-6">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-[#4A3F35] font-serif mb-12 text-center">平台特色</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white p-8 rounded-3xl shadow-sm border border-[#EAE6DF] text-center">
              <div className="bg-[#EAE2D3] w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-6 text-[#B39969]">
                <Video size={32} />
              </div>
              <h3 className="text-xl font-bold text-[#4A3F35] mb-4">先看課、後測驗</h3>
              <p className="text-[#8C7A6B]">豐富的影音與圖文教材，讓學生在測驗前先建立扎實基礎，提升學習成效。</p>
            </div>
            <div className="bg-white p-8 rounded-3xl shadow-sm border border-[#EAE6DF] text-center">
              <div className="bg-[#EAE2D3] w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-6 text-[#B39969]">
                <MessageCircle size={32} />
              </div>
              <h3 className="text-xl font-bold text-[#4A3F35] mb-4">師生即時討論</h3>
              <p className="text-[#8C7A6B]">專屬課程討論區，有問題隨時發問，老師與同學共同解答，營造共學氛圍。</p>
            </div>
            <div className="bg-white p-8 rounded-3xl shadow-sm border border-[#EAE6DF] text-center">
              <div className="bg-[#EAE2D3] w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-6 text-[#B39969]">
                <Award size={32} />
              </div>
              <h3 className="text-xl font-bold text-[#4A3F35] mb-4">遊戲化成就系統</h3>
              <p className="text-[#8C7A6B]">解鎖徽章、累積經驗值升級，讓學習像玩遊戲一樣充滿成就感與動力。</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export function AnnouncementsAdminTab() {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [announcements, setAnnouncements] = useState<Announcement[]>([]);

  const fetchAnnouncements = async () => {
    const q = query(collection(db, 'announcements'), orderBy('createdAt', 'desc'));
    const snap = await getDocs(q);
    setAnnouncements(snap.docs.map(d => ({ id: d.id, ...d.data() } as Announcement)));
  };

  useEffect(() => { fetchAnnouncements(); }, []);

  const handlePost = async () => {
    if (!title.trim() || !content.trim()) return;
    await addDoc(collection(db, 'announcements'), {
      title, content, author: '系統管理員', createdAt: Date.now()
    });
    toast('發布成功！');
    setTitle(''); setContent('');
    fetchAnnouncements();
  };

  const handleDelete = async (id: string) => {
    if (confirm('確定刪除此公告？')) {
      await deleteDoc(doc(db, 'announcements', id));
      toast('刪除成功');
      fetchAnnouncements();
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-2xl border border-[#EAE6DF] shadow-sm space-y-4">
        <h3 className="font-bold text-[#4A3F35] text-lg">發布新公告</h3>
        <input type="text" placeholder="公告標題" value={title} onChange={e => setTitle(e.target.value)} className="w-full bg-[#FDFBF7] border border-[#D5CFC4] rounded-lg px-4 py-2" />
        <textarea placeholder="公告內容" value={content} onChange={e => setContent(e.target.value)} className="w-full bg-[#FDFBF7] border border-[#D5CFC4] rounded-lg px-4 py-2 h-32" />
        <button onClick={handlePost} className="bg-[#C2A878] text-[#4A3F35] px-6 py-2 rounded-lg font-bold hover:bg-[#B39969]">發布公告</button>
      </div>

      <div className="space-y-4">
        <h3 className="font-bold text-[#4A3F35] text-lg">歷史公告</h3>
        {announcements.map(a => (
          <div key={a.id} className="bg-white p-4 rounded-xl border border-[#EAE6DF] flex justify-between items-start">
            <div>
              <h4 className="font-bold text-[#4A3F35]">{a.title}</h4>
              <p className="text-sm text-[#8C7A6B] mt-1">{a.content}</p>
              <p className="text-xs text-[#A69B8F] mt-2">{new Date(a.createdAt).toLocaleString()}</p>
            </div>
            <button onClick={() => handleDelete(a.id!)} className="text-[#BC7665] hover:bg-[#FDFBF7] p-2 rounded-lg"><Trash size={16}/></button>
          </div>
        ))}
      </div>
    </div>
  );
}

export function CourseMaterialsAdminTab({ subjectId }: { subjectId: string }) {
  const [materials, setMaterials] = useState<CourseMaterial[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [newMat, setNewMat] = useState<Partial<CourseMaterial>>({ type: 'video', unit: 1 });

  const fetchMats = async () => {
    const q = query(collection(db, 'materials'), where('subjectId', '==', subjectId), orderBy('createdAt', 'desc'));
    const snap = await getDocs(q);
    setMaterials(snap.docs.map(d => ({ id: d.id, ...d.data() } as CourseMaterial)));
  };

  useEffect(() => { fetchMats(); }, [subjectId]);

  const handleAdd = async () => {
    if (!newMat.title || !newMat.contentUrl) return toast('請填寫完整資訊');
    await addDoc(collection(db, 'materials'), {
      ...newMat, subjectId, createdAt: Date.now()
    });
    toast('新增成功');
    setShowForm(false);
    fetchMats();
  };

  const handleDelete = async (id: string) => {
    if (confirm('確定刪除教材？')) {
      await deleteDoc(doc(db, 'materials', id));
      toast('刪除成功');
      fetchMats();
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h3 className="font-bold text-xl text-[#4A3F35]">課程教材管理</h3>
        <button onClick={() => setShowForm(!showForm)} className="bg-[#C2A878] text-[#4A3F35] px-4 py-2 rounded-lg font-bold">
          {showForm ? '取消' : '新增教材'}
        </button>
      </div>

      {showForm && (
        <div className="bg-white p-6 rounded-2xl border border-[#EAE6DF] shadow-sm space-y-4 grid grid-cols-2 gap-4">
          <div className="col-span-2 md:col-span-1">
            <label className="text-xs text-[#8C7A6B]">類型</label>
            <select value={newMat.type} onChange={e => setNewMat({...newMat, type: e.target.value as any})} className="w-full bg-[#FDFBF7] border border-[#D5CFC4] rounded-lg px-4 py-2 mt-1">
              <option value="video">影片 (YouTube)</option>
              <option value="pdf">PDF 講義</option>
              <option value="article">文章閱讀連結</option>
            </select>
          </div>
          <div className="col-span-2 md:col-span-1">
             <label className="text-xs text-[#8C7A6B]">單元</label>
             <input type="number" value={newMat.unit} onChange={e => setNewMat({...newMat, unit: parseInt(e.target.value)})} className="w-full bg-[#FDFBF7] border border-[#D5CFC4] rounded-lg px-4 py-2 mt-1" />
          </div>
          <div className="col-span-2">
            <label className="text-xs text-[#8C7A6B]">標題</label>
            <input type="text" value={newMat.title || ''} onChange={e => setNewMat({...newMat, title: e.target.value})} className="w-full bg-[#FDFBF7] border border-[#D5CFC4] rounded-lg px-4 py-2 mt-1" />
          </div>
          <div className="col-span-2">
            <label className="text-xs text-[#8C7A6B]">內容網址 (URL)</label>
            <input type="text" value={newMat.contentUrl || ''} onChange={e => setNewMat({...newMat, contentUrl: e.target.value})} className="w-full bg-[#FDFBF7] border border-[#D5CFC4] rounded-lg px-4 py-2 mt-1" />
          </div>
          <div className="col-span-2">
            <label className="text-xs text-[#8C7A6B]">簡介描述</label>
            <textarea value={newMat.description || ''} onChange={e => setNewMat({...newMat, description: e.target.value})} className="w-full bg-[#FDFBF7] border border-[#D5CFC4] rounded-lg px-4 py-2 mt-1" />
          </div>
          <div className="col-span-2">
            <button onClick={handleAdd} className="bg-[#4A3F35] text-white px-6 py-2 rounded-lg font-bold w-full">儲存教材</button>
          </div>
        </div>
      )}

      <div className="grid md:grid-cols-2 gap-4">
        {materials.map(m => (
          <div key={m.id} className="bg-white p-5 rounded-2xl border border-[#EAE6DF] shadow-sm flex items-start gap-4">
            <div className="bg-[#EAE2D3] p-3 rounded-xl text-[#B39969]">
              {m.type === 'video' ? <Video /> : m.type === 'pdf' ? <FileText /> : <BookOpen />}
            </div>
            <div className="flex-1">
              <div className="flex justify-between items-start">
                <h4 className="font-bold text-[#4A3F35]">{m.title}</h4>
                <button onClick={() => handleDelete(m.id!)} className="text-[#BC7665] hover:bg-[#FDFBF7] p-1 rounded-lg"><Trash size={16}/></button>
              </div>
              <p className="text-xs text-[#A69B8F] mt-1">單元 {m.unit} • {m.type.toUpperCase()}</p>
              <p className="text-sm text-[#8C7A6B] mt-2 line-clamp-2">{m.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export function DiscussionBoard({ targetId, user }: { targetId: string, user: UserProfile }) {
  const [messages, setMessages] = useState<DiscussionMsg[]>([]);
  const [input, setInput] = useState('');

  useEffect(() => {
    const q = query(collection(db, 'discussions'), where('targetId', '==', targetId), orderBy('createdAt', 'asc'));
    const unsub = onSnapshot(q, (snap) => {
      setMessages(snap.docs.map(d => ({ id: d.id, ...d.data() } as DiscussionMsg)));
    });
    return unsub;
  }, [targetId]);

  const handleSend = async () => {
    if (!input.trim()) return;
    await addDoc(collection(db, 'discussions'), {
      targetId,
      authorId: user.uid,
      authorName: user.displayName || '匿名學生',
      content: input,
      createdAt: Date.now()
    });
    setInput('');
  };

  return (
    <div className="bg-white rounded-2xl border border-[#EAE6DF] shadow-sm flex flex-col h-[400px]">
      <div className="p-4 border-b border-[#EAE6DF] flex items-center gap-2">
        <MessageCircle size={20} className="text-[#C2A878]"/>
        <h3 className="font-bold text-[#4A3F35]">討論區 / Q&A</h3>
      </div>
      <div className="flex-1 p-4 overflow-y-auto space-y-4">
        {messages.length === 0 && <p className="text-center text-[#A69B8F] mt-10">目前尚無討論，來發起第一個問題吧！</p>}
        {messages.map(m => (
          <div key={m.id} className={`flex flex-col ${m.authorId === user.uid ? 'items-end' : 'items-start'}`}>
            <span className="text-[10px] text-[#A69B8F] mb-1 px-1">{m.authorName} • {new Date(m.createdAt).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
            <div className={`px-4 py-2 rounded-2xl max-w-[80%] ${m.authorId === user.uid ? 'bg-[#C2A878] text-white rounded-br-none' : 'bg-[#FDFBF7] border border-[#EAE6DF] text-[#4A3F35] rounded-bl-none'}`}>
              {m.content}
            </div>
          </div>
        ))}
      </div>
      <div className="p-4 border-t border-[#EAE6DF] flex gap-2">
        <input 
          type="text" 
          value={input} 
          onChange={e => setInput(e.target.value)} 
          onKeyDown={e => e.key === 'Enter' && handleSend()}
          placeholder="輸入討論內容..." 
          className="flex-1 bg-[#FDFBF7] border border-[#D5CFC4] rounded-full px-4 py-2 text-sm focus:outline-none focus:border-[#C2A878]" 
        />
        <button onClick={handleSend} className="bg-[#4A3F35] text-white p-2 rounded-full hover:bg-[#3A3025] transition-colors">
          <Send size={18} className="-ml-0.5 mt-0.5" />
        </button>
      </div>
    </div>
  );
}

export function CourseMaterialsStudentView({ subjectId, user }: { subjectId: string, user: UserProfile }) {
  const [materials, setMaterials] = useState<CourseMaterial[]>([]);
  const [activeMat, setActiveMat] = useState<CourseMaterial | null>(null);

  useEffect(() => {
    const fetchMats = async () => {
      const q = query(collection(db, 'materials'), where('subjectId', '==', subjectId), orderBy('createdAt', 'desc'));
      const snap = await getDocs(q);
      setMaterials(snap.docs.map(d => ({ id: d.id, ...d.data() } as CourseMaterial)));
    };
    fetchMats();
  }, [subjectId]);

  return (
    <div className="flex flex-col lg:flex-row gap-6">
      <div className="lg:w-2/3 space-y-6">
        {activeMat ? (
          <div className="bg-white rounded-3xl overflow-hidden shadow-md border border-[#EAE6DF]">
            <div className="aspect-video bg-black flex items-center justify-center relative">
               {activeMat.type === 'video' ? (
                 activeMat.contentUrl.includes('youtube.com') || activeMat.contentUrl.includes('youtu.be') ? (
                   <iframe src={activeMat.contentUrl.replace('watch?v=', 'embed/').replace('youtu.be/', 'youtube.com/embed/')} className="w-full h-full border-0" allowFullScreen></iframe>
                 ) : (
                   <video src={activeMat.contentUrl} controls className="w-full h-full object-contain"></video>
                 )
               ) : (
                 <div className="text-white text-center p-10 flex flex-col items-center">
                    {activeMat.type === 'pdf' ? <FileText size={64} className="mb-4 text-[#C2A878]" /> : <BookOpen size={64} className="mb-4 text-[#C2A878]" />}
                    <h3 className="text-2xl font-bold mb-4">{activeMat.title}</h3>
                    <a href={activeMat.contentUrl} target="_blank" rel="noreferrer" className="bg-[#C2A878] text-[#4A3F35] px-6 py-2 rounded-full font-bold">點此開啟內容</a>
                 </div>
               )}
            </div>
            <div className="p-6">
              <div className="flex items-center gap-2 text-sm text-[#C2A878] font-bold mb-2">
                單元 {activeMat.unit}
              </div>
              <h2 className="text-2xl font-bold text-[#4A3F35] mb-4">{activeMat.title}</h2>
              <p className="text-[#8C7A6B] leading-relaxed">{activeMat.description}</p>
            </div>
          </div>
        ) : (
          <div className="bg-[#FDFBF7] border border-[#EAE6DF] rounded-3xl p-12 text-center h-full flex flex-col items-center justify-center">
             <Video size={64} className="text-[#D5CFC4] mb-4" />
             <h3 className="text-xl font-bold text-[#8C7A6B]">請從右側選擇教材開始學習</h3>
          </div>
        )}
        
        {activeMat && (
          <DiscussionBoard targetId={`mat_${activeMat.id}`} user={user} />
        )}
      </div>

      <div className="lg:w-1/3 space-y-4">
        <h3 className="font-serif text-xl font-bold text-[#4A3F35] mb-4 flex items-center gap-2">
          <BookOpen size={24} className="text-[#C2A878]"/>
          課程內容清單
        </h3>
        <div className="space-y-3 max-h-[600px] overflow-y-auto pr-2">
          {materials.map(m => (
            <div 
              key={m.id} 
              onClick={() => setActiveMat(m)}
              className={`p-4 rounded-2xl cursor-pointer transition-all border ${activeMat?.id === m.id ? 'bg-[#EAE2D3] border-[#C2A878] shadow-sm' : 'bg-white border-[#EAE6DF] hover:border-[#C2A878]'}`}
            >
              <div className="flex gap-3">
                <div className={`p-2 rounded-lg h-fit ${activeMat?.id === m.id ? 'bg-[#C2A878] text-white' : 'bg-[#FDFBF7] text-[#A69B8F]'}`}>
                  {m.type === 'video' ? <Play size={16} className="ml-0.5"/> : m.type === 'pdf' ? <FileText size={16} /> : <BookOpen size={16} />}
                </div>
                <div>
                  <h4 className={`font-bold ${activeMat?.id === m.id ? 'text-[#4A3F35]' : 'text-[#5A4F45]'}`}>{m.title}</h4>
                  <p className="text-xs text-[#8C7A6B] mt-1 line-clamp-1">{m.description}</p>
                </div>
              </div>
            </div>
          ))}
          {materials.length === 0 && <p className="text-[#A69B8F]">目前沒有可用的教材。</p>}
        </div>
      </div>
    </div>
  );
}

export function GamificationProfile({ user }: { user: UserProfile }) {
  const xp = user.points || 0;
  const level = Math.floor(Math.sqrt(xp / 100)) + 1;
  const currentLevelXp = Math.pow(level - 1, 2) * 100;
  const nextLevelXp = Math.pow(level, 2) * 100;
  const progress = ((xp - currentLevelXp) / (nextLevelXp - currentLevelXp)) * 100;

  return (
    <div className="bg-white rounded-3xl border border-[#EAE6DF] p-6 shadow-sm flex flex-col md:flex-row items-center gap-6">
      <div className="relative w-24 h-24 rounded-full bg-[#EAE2D3] flex items-center justify-center border-4 border-[#C2A878]">
        {user.photoURL ? (
          <img src={user.photoURL} alt={user.displayName} className="w-full h-full rounded-full object-cover" />
        ) : (
          <User size={40} className="text-[#B39969]" />
        )}
        <div className="absolute -bottom-2 bg-[#4A3F35] text-white text-xs font-bold px-3 py-1 rounded-full border-2 border-white">
          Lv. {level}
        </div>
      </div>
      <div className="flex-1 w-full space-y-2">
        <div className="flex justify-between items-end">
          <h2 className="text-2xl font-bold text-[#4A3F35] font-serif">{user.displayName}</h2>
          <span className="text-sm font-bold text-[#8C7A6B]">{xp} XP</span>
        </div>
        <div className="w-full bg-[#FDFBF7] h-3 rounded-full overflow-hidden border border-[#EAE6DF]">
          <div className="bg-gradient-to-r from-[#C2A878] to-[#B39969] h-full rounded-full transition-all duration-1000" style={{ width: `${Math.max(5, progress)}%` }}></div>
        </div>
        <p className="text-xs text-right text-[#A69B8F]">距離升級還需 {nextLevelXp - xp} XP</p>
      </div>
      <div className="w-full md:w-auto flex gap-2 justify-start md:justify-end border-t md:border-t-0 md:border-l border-[#EAE6DF] pt-4 md:pt-0 md:pl-6">
        {user.badges && user.badges.length > 0 ? (
          user.badges.slice(0,3).map((b, i) => (
             <div key={i} className="flex flex-col items-center gap-1 group relative">
               <div className="bg-gradient-to-br from-[#FDFBF7] to-[#EAE2D3] border border-[#C2A878] p-2 rounded-full shadow-sm text-[#C2A878]">
                 <Award size={24} />
               </div>
               <span className="text-[10px] text-[#8C7A6B] font-bold">{b}</span>
             </div>
          ))
        ) : (
          <div className="text-sm text-[#A69B8F] text-center w-full">完成任務解鎖徽章</div>
        )}
      </div>
    </div>
  );
}

""");
