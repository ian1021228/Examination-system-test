import re

with open("src/features.tsx", "r") as f:
    content = f.read()

new_upload = """  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;
    
    Array.from(files).forEach(async (file) => {
      const fileId = Math.random().toString(36).substring(7);
      const fileRef = ref(storage, `materials/${subjectId}/${Date.now()}_${file.name}`);
      
      setUploadingFiles(prev => [...prev, { name: file.name, progress: 0, task: null, id: fileId } as any]);

      try {
        const interval = setInterval(() => {
           setUploadingFiles(prev => prev.map(f => f.id === fileId ? { ...f, progress: Math.min(f.progress + 10, 90) } : f));
        }, 500);

        await uploadBytes(fileRef, file);
        const url = await getDownloadURL(fileRef);
        
        clearInterval(interval);
        
        setNewMat(prev => ({ ...prev, attachments: [...(prev.attachments || []), { name: file.name, url }] }));
        toast(`上傳成功: ${file.name}`);
      } catch (error: any) {
        console.error('Upload Error:', error);
        if (error.message && error.message.includes("CORS")) {
            toast(`上傳失敗: 請設定 Firebase Storage CORS`);
        } else {
            toast(`上傳失敗: ${file.name} (${error.message})`);
        }
      } finally {
        setUploadingFiles(prev => prev.filter(f => f.id !== fileId));
      }
    });
    
    e.target.value = '';
  };

  const cancelUpload = (task: any) => {
    toast('一般上傳無法取消');
  };"""

# Replace everything from `const handleFileUpload` to the end of `cancelUpload`
start = content.find("  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {")
end = content.find("  const removeAttachment = (index: number) => {")

if start != -1 and end != -1:
    content = content[:start] + new_upload + "\n\n" + content[end:]
    with open("src/features.tsx", "w") as f:
        f.write(content)
    print("Success")
else:
    print("Failed to find bounds")
