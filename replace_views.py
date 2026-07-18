import re

with open("src/features.tsx", "r") as f:
    content = f.read()

# Find bounds of CourseMaterialsAdminTab
start_admin = content.find("export function CourseMaterialsAdminTab")
start_student = content.find("export function CourseMaterialsStudentView")
end_student = content.find("export function GamificationProfile")

if start_admin != -1 and start_student != -1 and end_student != -1:
    before = content[:start_admin]
    after = content[end_student:]
    with open("src/features.tsx", "w") as f:
        f.write(before + "// REPLACE_MARKER\n\n" + after)
else:
    print("Could not find bounds")
