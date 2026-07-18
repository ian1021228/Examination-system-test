with open("src/App.tsx", "r") as f:
    content = f.read()

# 1. Update Route definition for LandingPage
content = content.replace(
    '<Route path="/" element={!user ? <SignIn /> : <Navigate to={user.role === \'admin\' ? "/admin" : "/select-subject"} />} />',
    '<Route path="/" element={!user ? <LandingPage /> : <Navigate to={user.role === \'admin\' ? "/admin" : "/select-subject"} />} />'
)

# 2. Modify TaskSelect to include GamificationProfile and CourseMaterials
task_select_func = "export function TaskSelect({ user }: { user: UserProfile }) {"
if "const [activeTab, setActiveTab]" not in content.split(task_select_func)[1].split("return (")[0]:
    # Need to insert activeTab
    content = content.replace(
        "const navigate = useNavigate();\n  const [tasks, setTasks] = useState<Task[]>([]);",
        "const navigate = useNavigate();\n  const [tasks, setTasks] = useState<Task[]>([]);\n  const [activeTab, setActiveTab] = useState<'tasks' | 'materials'>('tasks');"
    )

    # Change the return statement to wrap everything in a div and add Tabs & Gamification
    # Find the first div after return (
    split_content = content.split("export function TaskSelect({ user }: { user: UserProfile }) {")
    part2 = split_content[1]
    
    # Find return ( ... <div className="max-w-6xl w-full mx-auto py-10 space-y-8">
    # We will replace <div className="max-w-6xl w-full mx-auto py-10 space-y-8"> with a version that has GamificationProfile
    
    part2 = part2.replace(
        '<div className="max-w-6xl w-full mx-auto py-10 space-y-8">',
        '''<div className="max-w-6xl w-full mx-auto py-10 space-y-8">
      <GamificationProfile user={user} />
      <div className="flex bg-[#FDFBF7] p-1 rounded-xl w-full max-w-sm border border-[#EAE6DF]">
        <button onClick={() => setActiveTab('tasks')} className={`flex-1 px-4 py-2 rounded-lg text-sm font-bold transition-all ${activeTab === 'tasks' ? 'bg-[#C2A878] text-[#4A3F35] shadow-sm' : 'text-[#8C7A6B] hover:bg-[#F5F5F0]'}`}>測驗任務</button>
        <button onClick={() => setActiveTab('materials')} className={`flex-1 px-4 py-2 rounded-lg text-sm font-bold transition-all ${activeTab === 'materials' ? 'bg-[#C2A878] text-[#4A3F35] shadow-sm' : 'text-[#8C7A6B] hover:bg-[#F5F5F0]'}`}>先看課 / 教材區</button>
      </div>''', 1
    )
    
    # We also need to conditionally render the old content vs new content.
    # The old content starts with:
    # <div className="flex justify-between items-end">
    # We should wrap it in `{activeTab === 'tasks' && (` ... `)}`
    
    # Find the block we want to wrap
    # Let's just use string replacement carefully.
    part2 = part2.replace(
        '''<div className="flex justify-between items-end">
        <div>
          <button onClick={() => navigate('/select-subject')} className="text-[#A69B8F] hover:text-[#4A3F35] mb-2 flex items-center text-sm transition-colors">
            ← 返回科目選擇
          </button>
          <h2 className="font-serif text-3xl font-black text-[#4A3F35]">選擇任務</h2>
          <p className="text-[#8C7A6B] mt-1">{SUBJECT_LABELS[subjectId!] || subjectId} - 點擊任務開始挑戰</p>
        </div>
      </div>''',
      '''{activeTab === 'materials' && (
        <div className="space-y-4">
          <div>
            <button onClick={() => navigate('/select-subject')} className="text-[#A69B8F] hover:text-[#4A3F35] mb-2 flex items-center text-sm transition-colors">
              ← 返回科目選擇
            </button>
            <h2 className="font-serif text-3xl font-black text-[#4A3F35]">課程內容與教材</h2>
            <p className="text-[#8C7A6B] mt-1">在開始測驗前，先閱讀或觀看以下教材吧！</p>
          </div>
          <CourseMaterialsStudentView subjectId={subjectId!} user={user} />
        </div>
      )}
      
      {activeTab === 'tasks' && (
        <>
          <div className="flex justify-between items-end">
            <div>
              <button onClick={() => navigate('/select-subject')} className="text-[#A69B8F] hover:text-[#4A3F35] mb-2 flex items-center text-sm transition-colors">
                ← 返回科目選擇
              </button>
              <h2 className="font-serif text-3xl font-black text-[#4A3F35]">選擇任務</h2>
              <p className="text-[#8C7A6B] mt-1">{SUBJECT_LABELS[subjectId!] || subjectId} - 點擊任務開始挑戰</p>
            </div>
          </div>'''
    )
    
    # Also wrap the grid with tasks
    part2 = part2.replace(
        '''{tasks.length === 0 && (
          <div className="col-span-full text-center py-20 text-[#A69B8F] bg-white border border-[#EAE6DF] rounded-3xl">
            目前沒有可用的任務
          </div>
        )}
      </div>''',
        '''{tasks.length === 0 && (
          <div className="col-span-full text-center py-20 text-[#A69B8F] bg-white border border-[#EAE6DF] rounded-3xl">
            目前沒有可用的任務
          </div>
        )}
      </div>
      </>
      )}'''
    )

    content = split_content[0] + "export function TaskSelect({ user }: { user: UserProfile }) {" + part2

with open("src/App.tsx", "w") as f:
    f.write(content)
