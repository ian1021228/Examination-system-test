import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Add adminMode state
if "const [adminMode, setAdminMode]" not in content:
    content = content.replace("const [loading, setLoading] = useState(true);", "const [loading, setLoading] = useState(true);\n  const [adminMode, setAdminMode] = useState<'testing' | 'teaching'>('testing');")

# Replace tabs section
tabs_section_old = """      <div className="flex space-x-2 border-b border-[#EAE6DF] overflow-x-auto pb-2">
        <Tab btnTab="tasks" current={activeTab} set={setActiveTab as any} label="任務管理" icon={<List size={16} />} />
        <Tab btnTab="questions" current={activeTab} set={setActiveTab as any} label="題庫一覽" icon={<BookOpen size={16} />} />
        <Tab btnTab="import" current={activeTab} set={setActiveTab as any} label="匯入題庫" icon={<Upload size={16} />} />
        <Tab btnTab="attempts" current={activeTab} set={setActiveTab as any} label="作答數據" icon={<CheckCircle size={16} />} />
        <Tab btnTab="paper" current={activeTab} set={setActiveTab as any} label="紙本測驗" icon={<Printer size={16} />} />
        <Tab btnTab="settings" current={activeTab} set={setActiveTab as any} label="科目設定" icon={<Settings size={16} />} />
      </div>"""

tabs_section_new = """      <div className="flex flex-col space-y-4 border-b border-[#EAE6DF] pb-4">
        <div className="flex bg-[#F5F5F0] p-1 rounded-xl w-fit border border-[#EAE6DF]">
          <button onClick={() => { setAdminMode('teaching'); setActiveTab('materials'); }} className={`px-6 py-2 rounded-lg text-sm font-bold transition-all ${adminMode === 'teaching' ? 'bg-[#C2A878] text-[#4A3F35] shadow-sm' : 'text-[#8C7A6B] hover:bg-[#EAE6DF]'}`}>
            📚 教學區
          </button>
          <button onClick={() => { setAdminMode('testing'); setActiveTab('tasks'); }} className={`px-6 py-2 rounded-lg text-sm font-bold transition-all ${adminMode === 'testing' ? 'bg-[#C2A878] text-[#4A3F35] shadow-sm' : 'text-[#8C7A6B] hover:bg-[#EAE6DF]'}`}>
            📝 測驗區
          </button>
        </div>

        {adminMode === 'testing' ? (
          <div className="flex space-x-2 overflow-x-auto">
            <Tab btnTab="tasks" current={activeTab} set={setActiveTab as any} label="任務管理" icon={<List size={16} />} />
            <Tab btnTab="questions" current={activeTab} set={setActiveTab as any} label="題庫一覽" icon={<BookOpen size={16} />} />
            <Tab btnTab="import" current={activeTab} set={setActiveTab as any} label="匯入題庫" icon={<Upload size={16} />} />
            <Tab btnTab="attempts" current={activeTab} set={setActiveTab as any} label="作答數據" icon={<CheckCircle size={16} />} />
            <Tab btnTab="paper" current={activeTab} set={setActiveTab as any} label="紙本測驗" icon={<Printer size={16} />} />
            <Tab btnTab="settings" current={activeTab} set={setActiveTab as any} label="科目設定" icon={<Settings size={16} />} />
          </div>
        ) : (
          <div className="flex space-x-2 overflow-x-auto">
            <Tab btnTab="materials" current={activeTab} set={setActiveTab as any} label="教材編輯系統" icon={<BookOpen size={16} />} />
          </div>
        )}
      </div>"""

content = content.replace(tabs_section_old, tabs_section_new)

# Make sure CourseMaterialsAdminTab is rendered
render_section_old = """            {activeTab === 'settings' && <SettingsTab config={config} subjectId={subjectId} />}
          </>"""

render_section_new = """            {activeTab === 'settings' && <SettingsTab config={config} subjectId={subjectId} />}
            {activeTab === 'materials' && <CourseMaterialsAdminTab subjectId={subjectId!} />}
          </>"""

if "CourseMaterialsAdminTab" not in content.split(render_section_old)[0]:
    content = content.replace(render_section_old, render_section_new)

with open('src/App.tsx', 'w') as f:
    f.write(content)
