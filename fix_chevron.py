import re

with open("src/features.tsx", "r") as f:
    content = f.read()

content = content.replace("import { ChevronLeft, ", "import { ")

# Now properly add ChevronLeft ONLY to lucide-react import
import_lucide = re.search(r"import \{.*?\} from 'lucide-react';", content)
if import_lucide:
    lucide_str = import_lucide.group(0)
    new_lucide = lucide_str.replace("import { ", "import { ChevronLeft, ")
    content = content.replace(lucide_str, new_lucide)

with open("src/features.tsx", "w") as f:
    f.write(content)
print("Success")
