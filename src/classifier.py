import os
from openai import OpenAI

# 初始化 DeepSeek 客户端
# 这里的 DEEPSEEK_API_KEY 必须和你 GitHub Secrets 里填的名字一模一样
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"), 
    base_url="https://api.deepseek.com"
)

def classify(text):
    """
    使用 DeepSeek API 对视频标题和描述进行智能分类和简短摘要
    """
    if not text or len(text.strip()) < 5:
        return ["其他"]

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个AI资讯专家。请根据提供的视频标题和描述，从以下标签中选择最合适的1-2个：🔥热点、🤖机器人、🧠大模型、🇨🇳中国AI、🎓论文、💰融资。只需返回标签名称，用逗号隔开。"},
                {"role": "user", "content": f"内容如下：{text}"}
            ],
            max_tokens=50,
            temperature=0.3  # 低随机性，确保分类准确
        )
        # 获取 AI 返回的内容并按逗号分割成列表
        result = response.choices[0].message.content.strip()
        tags = [tag.strip() for tag in result.split(',') if tag.strip()]
        return tags if tags else ["🔥热点"]
        
    except Exception as e:
        print(f"DeepSeek 分类请求失败: {e}")
        # 如果接口报错（比如欠费或网络问题），降级回默认标签，确保程序不崩溃
        return ["🔥热点"]
