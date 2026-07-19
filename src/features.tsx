import { createPortal } from 'react-dom';
import React, { useState, useEffect, useRef } from 'react';
import { collection, query, where, getDocs, addDoc, deleteDoc, doc, updateDoc, orderBy, limit, onSnapshot } from 'firebase/firestore';
import { db, auth, storage } from './firebase';
import { ref, uploadBytes, getDownloadURL, uploadBytesResumable, UploadTask } from 'firebase/storage';
import Markdown from 'react-markdown';
import type { UserProfile, Subject } from './App';
import { useNavigate, useParams, Link } from 'react-router-dom';
import { ChevronLeft, BookOpen, Video, FileText, MessageCircle, Send, Award, Trash, Star, Play, CheckCircle, ChevronRight, Layout, Info, User, Volume2, VolumeX, Calendar, Paperclip, Download, Plus, X, Upload, ShoppingCart, Trophy, Lock, Unlock , Edit2} from 'lucide-react';
import { toast } from './toast';
import { googleSignIn, getAccessToken } from './auth';
import { confirmModal } from './confirm';

export interface Announcement {
  id?: string;
  title: string;
  content: string;
  author: string;
  createdAt: number;
}

export interface MaterialProgress {
  id?: string;
  userId: string;
  materialId: string;
  subjectId: string;
  completed: boolean;
  timeSpent: number;
  notes: string;
  highlights: string[];
  lastUpdated: number;
}

export interface CourseMaterial {
  id?: string;
  subjectId: string;
  unit: number;
  type: 'video' | 'pdf' | 'article' | 'lesson';
  title: string;
  contentUrl: string;
  description: string;
  markdownNotes?: string;
  attachments?: { name: string; url: string }[];
  createdAt: number;
  requiredMaterialIds?: string[];
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
  pet: 'PET 英文'
};

