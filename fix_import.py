with open("src/App.tsx", "r") as f:
    content = f.read()

import_str = "import { LandingPage, AnnouncementsAdminTab, CourseMaterialsAdminTab, DiscussionBoard, CourseMaterialsStudentView, GamificationProfile } from './features';\n"
if "from './features'" not in content:
    content = content.replace("import html2pdf from 'html2pdf.js';", "import html2pdf from 'html2pdf.js';\n" + import_str)

with open("src/App.tsx", "w") as f:
    f.write(content)
