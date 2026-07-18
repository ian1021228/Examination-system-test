import re

with open("src/App.tsx", "r") as f:
    content = f.read()

content = content.replace("import { Calendar, ", "import { ")

# But now Calendar from lucide-react is missing, let's add it back
import_lucide = re.search(r"import \{.*?\} from 'lucide-react';", content)
if import_lucide:
    lucide_str = import_lucide.group(0)
    new_lucide = lucide_str.replace("import { ", "import { Calendar, ")
    content = content.replace(lucide_str, new_lucide)

with open("src/App.tsx", "w") as f:
    f.write(content)
print("Success")
