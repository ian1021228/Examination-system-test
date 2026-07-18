import re

with open("src/App.tsx", "r") as f:
    content = f.read()

content = content.replace("} , limit , onSnapshot from 'firebase/firestore';", ", limit, onSnapshot } from 'firebase/firestore';")

with open("src/App.tsx", "w") as f:
    f.write(content)
print("Success")
