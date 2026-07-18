with open("src/features.tsx", "r") as f:
    content = f.read()

with open("new_views.tsx", "r") as f:
    new_views = f.read()

content = content.replace("// REPLACE_MARKER\n", new_views)

with open("src/features.tsx", "w") as f:
    f.write(content)
