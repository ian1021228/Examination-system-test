import re

with open("src/App.tsx", "r") as f:
    content = f.read()

# Add import for Announcement if missing
if "Announcement" not in content:
    content = content.replace("import { LandingPage", "import { LandingPage, Announcement")

# Add fetch logic to SubjectSelect
fetch_logic = """export function SubjectSelect() {
  const navigate = useNavigate();
  const [announcements, setAnnouncements] = useState<Announcement[]>([]);

  useEffect(() => {
    const q = query(collection(db, 'announcements'), orderBy('createdAt', 'desc'), limit(5));
    const unsub = onSnapshot(q, (snap) => {
      setAnnouncements(snap.docs.map(d => ({ id: d.id, ...d.data() } as Announcement)));
    });
    return unsub;
  }, []);
"""

content = content.replace("export function SubjectSelect() {\n  const navigate = useNavigate();", fetch_logic)

# Add UI to SubjectSelect
ui_logic = """
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {SUBJECT_CONFIGS.map(subj => (
          <div 
            key={subj.id}
            onClick={() => navigate(`/subject/${subj.id}/tasks`)}
            className="bg-[#FDFBF7]/60 border border-[#EAE6DF] rounded-3xl p-6 cursor-pointer hover:border-[#D5CFC4] transition-all transform hover:-translate-y-1 hover:shadow-md group"
          >
            <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${subj.color} flex items-center justify-center text-3xl mb-4 shadow-sm`}>
              {subj.icon}
            </div>
            <h3 className="font-serif text-xl font-bold text-[#4A3F35] mb-1 group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-white group-hover:to-gray-400 transition-all">
              {SUBJECT_LABELS[subj.id]}
            </h3>
            <p className="text-sm text-[#A69B8F]">點擊進入 {SUBJECT_LABELS[subj.id]} 任務中心</p>
          </div>
        ))}
      </div>

      {/* Announcements */}
      <div className="mt-16">
        <div className="flex items-center gap-2 mb-8">
          <Calendar className="text-[#C2A878]" size={28} />
          <h2 className="text-3xl font-bold text-[#4A3F35] font-serif">平台公告</h2>
        </div>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {announcements.map(a => (
            <div key={a.id} className="bg-white border border-[#EAE6DF] rounded-2xl p-6 shadow-sm hover:shadow-md transition-all group">
              <div className="flex justify-between items-start mb-4">
                <h3 className="font-bold text-lg text-[#4A3F35] group-hover:text-[#B39969] transition-colors">{a.title}</h3>
              </div>
              <p className="text-[#8C7A6B] text-sm line-clamp-3 whitespace-pre-wrap">{a.content}</p>
              <div className="mt-4 pt-4 border-t border-[#EAE6DF] flex justify-between text-xs text-[#A69B8F]">
                <span>{a.author}</span>
                <span>{new Date(a.createdAt).toLocaleDateString()}</span>
              </div>
            </div>
          ))}
          {announcements.length === 0 && (
            <div className="col-span-full text-center py-10 text-[#A69B8F]">目前沒有平台公告</div>
          )}
        </div>
      </div>
"""

content = content.replace("""      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {SUBJECT_CONFIGS.map(subj => (
          <div 
            key={subj.id}
            onClick={() => navigate(`/subject/${subj.id}/tasks`)}
            className="bg-[#FDFBF7]/60 border border-[#EAE6DF] rounded-3xl p-6 cursor-pointer hover:border-[#D5CFC4] transition-all transform hover:-translate-y-1 hover:shadow-md group"
          >
            <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${subj.color} flex items-center justify-center text-3xl mb-4 shadow-sm`}>
              {subj.icon}
            </div>
            <h3 className="font-serif text-xl font-bold text-[#4A3F35] mb-1 group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-white group-hover:to-gray-400 transition-all">
              {SUBJECT_LABELS[subj.id]}
            </h3>
            <p className="text-sm text-[#A69B8F]">點擊進入 {SUBJECT_LABELS[subj.id]} 任務中心</p>
          </div>
        ))}
      </div>""", ui_logic)

# Make sure Calendar is imported if we are using it
if "Calendar" not in content[:content.find("from 'lucide-react'")]:
    content = content.replace("import { ", "import { Calendar, ")


with open("src/App.tsx", "w") as f:
    f.write(content)

print("Success")