export function LandingPage() {
  const navigate = useNavigate();
  const [announcements, setAnnouncements] = useState<Announcement[]>([]);

  useEffect(() => {
    const q = query(collection(db, 'announcements'));
    const unsub = onSnapshot(q, (snap) => {
      const data = snap.docs.map(d => ({ id: d.id, ...d.data() } as Announcement));
      data.sort((a, b) => (b.createdAt || 0) - (a.createdAt || 0));
      setAnnouncements(data.slice(0, 5));
    }, (err) => console.warn("Snapshot error:", err));
    return unsub;
  }, []);

  return (
    <div className="w-full bg-white font-sans text-gray-900">
      {/* Navigation Bar */}
      <nav className="border-b border-gray-100 bg-white/80 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-tr from-indigo-600 to-blue-500 rounded-xl flex items-center justify-center text-white shadow-lg">
              <span className="font-bold text-xl">D</span>
            </div>
            <span className="font-bold text-xl tracking-tight text-gray-900">DevSeed</span>
          </div>
          <div className="flex items-center gap-4">
            <button onClick={() => navigate('/signin')} className="text-gray-600 hover:text-gray-900 font-semibold px-4 py-2 transition-colors">
              登入
            </button>
            <button onClick={() => navigate('/signin')} className="bg-gray-900 hover:bg-gray-800 text-white px-6 py-2.5 rounded-full font-semibold transition-all shadow-md hover:shadow-lg">
              免費註冊
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative overflow-hidden pt-20 pb-32 lg:pt-32 lg:pb-40">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-indigo-50 via-white to-white -z-10"></div>
        <div className="max-w-7xl mx-auto px-6 flex flex-col lg:flex-row items-center justify-between gap-16">
          <div className="lg:w-1/2 space-y-10 text-center lg:text-left relative z-10">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-indigo-50 border border-indigo-100 text-indigo-700 text-sm font-semibold">
              <span className="w-2 h-2 rounded-full bg-indigo-600 animate-pulse"></span>
              企業級數位學習平台
            </div>
            <h1 className="text-5xl lg:text-7xl font-black tracking-tight leading-[1.1] text-gray-900">
              驅動未來的 <br/>
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-blue-500">智能學習體驗</span>
            </h1>
            <p className="text-lg text-gray-600 max-w-xl mx-auto lg:mx-0 leading-relaxed">
              DevSeed 提供全方位的數位教育解決方案。結合互動式多媒體教材、即時測驗與成效分析，助您釋放最大學習潛能。
            </p>
            <div className="flex flex-col sm:flex-row items-center gap-4 justify-center lg:justify-start">
              <button onClick={() => navigate('/signin')} className="w-full sm:w-auto bg-indigo-600 text-white px-8 py-4 rounded-full font-bold text-lg hover:bg-indigo-700 transition-all shadow-[0_8px_30px_rgb(79,70,229,0.3)] hover:shadow-[0_8px_30px_rgb(79,70,229,0.5)] transform hover:-translate-y-1">
                立即開始使用
              </button>
            </div>
          </div>
          <div className="lg:w-1/2 relative w-full">
            <div className="relative rounded-2xl overflow-hidden shadow-[0_20px_50px_rgba(0,0,0,0.1)] border border-gray-100 bg-white p-2 transform rotate-1 hover:rotate-0 transition-transform duration-500">
              <img src="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=1200&q=80" alt="Platform Preview" className="w-full h-auto rounded-xl object-cover aspect-[4/3]" />
            </div>
            <div className="absolute -bottom-10 -left-10 w-40 h-40 bg-blue-400/20 rounded-full blur-3xl"></div>
            <div className="absolute -top-10 -right-10 w-40 h-40 bg-indigo-400/20 rounded-full blur-3xl"></div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-32 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="text-center max-w-3xl mx-auto mb-20">
            <h2 className="text-4xl font-black text-gray-900 mb-6 tracking-tight">打造完美學習閉環</h2>
            <p className="text-lg text-gray-600">從知識輸入到實戰輸出，我們為您設計了最科學的學習軌跡。</p>
          </div>
          <div className="grid md:grid-cols-3 gap-10">
            <div className="p-8 rounded-3xl bg-white border border-gray-100 shadow-sm hover:shadow-xl transition-shadow duration-300">
              <div className="w-14 h-14 bg-blue-50 rounded-2xl flex items-center justify-center text-blue-600 mb-8">
                <Video size={28} strokeWidth={2} />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">沉浸式教材</h3>
              <p className="text-gray-600 leading-relaxed">
                支援高畫質影音、豐富圖文與 Markdown 語法，讓知識不再生硬。
              </p>
            </div>
            <div className="p-8 rounded-3xl bg-white border border-gray-100 shadow-sm hover:shadow-xl transition-shadow duration-300">
              <div className="w-14 h-14 bg-indigo-50 rounded-2xl flex items-center justify-center text-indigo-600 mb-8">
                <MessageCircle size={28} strokeWidth={2} />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">即時共學社群</h3>
              <p className="text-gray-600 leading-relaxed">
                內建討論看板，學習不再孤單。師生零時差解惑，加速知識吸收。
              </p>
            </div>
            <div className="p-8 rounded-3xl bg-white border border-gray-100 shadow-sm hover:shadow-xl transition-shadow duration-300">
              <div className="w-14 h-14 bg-purple-50 rounded-2xl flex items-center justify-center text-purple-600 mb-8">
                <Award size={28} strokeWidth={2} />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">遊戲化驅動</h3>
              <p className="text-gray-600 leading-relaxed">
                結合經驗值、排行榜與徽章系統，激發內在動機，讓進步看得見。
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Announcements Section */}
      <section className="py-24 bg-gray-50 border-t border-gray-100">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-16">
            <div className="max-w-2xl">
              <h2 className="text-3xl font-black text-gray-900 mb-4">系統公告與動態</h2>
              <p className="text-gray-600">隨時掌握平台最新更新與重要訊息。</p>
            </div>
          </div>
          
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {announcements.length > 0 ? (
              announcements.map((a) => (
                <div key={a.id} className="bg-white rounded-2xl p-8 shadow-sm border border-gray-100 hover:shadow-md transition-shadow group flex flex-col h-full">
                  <div className="flex-grow">
                    <div className="flex items-center gap-3 mb-5">
                      <span className="px-3 py-1 bg-indigo-50 text-indigo-700 text-xs font-bold rounded-full">動態</span>
                      <span className="text-sm text-gray-400 font-medium">{new Date(a.createdAt).toLocaleDateString()}</span>
                    </div>
                    <h3 className="font-bold text-xl text-gray-900 mb-3 group-hover:text-indigo-600 transition-colors">{a.title}</h3>
                    <p className="text-gray-600 text-sm leading-relaxed line-clamp-3">{a.content}</p>
                  </div>
                  <div className="mt-6 pt-4 border-t border-gray-50 flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-gray-600 font-bold text-xs">
                      {a.author?.[0] || '管'}
                    </div>
                    <span className="text-sm font-semibold text-gray-700">{a.author || '系統管理員'}</span>
                  </div>
                </div>
              ))
            ) : (
              <div className="col-span-full py-20 text-center bg-white rounded-2xl border border-gray-100 shadow-sm">
                <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gray-50 text-gray-400 mb-4">
                  <Info size={24} />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">目前沒有最新動態</h3>
                <p className="text-gray-500">系統運作一切正常，請安心使用。</p>
              </div>
            )}
          </div>
        </div>
      </section>
      
      {/* CTA Section */}
      <section className="py-32 px-6">
        <div className="max-w-5xl mx-auto bg-gray-900 rounded-[2.5rem] p-12 lg:p-24 text-center relative overflow-hidden shadow-2xl">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-indigo-900/40 via-transparent to-transparent"></div>
          
          <div className="relative z-10 max-w-2xl mx-auto">
            <h2 className="text-4xl lg:text-5xl font-black text-white mb-6 tracking-tight">準備好提升學習效率了嗎？</h2>
            <p className="text-gray-300 text-lg mb-10 leading-relaxed">加入 DevSeed，立即體驗無縫銜接的數位學習環境。只需一分鐘即可完成註冊。</p>
            <button onClick={() => navigate('/signin')} className="bg-white text-gray-900 px-10 py-4 rounded-full font-bold text-lg hover:bg-gray-50 transition-all transform hover:-translate-y-1 shadow-xl inline-flex items-center justify-center gap-3">
              免費建立帳號 <ChevronRight size={20} />
            </button>
          </div>
        </div>
      </section>
      
      {/* Footer */}
      <footer className="bg-white border-t border-gray-100 py-12">
        <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gray-900 rounded-lg flex items-center justify-center text-white">
              <span className="font-bold text-sm">D</span>
            </div>
            <span className="font-bold text-gray-900">DevSeed</span>
          </div>
          <p className="text-gray-500 text-sm">© {new Date().getFullYear()} DevSeed. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

export function AnnouncementsAdminTab() {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [announcements, setAnnouncements] = useState<Announcement[]>([]);

  const fetchAnnouncements = async () => {
    const q = query(collection(db, 'announcements'));
    const snap = await getDocs(q);
    const data = snap.docs.map(d => ({ id: d.id, ...d.data() } as Announcement));
    data.sort((a, b) => (b.createdAt || 0) - (a.createdAt || 0));
    setAnnouncements(data);
  };

  useEffect(() => { fetchAnnouncements(); }, []);

  const handlePost = async () => {
    if (!title || !content) return;
    try {
      await addDoc(collection(db, 'announcements'), {
        title, content, author: '系統管理員', createdAt: Date.now()
      });
      setTitle(''); setContent(''); fetchAnnouncements();
    } catch (e) {
      console.error(e);
    }
  };

  const handleDelete = async (id: string) => {
    await deleteDoc(doc(db, 'announcements', id));
    fetchAnnouncements();
  };

  return (
    <div className="bg-white p-6 rounded-3xl shadow-sm border border-gray-100 mb-8">
      <h2 className="font-bold text-2xl mb-6 text-gray-900">發布系統公告</h2>
      <div className="space-y-4 mb-8">
        <input placeholder="公告標題" value={title} onChange={e => setTitle(e.target.value)} className="w-full border border-gray-200 rounded-xl p-3" />
        <textarea placeholder="公告內容..." value={content} onChange={e => setContent(e.target.value)} className="w-full border border-gray-200 rounded-xl p-3 h-32" />
        <button onClick={handlePost} className="bg-indigo-600 text-white px-6 py-2 rounded-xl font-bold hover:bg-indigo-700">發布公告</button>
      </div>
      <h3 className="font-bold text-lg mb-4 text-gray-900">歷史公告</h3>
      <div className="space-y-4">
        {announcements.map(a => (
          <div key={a.id} className="p-4 border border-gray-100 rounded-xl flex justify-between">
            <div>
              <h4 className="font-bold text-gray-900">{a.title}</h4>
              <p className="text-gray-600 text-sm mt-1">{a.content}</p>
              <p className="text-gray-400 text-xs mt-2">{new Date(a.createdAt).toLocaleString()}</p>
            </div>
            <button onClick={() => handleDelete(a.id!)} className="text-red-500 hover:bg-red-50 p-2 rounded-lg"><Trash size={16}/></button>
          </div>
        ))}
      </div>
    </div>
  );
}

export function CourseMaterialsAdminTab({ subjectId }: { subjectId: string }) {
  const [materials, setMaterials] = useState<CourseMaterial[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [newMat, setNewMat] = useState<Partial<CourseMaterial>>({ type: 'lesson', unit: 1, title: '', contentUrl: '', description: '', markdownNotes: '', attachments: [] });

  const fetchMaterials = async () => {
    const q = query(collection(db, 'materials'), where('subjectId', '==', subjectId));
    const snap = await getDocs(q);
    const data = snap.docs.map(d => ({ id: d.id, ...d.data() } as CourseMaterial));
    data.sort((a, b) => a.unit - b.unit);
    setMaterials(data);
  };

  useEffect(() => { fetchMaterials(); }, [subjectId]);

  const handleEdit = (m: CourseMaterial) => {
    setNewMat(m);
    setEditingId(m.id || null);
    setShowForm(true);
  };

  const handleSave = async () => {
    if (!newMat.title) return;
    try {
      const mat = { ...newMat, subjectId, createdAt: newMat.createdAt || Date.now() };
      if (editingId) {
        await updateDoc(doc(db, 'materials', editingId), mat);
      } else {
        await addDoc(collection(db, 'materials'), mat);
      }
      setShowForm(false);
      setEditingId(null);
      setNewMat({ type: 'lesson', unit: 1, title: '', contentUrl: '', description: '', markdownNotes: '', attachments: [] });
      fetchMaterials();
    } catch (e) {
      console.error(e);
    }
  };

  const handleDelete = async (id: string) => {
    await deleteDoc(doc(db, 'materials', id));
    fetchMaterials();
  };

  const groupedMaterials = materials.reduce((acc, curr) => {
    const unit = curr.unit || 1;
    if (!acc[unit]) acc[unit] = [];
    acc[unit].push(curr);
    return acc;
  }, {} as Record<number, CourseMaterial[]>);

  return (
    <div className="bg-white p-6 rounded-3xl shadow-sm border border-gray-100">
      <div className="flex justify-between items-center mb-6">
        <h2 className="font-bold text-2xl text-gray-900">課程教材管理</h2>
        <button onClick={() => {
          if (showForm) {
            setShowForm(false);
            setEditingId(null);
            setNewMat({ type: 'lesson', unit: 1, title: '', contentUrl: '', description: '', markdownNotes: '', attachments: [] });
          } else {
            setShowForm(true);
          }
        }} className="bg-indigo-600 text-white px-4 py-2 rounded-xl hover:bg-indigo-700 flex items-center gap-2">
          {showForm ? '取消' : <><Upload size={18}/> 新增教材</>}
        </button>
      </div>

      {showForm && (
        <div className="mb-8 p-6 bg-gray-50 rounded-2xl border border-gray-200 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-12 gap-4">
            <div className="md:col-span-3">
              <label className="text-sm font-bold text-gray-700">類型</label>
              <select value={newMat.type} onChange={e => setNewMat({...newMat, type: e.target.value as any})} className="w-full border border-gray-200 rounded-xl p-3 bg-white mt-1 focus:outline-none focus:ring-2 focus:ring-indigo-500">
                <option value="lesson">課程講義</option>
                <option value="exam">考卷</option>
                <option value="solution">考卷解答</option>
                <option value="video">影音</option>
              </select>
            </div>
            <div className="md:col-span-2">
              <label className="text-sm font-bold text-gray-700">單元</label>
              <input type="number" value={newMat.unit} onChange={e => setNewMat({...newMat, unit: Number(e.target.value)})} className="w-full border border-gray-200 rounded-xl p-3 mt-1 bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"/>
            </div>
            <div className="md:col-span-7">
              <label className="text-sm font-bold text-gray-700">標題</label>
              <input value={newMat.title} onChange={e => setNewMat({...newMat, title: e.target.value})} className="w-full border border-gray-200 rounded-xl p-3 mt-1 bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="例如：第一單元 基礎觀念"/>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-12 gap-4">
            <div className="md:col-span-8">
              <label className="text-sm font-bold text-gray-700">內容連結 (影片URL或檔案連結)</label>
              <input value={newMat.contentUrl} onChange={e => setNewMat({...newMat, contentUrl: e.target.value})} className="w-full border border-gray-200 rounded-xl p-3 mt-1 bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="https://youtube.com/..."/>
            </div>
            <div className="md:col-span-4">
              <label className="text-sm font-bold text-gray-700">簡短說明</label>
              <input value={newMat.description || ''} onChange={e => setNewMat({...newMat, description: e.target.value})} className="w-full border border-gray-200 rounded-xl p-3 mt-1 bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="選填：章節摘要..."/>
            </div>
          </div>

          <div>
            <label className="text-sm font-bold text-gray-700">補充檔案連結</label>
            <div className="mt-2 space-y-2">
              {newMat.attachments?.map((att, i) => (
                <div key={i} className="flex gap-2">
                  <input value={att.name} onChange={e => {
                    const newAtts = [...(newMat.attachments || [])];
                    newAtts[i].name = e.target.value;
                    setNewMat({...newMat, attachments: newAtts});
                  }} className="border border-gray-200 rounded-xl p-3 w-1/3 bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="檔案名稱" />
                  <input value={att.url} onChange={e => {
                    const newAtts = [...(newMat.attachments || [])];
                    newAtts[i].url = e.target.value;
                    setNewMat({...newMat, attachments: newAtts});
                  }} className="border border-gray-200 rounded-xl p-3 flex-grow bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="https://..." />
                  <button onClick={() => {
                    const newAtts = [...(newMat.attachments || [])];
                    newAtts.splice(i, 1);
                    setNewMat({...newMat, attachments: newAtts});
                  }} className="text-red-500 hover:bg-red-50 p-3 rounded-xl transition-colors"><Trash size={18}/></button>
                </div>
              ))}
            </div>
            <button onClick={() => {
              setNewMat({...newMat, attachments: [...(newMat.attachments || []), {name: '', url: ''}]});
            }} className="text-sm text-indigo-600 font-bold mt-2 hover:text-indigo-800 flex items-center gap-1">
              <Plus size={16}/> 新增補充檔案
            </button>
          </div>
          <div>
            <label className="text-sm font-bold text-gray-700">Markdown 課程筆記</label>
            <textarea value={newMat.markdownNotes} onChange={e => setNewMat({...newMat, markdownNotes: e.target.value})} className="w-full border border-gray-200 rounded-xl p-3 h-32 mt-1 bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="支援 Markdown 語法..."/>
          </div>
          <button onClick={handleSave} className="bg-indigo-600 text-white px-6 py-2.5 rounded-xl font-bold w-full hover:bg-indigo-700 transition-colors shadow-md mt-2">{editingId ? '更新教材' : '儲存教材'}</button>
        </div>
      )}

      <div className="space-y-4">
        
        {Object.entries(groupedMaterials).map(([unit, mats]) => (
          <div key={unit} className="mb-8">
            <h3 className="text-xl font-bold text-gray-900 mb-4 border-b pb-2">Unit {unit}</h3>
            <div className="space-y-3">
              {mats.map(m => (
                <div key={m.id} className="flex justify-between items-center p-4 border border-gray-100 rounded-xl hover:bg-gray-50 transition-colors">
                  <div className="flex items-center gap-4">
                    <div className="w-10 h-10 bg-indigo-100 text-indigo-600 rounded-lg flex items-center justify-center font-bold">{m.unit}</div>
                    <div>
                      <h4 className="font-bold text-gray-900">{m.title}</h4>
                      <span className="text-xs text-gray-500 uppercase tracking-wide">{m.type}</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <button onClick={() => handleEdit(m)} className="text-indigo-500 hover:bg-indigo-50 p-2 rounded-lg"><Edit2 size={18}/></button>
                    <button onClick={() => handleDelete(m.id!)} className="text-red-500 hover:bg-red-50 p-2 rounded-lg"><Trash size={18}/></button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}

      </div>
    </div>
  );
}

export function DiscussionBoard({ subjectId, user }: { subjectId: string, user: UserProfile }) {
  const [posts, setPosts] = useState<DiscussionPost[]>([]);
  const [newPost, setNewPost] = useState('');

  useEffect(() => {
    const q = query(collection(db, 'discussions'), where('subjectId', '==', subjectId), orderBy('createdAt', 'desc'));
    const unsub = onSnapshot(q, snap => {
      setPosts(snap.docs.map(d => ({ id: d.id, ...d.data() } as DiscussionPost)));
    });
    return unsub;
  }, [subjectId]);

  const handleSubmit = async () => {
    if (!newPost.trim()) return;
    try {
      await addDoc(collection(db, 'discussions'), {
        subjectId, authorId: user.uid, authorName: user.displayName, content: newPost, createdAt: Date.now(), replies: []
      });
      setNewPost('');
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="bg-white p-6 md:p-10 rounded-[2rem] shadow-sm border border-gray-100">
      <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-3"><MessageCircle className="text-indigo-500"/> 科目討論版</h2>
      <div className="mb-8 flex gap-3">
        <div className="w-10 h-10 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-700 font-bold shrink-0">{user.displayName[0]}</div>
        <div className="flex-grow">
          <textarea value={newPost} onChange={e => setNewPost(e.target.value)} placeholder="有什麼問題想討論嗎？" className="w-full border border-gray-200 rounded-xl p-4 min-h-[100px] focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all"/>
          <div className="flex justify-end mt-3">
            <button onClick={handleSubmit} className="bg-indigo-600 text-white px-6 py-2 rounded-full font-bold hover:bg-indigo-700 transition-colors shadow-md flex items-center gap-2"><Send size={16}/> 發布</button>
          </div>
        </div>
      </div>
      <div className="space-y-6">
        {posts.map(post => (
          <div key={post.id} className="border border-gray-100 rounded-2xl p-6 bg-gray-50/50">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-8 h-8 bg-white border border-gray-200 rounded-full flex items-center justify-center text-gray-700 font-bold text-sm">{post.authorName[0]}</div>
              <div>
                <span className="font-bold text-gray-900 text-sm block">{post.authorName}</span>
                <span className="text-xs text-gray-500">{new Date(post.createdAt).toLocaleString()}</span>
              </div>
            </div>
            <p className="text-gray-800 leading-relaxed whitespace-pre-wrap pl-11">{post.content}</p>
          </div>
        ))}
        {posts.length === 0 && <p className="text-center text-gray-500 py-10">目前還沒有討論，來做第一個發問的人吧！</p>}
      </div>
    </div>
  );
}

export function CourseMaterialsStudentView({ subjectId, user }: { subjectId: string, user: UserProfile }) {
  const [materials, setMaterials] = useState<CourseMaterial[]>([]);
  const [activeMat, setActiveMat] = useState<CourseMaterial | null>(null);
  const [isPlayingTTS, setIsPlayingTTS] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);

  useEffect(() => {
    const q = query(collection(db, 'materials'), where('subjectId', '==', subjectId));
    const unsub = onSnapshot(q, snap => {
      const data = snap.docs.map(d => ({ id: d.id, ...d.data() } as CourseMaterial));
      data.sort((a, b) => a.unit - b.unit);
      setMaterials(data);
      if (data.length > 0 && !activeMat) setActiveMat(data[0]);
    });
    return unsub;
  }, [subjectId]);

  const toggleTTS = () => {
    if (isPlayingTTS) {
      window.speechSynthesis.cancel();
      setIsPlayingTTS(false);
    } else if (activeMat?.markdownNotes) {
      const textToRead = activeMat.markdownNotes.replace(/<[^>]*>?/gm, '').replace(/[#*_]/g, '');
      const utterance = new SpeechSynthesisUtterance(textToRead);
      utterance.lang = 'zh-TW';
      utterance.onend = () => setIsPlayingTTS(false);
      window.speechSynthesis.speak(utterance);
      setIsPlayingTTS(true);
    }
  };

  const getAbsoluteUrl = (url: string) => {
    if (!url) return '';
    let cleanUrl = url.trim();
    if (!/^https?:\/\//i.test(cleanUrl)) {
      cleanUrl = 'https://' + cleanUrl;
    }
    return cleanUrl;
  };

  const getYoutubeEmbedUrl = (url: string) => {
    try {
      const absoluteUrl = getAbsoluteUrl(url);
      const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=|shorts\/)([^#\&\?]*).*/;
      const match = absoluteUrl.match(regExp);
      if (match && match[2].length === 11) {
        return `https://www.youtube.com/embed/${match[2]}`;
      }
      return absoluteUrl;
    } catch (e) {
      // Ignore
    }
    return url;
  };


  const groupedMaterials = materials.reduce((acc, curr) => {
    const unit = curr.unit || 1;
    if (!acc[unit]) acc[unit] = [];
    acc[unit].push(curr);
    return acc;
  }, {} as Record<number, CourseMaterial[]>);

  if (isFullscreen && activeMat) {
    return createPortal(
      <div className="fixed inset-0 z-[100] bg-white overflow-y-auto">
        <div className="max-w-5xl mx-auto px-6 py-10 relative">
          <button onClick={() => setIsFullscreen(false)} className="absolute top-6 right-6 lg:-right-16 text-gray-400 hover:text-gray-900 bg-gray-100 hover:bg-gray-200 p-3 rounded-full transition-all">
            <X size={24}/>
          </button>
          
          <h2 className="text-4xl font-black text-gray-900 mb-2">{activeMat.title}</h2>
          {activeMat.description && <p className="text-gray-500 mb-8 text-lg">{activeMat.description}</p>}

          {(activeMat.type === 'video' || activeMat.contentUrl) && (
            <div className="aspect-video bg-black rounded-3xl overflow-hidden mb-12 shadow-2xl">
              {(() => {
                const absUrl = getAbsoluteUrl(activeMat.contentUrl || '');
                if (absUrl.includes('youtube.com') || absUrl.includes('youtu.be') || absUrl.includes('youtube-nocookie.com')) {
                  return <iframe src={getYoutubeEmbedUrl(activeMat.contentUrl || '')} className="w-full h-full border-0" allowFullScreen></iframe>;
                } else if (absUrl) {
                  return <video src={absUrl} controls className="w-full h-full"></video>;
                }
                return null;
              })()}
            </div>
          )}

          {activeMat.markdownNotes && (
            <div className="relative mt-8">
              <button onClick={toggleTTS} className="absolute -top-16 right-0 bg-indigo-50 text-indigo-600 px-5 py-2.5 rounded-full font-bold flex items-center gap-2 hover:bg-indigo-100 transition-colors shadow-sm">
                {isPlayingTTS ? <><VolumeX size={18}/> 停止朗讀</> : <><Volume2 size={18}/> 語音朗讀</>}
              </button>
              <div className="prose prose-lg prose-indigo max-w-none prose-headings:text-gray-900 prose-p:text-gray-700">
                <Markdown>{activeMat.markdownNotes}</Markdown>
              </div>
            </div>
          )}

          {activeMat.attachments && activeMat.attachments.length > 0 && (
            <div className="mt-16 pt-10 border-t border-gray-100">
              <h3 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2"><Paperclip size={20}/> 補充檔案</h3>
              <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-4">
                {activeMat.attachments.map((att, i) => (
                  <a key={i} href={att.url} target="_blank" rel="noopener noreferrer" className="flex items-center gap-3 p-4 border border-gray-200 rounded-2xl hover:border-indigo-300 hover:shadow-md transition-all group">
                    <div className="w-10 h-10 bg-indigo-50 rounded-xl flex items-center justify-center text-indigo-600 group-hover:scale-110 transition-transform">
                      <FileText size={20}/>
                    </div>
                    <span className="font-semibold text-gray-700 truncate">{att.name}</span>
                  </a>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>,
      document.body
    );
  }

  return (
    <div className="flex flex-col lg:flex-row gap-8 min-h-[70vh]">
      <div className="lg:w-1/3 space-y-4">
        <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-3"><BookOpen className="text-indigo-500"/> 課程章節</h2>
        
        {Object.entries(groupedMaterials).map(([unit, mats]) => (
          <div key={unit} className="mb-6">
            <h3 className="text-lg font-bold text-gray-900 mb-3 border-b pb-2">Unit {unit}</h3>
            <div className="space-y-3">
              {mats.map(m => (
                <button key={m.id} onClick={() => { setActiveMat(m); window.speechSynthesis.cancel(); setIsPlayingTTS(false); }} className={`w-full text-left p-4 rounded-xl border transition-all ${activeMat?.id === m.id ? 'bg-indigo-600 border-indigo-600 text-white shadow-lg transform scale-[1.02]' : 'bg-white border-gray-100 text-gray-700 hover:border-indigo-200 hover:shadow-md'}`}>
                  <div className="flex items-center gap-4">
                    <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold shrink-0 ${activeMat?.id === m.id ? 'bg-white/20 text-white' : 'bg-indigo-50 text-indigo-600'}`}>
                      {m.unit}
                    </div>
                    <div>
                      <div className="font-bold line-clamp-1 text-sm">{m.title}</div>
                      <div className={`text-xs mt-1 uppercase tracking-wider ${activeMat?.id === m.id ? 'text-indigo-100' : 'text-gray-400'}`}>{m.type}</div>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>
        ))}

      </div>
      <div className="lg:w-2/3">
        {activeMat ? (
          <div className="bg-white rounded-[2rem] p-6 md:p-10 shadow-sm border border-gray-100 relative">
            <button onClick={() => setIsFullscreen(true)} className="absolute top-6 right-6 text-gray-400 hover:text-indigo-600 bg-gray-50 hover:bg-indigo-50 p-3 rounded-full transition-all" title="全螢幕無擾模式">
              <Layout size={20}/>
            </button>
            <h2 className="text-3xl font-bold text-gray-900 mb-2 pr-16">{activeMat.title}</h2>
            {activeMat.description && <p className="text-gray-500 mb-8">{activeMat.description}</p>}
            
            {(activeMat.type === 'video' || activeMat.contentUrl) && (
              <div className="aspect-video bg-black rounded-2xl overflow-hidden mb-8 shadow-inner mt-6">
                {(() => {
                  const absUrl = getAbsoluteUrl(activeMat.contentUrl || '');
                  if (absUrl.includes('youtube.com') || absUrl.includes('youtu.be') || absUrl.includes('youtube-nocookie.com')) {
                    return <iframe src={getYoutubeEmbedUrl(activeMat.contentUrl || '')} className="w-full h-full border-0" allowFullScreen></iframe>;
                  } else if (absUrl) {
                    return <video src={absUrl} controls className="w-full h-full"></video>;
                  }
                  return null;
                })()}
              </div>
            )}
            {activeMat.markdownNotes && (
              <div className="relative mt-12">
                <button onClick={toggleTTS} className="absolute -top-12 right-0 bg-indigo-50 text-indigo-600 px-4 py-2 rounded-full font-bold flex items-center gap-2 hover:bg-indigo-100 transition-colors">
                  {isPlayingTTS ? <><VolumeX size={18}/> 停止朗讀</> : <><Volume2 size={18}/> 語音朗讀</>}
                </button>
                <div className="prose prose-indigo max-w-none prose-headings:text-gray-900 prose-p:text-gray-700 bg-gray-50/50 p-8 rounded-2xl border border-gray-100">
                  <Markdown>{activeMat.markdownNotes}</Markdown>
                </div>
              </div>
            )}
            
            {activeMat.attachments && activeMat.attachments.length > 0 && (
              <div className="mt-10 pt-8 border-t border-gray-100">
                <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2"><Paperclip size={18}/> 補充檔案</h3>
                <div className="grid sm:grid-cols-2 gap-4">
                  {activeMat.attachments.map((att, i) => (
                    <a key={i} href={att.url} target="_blank" rel="noopener noreferrer" className="flex items-center gap-3 p-3 border border-gray-200 rounded-xl hover:bg-gray-50 hover:border-indigo-200 transition-all">
                      <div className="w-8 h-8 bg-indigo-50 rounded-lg flex items-center justify-center text-indigo-600">
                        <FileText size={16}/>
                      </div>
                      <span className="font-medium text-gray-700 text-sm truncate">{att.name}</span>
                    </a>
                  ))}
                </div>
              </div>
            )}
            
            {!activeMat.contentUrl && !activeMat.markdownNotes && (!activeMat.attachments || activeMat.attachments.length === 0) && (
              <div className="text-center py-20 text-gray-500 bg-gray-50 rounded-2xl border border-gray-100 mt-6">
                本章節暫無詳細內容
              </div>
            )}
          </div>
        ) : (
          <div className="h-full flex items-center justify-center text-gray-400 bg-white rounded-[2rem] border border-gray-100 p-10 text-center">
            <div>
              <BookOpen size={48} className="mx-auto mb-4 opacity-50"/>
              <p className="text-xl font-bold text-gray-500">請從左側選擇課程章節</p>
            </div>
          </div>
        )}
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
               <span className="text-[10px] text-[#8C7A6B] font-bold text-center leading-tight whitespace-pre-wrap w-16">{BADGE_LABELS[b] || b}</span>
             </div>
          ))
        ) : (
          <div className="text-sm text-[#A69B8F] text-center w-full">完成任務解鎖徽章</div>
        )}
      </div>
    </div>
  );
}



// ==========================================
// Leaderboard Component
// ==========================================
export function Leaderboard({ user }: { user: UserProfile }) {
  const [users, setUsers] = useState<UserProfile[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUsers = async () => {
      const q = query(collection(db, 'users'), where('role', '==', 'player'), orderBy('points', 'desc'), limit(50));
      const snap = await getDocs(q);
      const data = snap.docs.map(d => d.data() as UserProfile);
      setUsers(data);
      setLoading(false);
    };
    fetchUsers();
  }, []);

  return (
    <div className="max-w-4xl mx-auto w-full py-8">
      <div className="bg-white rounded-3xl p-8 shadow-xl border-2 border-[#EAE6DF]">
        <div className="flex items-center gap-4 mb-8 pb-6 border-b-2 border-[#F5F5F0]">
          <div className="bg-yellow-100 p-4 rounded-2xl text-yellow-600">
            <Trophy size={32} />
          </div>
          <div>
            <h2 className="text-3xl font-black text-[#4A3F35] font-serif">榮譽排行榜</h2>
            <p className="text-[#8C7A6B] font-medium mt-1">累積 XP 總分排行，展現你的學習成果！</p>
          </div>
        </div>

        {loading ? (
          <div className="text-center py-12 text-[#8C7A6B]">載入中...</div>
        ) : (
          <div className="space-y-4">
            {users.map((u, idx) => (
              <div 
                key={u.uid} 
                className={`flex items-center justify-between p-4 rounded-2xl transition-all
                  ${u.uid === user.uid ? 'bg-yellow-50 border-2 border-yellow-200 shadow-md transform scale-[1.02]' : 'bg-[#FDFBF7] border-2 border-[#EAE6DF] hover:border-[#C2A878]'}
                `}
              >
                <div className="flex items-center gap-4">
                  <div className={`w-10 h-10 flex items-center justify-center font-black text-lg rounded-xl shrink-0
                    ${idx === 0 ? 'bg-yellow-400 text-white shadow-lg shadow-yellow-200' : 
                      idx === 1 ? 'bg-gray-300 text-white' : 
                      idx === 2 ? 'bg-[#CD7F32] text-white' : 'bg-transparent text-[#8C7A6B]'}
                  `}>
                    #{idx + 1}
                  </div>
                  
                  {u.photoURL ? (
                    <img src={u.photoURL} alt="Avatar" className="w-12 h-12 rounded-full border-2 border-white shadow-sm object-cover" />
                  ) : (
                    <div className="w-12 h-12 rounded-full border-2 border-white shadow-sm bg-gradient-to-tr from-indigo-500 to-purple-500 flex items-center justify-center text-white font-bold text-lg">
                      {u.displayName[0]}
                    </div>
                  )}
                  
                  <div>
                    <h3 className="font-bold text-[#4A3F35] text-lg flex items-center gap-2">
                      {u.displayName}
                      {u.uid === user.uid && <span className="text-xs bg-yellow-200 text-yellow-800 px-2 py-0.5 rounded-full">你</span>}
                    </h3>
                    <p className="text-sm text-[#8C7A6B] flex items-center gap-1">
                      連續登入 {u.streak || 0} 天 🔥
                    </p>
                  </div>
                </div>
                
                <div className="text-right">
                  <div className="text-2xl font-black text-[#C2A878] font-mono">
                    {u.points || 0}
                  </div>
                  <div className="text-xs text-[#8C7A6B] font-bold uppercase tracking-wider">
                    XP
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

// ==========================================
// XP Shop Component
// ==========================================
export function XPShop({ user, setUser }: { user: UserProfile, setUser: (u: UserProfile) => void }) {
  const shopItems = [
    { id: 'frame_gold', name: '黃金頭像框', cost: 1000, desc: '尊貴的黃金光澤，象徵你的努力', type: 'frame', color: 'border-yellow-400' },
    { id: 'frame_diamond', name: '鑽石頭像框', cost: 3000, desc: '閃耀的鑽石光芒，頂尖學習者的證明', type: 'frame', color: 'border-cyan-400' },
    { id: 'frame_fire', name: '烈焰頭像框', cost: 5000, desc: '燃燒的學習之火，無人能擋', type: 'frame', color: 'border-red-500' },
    { id: 'theme_dark', name: '深色模式主題', cost: 2000, desc: '護眼的深色主題，適合夜間學習', type: 'theme', color: 'bg-gray-800' },
  ];

  const handlePurchase = async (item: any) => {
    if ((user.points || 0) < item.cost) {
      toast("XP 不足！快去完成任務賺取 XP 吧！");
      return;
    }

    const isFrame = item.type === 'frame';
    const unlockedList = isFrame ? (user.unlockedFrames || ['default']) : (user.unlockedThemes || ['default']);
    
    if (unlockedList.includes(item.id)) {
      // Equip
      const updates = isFrame ? { activeFrame: item.id } : { activeTheme: item.id };
      await updateDoc(doc(db, 'users', user.uid), updates);
      setUser({ ...user, ...updates });
      toast(`已裝備 ${item.name}！`);
    } else {
      // Buy
      const newPoints = (user.points || 0) - item.cost;
      const newUnlocked = [...unlockedList, item.id];
      const updates = isFrame 
        ? { points: newPoints, unlockedFrames: newUnlocked, activeFrame: item.id }
        : { points: newPoints, unlockedThemes: newUnlocked, activeTheme: item.id };
        
      await updateDoc(doc(db, 'users', user.uid), updates);
      setUser({ ...user, ...updates });
      toast(`成功購買並裝備 ${item.name}！`);
    }
  };

  return (
    <div className="max-w-4xl mx-auto w-full py-8">
      <div className="bg-white rounded-3xl p-8 shadow-xl border-2 border-[#EAE6DF]">
        <div className="flex items-center justify-between mb-8 pb-6 border-b-2 border-[#F5F5F0]">
          <div className="flex items-center gap-4">
            <div className="bg-emerald-100 p-4 rounded-2xl text-emerald-600">
              <ShoppingCart size={32} />
            </div>
            <div>
              <h2 className="text-3xl font-black text-[#4A3F35] font-serif">XP 兌換商店</h2>
              <p className="text-[#8C7A6B] font-medium mt-1">使用你的 XP 解鎖專屬外觀與特權！</p>
            </div>
          </div>
          <div className="bg-emerald-50 border-2 border-emerald-200 px-6 py-3 rounded-2xl text-center">
            <div className="text-xs text-emerald-600 font-bold uppercase tracking-wider mb-1">目前餘額</div>
            <div className="text-2xl font-black text-emerald-600 font-mono flex items-center gap-2">
              💎 {user.points || 0}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {shopItems.map(item => {
            const isFrame = item.type === 'frame';
            const isUnlocked = isFrame 
              ? (user.unlockedFrames?.includes(item.id)) 
              : (user.unlockedThemes?.includes(item.id));
            const isEquipped = isFrame 
              ? user.activeFrame === item.id 
              : user.activeTheme === item.id;
              
            return (
              <div key={item.id} className={`p-6 rounded-2xl border-2 transition-all flex flex-col justify-between
                ${isEquipped ? 'border-emerald-400 bg-emerald-50' : 'border-[#EAE6DF] bg-[#FDFBF7] hover:border-[#C2A878]'}
              `}>
                <div>
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-3">
                      {isFrame ? (
                        <div className={`w-12 h-12 rounded-full border-4 ${item.color} bg-white`} />
                      ) : (
                        <div className={`w-12 h-12 rounded-xl ${item.color} border-2 border-gray-300`} />
                      )}
                      <div>
                        <h3 className="font-bold text-lg text-[#4A3F35]">{item.name}</h3>
                        <p className="text-sm text-[#8C7A6B]">{item.type === 'frame' ? '頭像外框' : '介面主題'}</p>
                      </div>
                    </div>
                    {isUnlocked ? (
                      <div className="bg-indigo-100 text-indigo-600 p-2 rounded-xl">
                        <Unlock size={20} />
                      </div>
                    ) : (
                      <div className="bg-gray-100 text-gray-400 p-2 rounded-xl">
                        <Lock size={20} />
                      </div>
                    )}
                  </div>
                  <p className="text-[#8C7A6B] mb-6">{item.desc}</p>
                </div>
                
                <button 
                  onClick={() => handlePurchase(item)}
                  className={`w-full py-3 rounded-xl font-bold transition-all flex items-center justify-center gap-2
                    ${isEquipped ? 'bg-emerald-100 text-emerald-700 cursor-default' : 
                      isUnlocked ? 'bg-indigo-500 hover:bg-indigo-600 text-white shadow-md' : 
                      (user.points || 0) >= item.cost ? 'bg-[#C2A878] hover:bg-[#B39969] text-white shadow-md' : 'bg-gray-200 text-gray-500 cursor-not-allowed'}
                  `}
                  disabled={isEquipped}
                >
                  {isEquipped ? '已裝備' : isUnlocked ? '立即裝備' : `解鎖 (${item.cost} XP)`}
                </button>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
