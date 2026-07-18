import re

with open("src/App.tsx", "r") as f:
    content = f.read()

old_skill_str = """1. 題型 (Type)：必須混合產出以下三種題型：
   - 選擇題 (multiple_choice)：必須提供至少 4 個選項，並明確指出正確答案。
   - 填空題 (fill_in_the_blank)：題目中需使用底線（___）表示需填空的區域。不須提供選項，正確答案必須簡短、唯一且精確。
   - 閱讀題組 (question_group)：必須包含一段主文本（prompt）與數個子問題（subQuestions）。
2. 單元標註 (Unit)：請一次生成所有單元的題目，但必須在該題目的欄位中明確標註所屬「單元」（以數字表示，如 1, 2, 3）。
3. 難易度 (Difficulty)：每題需標註難度，分為：簡單 (easy)、中等 (medium)、困難 (hard)。難易度需平均分配。
4. 提示/詳解 (Clue)：為每題設計一句簡短的提示或詳解，協助學生思考。"""

new_skill_str = """1. 題型 (Type)：必須混合產出以下三種題型：
   - 選擇題 (multiple_choice)：必須提供至少 4 個選項，並明確指出正確答案。
   - 填空題 (fill_in_the_blank)：題目中需使用底線（___）表示需填空的區域。不須提供選項，正確答案必須簡短、唯一且精確。
   - 閱讀題組 (question_group)：必須包含一段主文本（prompt）與數個子問題（subQuestions）。
2. 多媒體題 (Multimedia)：若適合搭配圖片、影片或音訊，請在物件中提供 mediaUrl 與 mediaType。mediaType 可填寫 image, youtube, 或 audio。
3. 單元標註 (Unit)：請一次生成所有單元的題目，但必須在該題目的欄位中明確標註所屬「單元」（以數字表示，如 1, 2, 3）。
4. 難易度 (Difficulty)：每題需標註難度，分為：簡單 (easy)、中等 (medium)、困難 (hard)。難易度需平均分配。
5. 提示/詳解 (Clue)：為每題設計一句簡短的提示或詳解，協助學生思考。"""

content = content.replace(old_skill_str, new_skill_str)

old_json_str = """    "clue": "解題小提示",
    "subQuestions": [ // 若為閱讀題組 (question_group) 才需要此欄位"""

new_json_str = """    "clue": "解題小提示",
    "mediaUrl": "https://...", // 選填，若有多媒體題才提供
    "mediaType": "image", // 選填，若有多媒體題才提供 (image, youtube, audio)
    "subQuestions": [ // 若為閱讀題組 (question_group) 才需要此欄位"""

content = content.replace(old_json_str, new_json_str)

with open("src/App.tsx", "w") as f:
    f.write(content)
