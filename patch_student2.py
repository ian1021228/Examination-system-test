with open("src/App.tsx", "r") as f:
    content = f.read()

# 1. Update Route definition for LandingPage (Already done but double check)
content = content.replace(
    '<Route path="/" element={!user ? <SignIn /> : <Navigate to={user.role === \'admin\' ? "/admin" : "/select-subject"} />} />',
    '<Route path="/" element={!user ? <LandingPage /> : <Navigate to={user.role === \'admin\' ? "/admin" : "/select-subject"} />} />'
)

# 2. Update activeTab type
task_select_func = "export function TaskSelect({ user }: { user: UserProfile }) {"
split_content = content.split(task_select_func)
part2 = split_content[1]

part2 = part2.replace(
    "useState<'tasks'|'mistakes'|'leaderboard'>('tasks');",
    "useState<'tasks'|'mistakes'|'leaderboard'|'materials'>('tasks');"
)

# Insert GamificationProfile and new Tab
part2 = part2.replace(
    '<div className="max-w-6xl w-full mx-auto py-10 space-y-8">',
    '''<div className="max-w-6xl w-full mx-auto py-10 space-y-8">
      <GamificationProfile user={user} />'''
)

# Add materials to tabs buttons
old_tabs = '''<button onClick={() => setActiveTab('leaderboard')} className={`flex-1 px-4 py-2 rounded-lg text-sm font-bold transition-all ${activeTab === 'leaderboard' ? 'bg-[#C2A878] text-[#4A3F35] shadow-sm' : 'text-[#8C7A6B] hover:bg-[#F5F5F0]'}`}>
          排行榜
        </button>'''
new_tabs = old_tabs + '''
        <button onClick={() => setActiveTab('materials')} className={`flex-1 px-4 py-2 rounded-lg text-sm font-bold transition-all ${activeTab === 'materials' ? 'bg-[#C2A878] text-[#4A3F35] shadow-sm' : 'text-[#8C7A6B] hover:bg-[#F5F5F0]'}`}>
          先看課 / 教材區
        </button>'''
part2 = part2.replace(old_tabs, new_tabs)

# Add materials render view
# It renders at the end before </div></div>
# Let's find where Leaderboard Tab renders:
# {activeTab === 'leaderboard' && <LeaderboardTab user={user} />}
part2 = part2.replace(
    "{activeTab === 'leaderboard' && <LeaderboardTab user={user} />}",
    "{activeTab === 'leaderboard' && <LeaderboardTab user={user} />}\n      {activeTab === 'materials' && <CourseMaterialsStudentView subjectId={subjectId!} user={user} />}"
)

content = split_content[0] + task_select_func + part2

with open("src/App.tsx", "w") as f:
    f.write(content)
