import re

with open("src/features.tsx", "r") as f:
    content = f.read()

new_upload = """  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;
    
    Array.from(files).forEach(file => {
      const fileRef = ref(storage, `materials/${subjectId}/${Date.now()}_${file.name}`);
      const uploadTask = uploadBytesResumable(fileRef, file);
      
      const fileId = Math.random().toString(36).substring(7);
      
      setUploadingFiles(prev => [...prev, { name: file.name, progress: 0, task: uploadTask, id: fileId } as any]);

      uploadTask.on('state_changed', 
        (snapshot) => {
          const progress = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
          console.log(`Upload progress for ${file.name}: ${progress}%`);
          setUploadingFiles(prev => prev.map(f => f.id === fileId ? { ...f, progress } : f));
        }, 
        (error) => {
          console.error('Upload Error:', error);
          toast(`上傳失敗: ${file.name} (${error.message})`);
          setUploadingFiles(prev => prev.filter(f => f.id !== fileId));
        }, 
        async () => {
          console.log('Upload complete for', file.name);
          try {
            const url = await getDownloadURL(uploadTask.snapshot.ref);
            setNewMat(prev => ({ ...prev, attachments: [...(prev.attachments || []), { name: file.name, url }] }));
            toast(`上傳成功: ${file.name}`);
          } catch (err: any) {
             console.error('Error getting download URL:', err);
             toast(`取得下載連結失敗: ${file.name}`);
          } finally {
            setUploadingFiles(prev => prev.filter(f => f.id !== fileId));
          }
        }
      );
    });
    
    e.target.value = '';
  };"""

content = re.sub(r"  const handleFileUpload = \(e: React\.ChangeEvent<HTMLInputElement>\) => \{.*?\n  \};\n"
                 r"\n  const cancelUpload", 
                 new_upload + "\n\n  const cancelUpload", content, flags=re.DOTALL)

with open("src/features.tsx", "w") as f:
    f.write(content)
