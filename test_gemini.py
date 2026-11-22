
import os
from google import genai
from google.genai import errors

key = os.getenv("GEMINI_API_KEY")
if not key:
    raise RuntimeError("找不到 GEMINI_API_KEY")

client = genai.Client(api_key=key)

print("正在查詢可用模型...", flush=True)

models = []
for item in client.models.list():
    name = item.name.replace("models/", "")
    methods = item.supported_actions or []
    if "generateContent" in methods and "flash" in name.lower():
        models.append(name)

print("找到的 Flash 模型：", models, flush=True)

if not models:
    raise RuntimeError("找不到可用的 Flash 模型")

for name in models:
    print("測試模型：", name, flush=True)
    try:
        response = client.models.generate_content(
            model=name,
            contents="請只回答：測試成功"
        )
        if response.text:
            print("SUCCESS_MODEL:", name, flush=True)
            print("回覆：", response.text, flush=True)
            break
    except errors.APIError as e:
        print("模型失敗：", name, "錯誤：", e.code, flush=True)
else:
    raise RuntimeError("所有候選模型均無法成功回覆")
