import re

with open("src/App.tsx", "r") as f:
    content = f.read()

old_process = """      await addDoc(collection(db, 'questions'), {
        subject: subjectId,
        unit: parseInt(String(itemUnit)) || 1,
        difficulty: itemDiff,
        type: itemType,
        prompt: String(prompt).replace(/\\[SOURCE_IMAGE\\]/g, ''),
        options: options,
        correctAnswer: String(correctAnswer),
        clue: clue,
        createdAt: Date.now()
      } as Omit<Question, 'id'>);"""

new_process = """      let mediaUrl = item.mediaUrl || item['多媒體連結'] || null;
      let mediaType = item.mediaType || item['多媒體類型'] || (mediaUrl ? 'image' : undefined);
      let explanation = item.explanation || item['詳解'] || null;
      let subQuestions = item.subQuestions || item['子問題'] || null;

      await addDoc(collection(db, 'questions'), {
        subject: subjectId,
        unit: parseInt(String(itemUnit)) || 1,
        difficulty: itemDiff,
        type: itemType,
        prompt: String(prompt).replace(/\\[SOURCE_IMAGE\\]/g, ''),
        options: options,
        correctAnswer: String(correctAnswer),
        clue: clue,
        mediaUrl,
        mediaType,
        explanation,
        subQuestions,
        createdAt: Date.now()
      } as Omit<Question, 'id'>);"""

content = content.replace(old_process, new_process)

with open("src/App.tsx", "w") as f:
    f.write(content)
