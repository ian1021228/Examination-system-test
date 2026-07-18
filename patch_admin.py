with open("src/App.tsx", "r") as f:
    content = f.read()

# Add imports
if "from './features'" not in content:
    content = content.replace("import { toast } from './toast';", "import { toast } from './toast';\nimport { LandingPage, AnnouncementsAdminTab, CourseMaterialsAdminTab, DiscussionBoard, CourseMaterialsStudentView, GamificationProfile } from './features';")

# Add to AdminDashboard or AdminSubjectView
# Let's add Announcements to AdminDashboard, and Materials to AdminSubjectView.

# In AdminSubjectView:
# 1. Update state type
content = content.replace("useState<'tasks' | 'questions' | 'ai' | 'import' | 'settings' | 'attempts' | 'paper'>", "useState<'tasks' | 'questions' | 'ai' | 'import' | 'settings' | 'attempts' | 'paper' | 'materials'>")

# 2. Add Tab button
tab_btn_import = "<Tab btnTab=\"import\" current={activeTab} set={setActiveTab} label=\"匯入\" icon=\"📥\" />"
new_tab_btn = tab_btn_import + "\n            <Tab btnTab=\"materials\" current={activeTab} set={setActiveTab} label=\"教材\" icon=\"📚\" />"
content = content.replace(tab_btn_import, new_tab_btn)

# 3. Add Tab component render
tab_render_import = "{activeTab === 'import' && <ImportTab subjectId={subjectId!} config={config} />}"
new_tab_render = tab_render_import + "\n            {activeTab === 'materials' && <CourseMaterialsAdminTab subjectId={subjectId!} />}"
content = content.replace(tab_render_import, new_tab_render)

# In AdminDashboard:
# Add announcements button or section.
# Actually let's just make a new tab in AdminDashboard for global announcements.
# Currently AdminDashboard doesn't have tabs.
content = content.replace("""<h2 className="font-serif text-3xl font-black text-[#4A3F35]">總指揮中心</h2>""", """<div className="flex items-center gap-4">
            <h2 className="font-serif text-3xl font-black text-[#4A3F35]">總指揮中心</h2>
          </div>""")

if "AnnouncementsAdminTab" not in content.split("export function AdminDashboard")[1].split("export function AdminSubjectView")[0]:
    # It's easier to just insert AnnouncementsAdminTab below the subject grid.
    admin_grid = "</div>\n    </div>\n  );\n}"
    if admin_grid in content:
        content = content.replace(admin_grid, """</div>
      <div className="mt-12">
        <div className="flex items-center gap-2 mb-6">
          <h2 className="font-serif text-2xl font-black text-[#4A3F35]">平台公告管理</h2>
        </div>
        <AnnouncementsAdminTab />
      </div>
    </div>
  );
}""", 1)


with open("src/App.tsx", "w") as f:
    f.write(content)
