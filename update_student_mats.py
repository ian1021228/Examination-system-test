import re

with open("src/features.tsx", "r") as f:
    content = f.read()

student_view_old = """  useEffect(() => {
    const fetchMats = async () => {
      const q = query(collection(db, 'materials'), where('subjectId', '==', subjectId), orderBy('createdAt', 'desc'));
      const snap = await getDocs(q);
      setMaterials(snap.docs.map(d => ({ id: d.id, ...d.data() } as CourseMaterial)));
    };
    fetchMats();
  }, [subjectId]);"""

student_view_new = """  useEffect(() => {
    const fetchMats = async () => {
      const q = query(collection(db, 'materials'), where('subjectId', '==', subjectId), orderBy('createdAt', 'desc'));
      const snap = await getDocs(q);
      const data = snap.docs.map(d => ({ id: d.id, ...d.data() } as CourseMaterial));
      data.sort((a, b) => a.unit - b.unit || b.createdAt - a.createdAt);
      setMaterials(data);
    };
    fetchMats();
  }, [subjectId]);"""

content = content.replace(student_view_old, student_view_new)

with open("src/features.tsx", "w") as f:
    f.write(content)
