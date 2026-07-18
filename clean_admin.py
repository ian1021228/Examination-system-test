import re

with open("src/features.tsx", "r") as f:
    content = f.read()

# We know the first occurrence of "  if (isFullscreen && activeMat) {" is inside CourseMaterialsAdminTab
admin_start = "export function CourseMaterialsAdminTab"
admin_idx = content.find(admin_start)

if admin_idx != -1:
    is_fullscreen_start = content.find("  if (isFullscreen && activeMat) {", admin_idx)
    filtered_mats = content.find("  const filteredMats = filterUnit === 'all'", is_fullscreen_start)
    if is_fullscreen_start != -1 and filtered_mats != -1:
        # We delete this entire block
        content = content[:is_fullscreen_start] + content[filtered_mats:]

with open("src/features.tsx", "w") as f:
    f.write(content)

print("Cleaned admin")
