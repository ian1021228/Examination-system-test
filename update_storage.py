import re

with open("src/App.tsx", "r") as f:
    content = f.read()

content = content.replace(
    "import { getFirestore, doc, getDoc, setDoc, collection, query, where, getDocs, addDoc, deleteDoc, updateDoc } from 'firebase/firestore';",
    "import { getFirestore, doc, getDoc, setDoc, collection, query, where, getDocs, addDoc, deleteDoc, updateDoc } from 'firebase/firestore';\nimport { getStorage } from 'firebase/storage';"
)

content = content.replace(
    "export const db = getFirestore(app);",
    "export const db = getFirestore(app);\nexport const storage = getStorage(app);"
)

with open("src/App.tsx", "w") as f:
    f.write(content)

with open("src/features.tsx", "r") as f:
    feat = f.read()

feat = feat.replace(
    "import { db, auth } from './App';",
    "import { db, auth, storage } from './App';\nimport { ref, uploadBytes, getDownloadURL } from 'firebase/storage';\nimport Markdown from 'react-markdown';"
)

with open("src/features.tsx", "w") as f:
    f.write(feat)
