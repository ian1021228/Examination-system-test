import re

with open("src/features.tsx", "r") as f:
    content = f.read()

if "import { createPortal } from 'react-dom';" not in content:
    content = "import { createPortal } from 'react-dom';\n" + content

# Replace the first modal return
old_modal_start = """  if (isFullscreen && activeMat) {
    return (
      <div className="fixed inset-0 z-50 bg-[#FDFBF7] flex flex-col h-screen overflow-hidden">"""

new_modal_start = """  if (isFullscreen && activeMat) {
    return createPortal(
      <div className="fixed inset-0 z-[100] bg-[#FDFBF7] flex flex-col h-screen overflow-hidden">"""

content = content.replace(old_modal_start, new_modal_start)

# End of the first modal return (it's right before `const filteredMats = filterUnit === 'all' ? materials : materials.filter(m => m.unit === filterUnit);`)
old_modal_end = """        )}
      </div>
    );
  }
  const filteredMats"""

new_modal_end = """        )}
      </div>,
      document.body
    );
  }
  const filteredMats"""

content = content.replace(old_modal_end, new_modal_end)

with open("src/features.tsx", "w") as f:
    f.write(content)
print("Success")
