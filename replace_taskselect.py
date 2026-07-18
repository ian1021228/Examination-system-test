with open("src/App.tsx", "r") as f:
    content = f.read()

taskselect_code = """export function TaskSelect({ user }: { user: UserProfile }) {
  const { subjectId } = useParams<{ subjectId: Subject }>();
  const navigate = useNavigate();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'tasks'|'mistakes'|'leaderboard'|'materials'>('tasks');

  useEffect(() => {
    if (!subjectId) return;
    const fetchTasks = async () => {
      try {
        const q = query(
          collection(db, 'tasks'),
          where('subject', '==', subjectId),
          where('isActive', '==', true)
        );
        const snap = await getDocs(q);
        const tasksData = snap.docs.map(d => ({ id: d.id, ...d.data() } as Task));
        tasksData.sort((a, b) => b.createdAt - a.createdAt);
        setTasks(tasksData);
      } catch (e) {
        console.error(e);
      }
      setLoading(false);
    };
    fetchTasks();
  }, [subjectId]);

  return (
    <div className="max-w-6xl w-full mx-auto py-10 space-y-8">
      <GamificationProfile user={user} />
      
      <div className="flex bg-[#FDFBF7] p-1 rounded-xl w-full max-w-lg border border-[#EAE6DF]">
        <button onClick={() => setActiveTab('materials')} className={`flex-1 px-4 py-2 rounded-lg text-sm font-bold transition-all ${activeTab === 'materials' ? 'bg-[#C2A878] text-[#4A3F35] shadow-sm' : 'text-[#8C7A6B] hover:bg-[#F5F5F0]'}`}>
          先看課 / 教材區
        </button>
        <button onClick={() => setActiveTab('tasks')} className={`flex-1 px-4 py-2 rounded-lg text-sm font-bold transition-all ${activeTab === 'tasks' ? 'bg-[#C2A878] text-[#4A3F35] shadow-sm' : 'text-[#8C7A6B] hover:bg-[#F5F5F0]'}`}>
          測驗任務
        </button>
        <button onClick={() => setActiveTab('mistakes')} className={`flex-1 px-4 py-2 rounded-lg text-sm font-bold transition-all ${activeTab === 'mistakes' ? 'bg-[#C2A878] text-[#4A3F35] shadow-sm' : 'text-[#8C7A6B] hover:bg-[#F5F5F0]'}`}>
          錯題複習
        </button>
        <button onClick={() => setActiveTab('leaderboard')} className={`flex-1 px-4 py-2 rounded-lg text-sm font-bold transition-all ${activeTab === 'leaderboard' ? 'bg-[#C2A878] text-[#4A3F35] shadow-sm' : 'text-[#8C7A6B] hover:bg-[#F5F5F0]'}`}>
          排行榜
        </button>
      </div>

      {activeTab === 'materials' && (
        <div className="space-y-4">
          <div className="flex justify-between items-end">
            <div>
              <button onClick={() => navigate('/select-subject')} className="text-[#A69B8F] hover:text-[#4A3F35] mb-2 flex items-center text-sm transition-colors">
                ← 返回科目選擇
              </button>
              <h2 className="font-serif text-3xl font-black text-[#4A3F35]">課程內容與教材</h2>
              <p className="text-[#8C7A6B] mt-1">在開始測驗前，先閱讀或觀看以下教材吧！</p>
            </div>
          </div>
          <CourseMaterialsStudentView subjectId={subjectId!} user={user} />
        </div>
      )}

      {activeTab === 'tasks' && (
        <div className="space-y-4">
          <div className="flex justify-between items-end">
            <div>
              <button onClick={() => navigate('/select-subject')} className="text-[#A69B8F] hover:text-[#4A3F35] mb-2 flex items-center text-sm transition-colors">
                ← 返回科目選擇
              </button>
              <h2 className="font-serif text-3xl font-black text-[#4A3F35]">選擇任務</h2>
              <p className="text-[#8C7A6B] mt-1">{SUBJECT_LABELS[subjectId!] || subjectId} - 點擊任務開始挑戰</p>
            </div>
          </div>

          {loading ? (
            <div className="text-center py-20 text-[#A69B8F]">尋找任務中...</div>
          ) : (
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {tasks.map(t => (
                <div 
                  key={t.id} 
                  onClick={() => navigate(`/play/${t.id}`)}
                  className="bg-white border border-[#EAE6DF] rounded-3xl p-6 cursor-pointer hover:border-[#C2A878] hover:-translate-y-1 transition-all group shadow-sm"
                >
                  <div className="flex justify-between items-start mb-4">
                    <h3 className="font-serif text-xl font-bold text-[#4A3F35] group-hover:text-[#B39969] transition-colors">{t.title}</h3>
                    <div className="bg-[#EAE2D3] text-[#B39969] p-2 rounded-xl">
                      <Play size={20} className="fill-current" />
                    </div>
                  </div>
                  <div className="flex flex-wrap gap-2 mb-4">
                    <span className="text-xs font-bold bg-[#F5F5F0] text-[#8C7A6B] px-2 py-1 rounded">
                      {t.difficulty === 'easy' ? '簡單' : t.difficulty === 'medium' ? '中等' : t.difficulty === 'hard' ? '困難' : '混合難度'}
                    </span>
                    <span className="text-xs font-bold bg-[#F5F5F0] text-[#8C7A6B] px-2 py-1 rounded">
                      {t.gameMode === 'survival' ? '生存模式' : t.gameMode === 'speed' ? '速答模式' : '一般模式'}
                    </span>
                  </div>
                  <div className="flex justify-between items-center text-sm">
                    <span className="text-[#A69B8F]">題數: {t.questionCount} {t.mcCount !== undefined ? `(選擇 ${t.mcCount}, 填空 ${t.fibCount})` : ""}</span>
                    <div className="flex items-center text-[#BC7665]">
                      {t.maxHearts ? (
                        <>
                          <Heart className="w-4 h-4 fill-current mr-1" />
                          {t.maxHearts}
                        </>
                      ) : (
                        <span className="text-[#8C7A6B]">無限愛心</span>
                      )}
                    </div>
                  </div>
                </div>
              ))}
              {tasks.length === 0 && (
                <div className="col-span-full text-center py-20 text-[#A69B8F] bg-white border border-[#EAE6DF] rounded-3xl">
                  目前沒有可用的任務
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {activeTab === 'mistakes' && <MistakesTab user={user} />}
      {activeTab === 'leaderboard' && <LeaderboardTab user={user} />}
    </div>
  );
}"""

import re
# Regex to match export function TaskSelect({ user }: { user: UserProfile }) { ... until the next export function Gameplay({ user }: { user: UserProfile }) {
pattern = re.compile(r"export function TaskSelect\({ user }: \{ user: UserProfile \}\) \{.*?(?=export function Gameplay)", re.DOTALL)

content = pattern.sub(taskselect_code + "\n\n", content)

with open("src/App.tsx", "w") as f:
    f.write(content)
