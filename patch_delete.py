import re

with open("src/App.tsx", "r") as f:
    content = f.read()

old_delete = """  const handleJsonDelete = async () => {
    if (!textInput.trim()) return;
    setIsImporting(true);
    try {
      const data = JSON.parse(textInput);
      if (!Array.isArray(data)) throw new Error('內容必須是 JSON 陣列');
      
      const promptsToDelete = data.map((item: any) => item.prompt).filter(Boolean);"""

new_delete = """  const handleJsonDelete = async () => {
    if (!textInput.trim()) return;
    setIsImporting(true);
    try {
      const data = parseRobustJSON(textInput);
      if (!Array.isArray(data)) throw new Error('內容必須是 JSON 陣列');
      
      const promptsToDelete = data.map((item: any) => item.prompt ? item.prompt.replace(/\\[SOURCE_IMAGE\\]/g, '') : '').filter(Boolean);"""

content = content.replace(old_delete, new_delete)

with open("src/App.tsx", "w") as f:
    f.write(content)
