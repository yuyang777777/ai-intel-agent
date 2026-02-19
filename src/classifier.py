import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"), 
    base_url="https://api.deepseek.com"
)

def classify(text):
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个AI资讯专家。请将输入的视频标题和描述翻译成中文，并总结成一句话摘要。格式为：[标签] 中文标题：摘要内容"},
                {"role": "user", "content": f"请处理以下内容：{text}"}
            ],
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[热点] {text[:50]}..." # 报错后的降级处理
