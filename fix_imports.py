import re

with open("src/App.tsx", "r") as f:
    content = f.read()

# Add missing firestore imports if they exist
imports_match = re.search(r"import \{.*?\} from 'firebase/firestore';", content)
if imports_match:
    imports_str = imports_match.group(0)
    new_imports = imports_str
    if "limit" not in new_imports:
        new_imports = new_imports.replace("from 'firebase/firestore'", ", limit from 'firebase/firestore'")
    if "onSnapshot" not in new_imports:
        new_imports = new_imports.replace("from 'firebase/firestore'", ", onSnapshot from 'firebase/firestore'")
    content = content.replace(imports_str, new_imports)

with open("src/App.tsx", "w") as f:
    f.write(content)
print("Success")
