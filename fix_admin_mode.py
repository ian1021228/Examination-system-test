with open("src/App.tsx", "r") as f:
    content = f.read()

import re

# Remove adminMode from places other than AdminSubjectView
# We'll first remove ALL of them, then add it exactly where we want.
content = content.replace("  const [adminMode, setAdminMode] = useState<'testing' | 'teaching'>('testing');\n", "")

# Now add it back specifically to AdminSubjectView
# export function AdminSubjectView() {
#   const { subjectId } = useParams<{ subjectId: Subject }>();
#   const navigate = useNavigate();
#   const [activeTab, setActiveTab] = useState<'tasks' | 'questions' | 'ai' | 'import' | 'settings' | 'attempts' | 'paper' | 'materials'>('tasks');
#   const [loading, setLoading] = useState(true);

target = "export function AdminSubjectView() {\n  const { subjectId } = useParams<{ subjectId: Subject }>();\n  const navigate = useNavigate();\n  const [activeTab, setActiveTab] = useState<'tasks' | 'questions' | 'ai' | 'import' | 'settings' | 'attempts' | 'paper' | 'materials'>('tasks');\n  const [loading, setLoading] = useState(true);"
replacement = target + "\n  const [adminMode, setAdminMode] = useState<'testing' | 'teaching'>('testing');"

content = content.replace(target, replacement)

with open("src/App.tsx", "w") as f:
    f.write(content)
