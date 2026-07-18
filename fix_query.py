import re

with open("src/features.tsx", "r") as f:
    content = f.read()

content = content.replace(
    "query(collection(db, 'materials'), where('subjectId', '==', subjectId), orderBy('createdAt', 'desc'))",
    "query(collection(db, 'materials'), where('subjectId', '==', subjectId))"
)

with open("src/features.tsx", "w") as f:
    f.write(content)
