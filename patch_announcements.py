import re

with open("src/features.tsx", "r") as f:
    content = f.read()

# Add import if missing
if "confirmModal" not in content:
    content = content.replace("import { toast } from './toast';", "import { toast } from './toast';\nimport { confirmModal } from './confirm';")

# Replace confirm with await confirmModal
content = content.replace("if (confirm('確定刪除此公告？')) {", "if (await confirmModal('確定刪除此公告？')) {")

# Also check other confirms in features.tsx
content = content.replace("if (confirm('確定刪除此教材？無法復原。')) {", "if (await confirmModal('確定刪除此教材？無法復原。')) {")

with open("src/features.tsx", "w") as f:
    f.write(content)

print("Success")
