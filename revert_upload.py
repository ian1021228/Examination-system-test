import re

with open("src/features.tsx", "r") as f:
    content = f.read()

new_upload = """  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;
    
    Array.from(files).forEach(file => {
      const fileId = Math.random().toString(36).substring(7);
      const fileRef = ref(storage, `materials/${subjectId}/${Date.now()}_${file.name}`);
      const uploadTask = uploadBytesResumable(fileRef, file);
      
      setUploadingFiles(prev => [...prev, { name: file.name, progress: 0, task: uploadTask, id: fileId } as any]);

      uploadTask.on('state_changed', 
        (snapshot) => {
          const progress = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
          setUploadingFiles(prev => prev.map(f => f.id === fileId ? { ...f, progress } : f));
        }, 
        (error) => {
          console.error('Upload Error:', error);
          toast(`上傳失敗: ${file.name} (${error.message})`);
          setUploadingFiles(prev => prev.filter(f => f.id !== fileId));
        }, 
        async () => {
          try {
            const url = await getDownloadURL(uploadTask.snapshot.ref);
            setNewMat(prev => ({ ...prev, attachments: [...(prev.attachments || []), { name: file.name, url }] }));
            toast(`上傳成功: ${file.name}`);
          } catch(err) {
            console.error(err);
            toast(`取得連結失敗: ${file.name}`);
          } finally {
            setUploadingFiles(prev => prev.filter(f => f.id !== fileId));
          }
        }
      );
    });
    
    e.target.value = '';
  };

  const cancelUpload = (task: any) => {
    try {
      task.cancel();
    } catch(e) {}
    setUploadingFiles(prev => prev.filter(f => f.task !== task));
    toast('已取消上傳');
  };"""

start = content.find("  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {")
end = content.find("  const removeAttachment = (index: number) => {")

if start != -1 and end != -1:
    content = content[:start] + new_upload + "\n\n" + content[end:]
    with open("src/features.tsx", "w") as f:
        f.write(content)
    print("Success")
else:
    print("Failed to find bounds")
