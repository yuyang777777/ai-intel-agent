# src/classifier.py
CATEGORIES = {
    "🔥热视频评分": ["demo", "showcase", "发布", "体验", "实测"],
    "📈趋势变化跟踪": ["趋势", "增长", "用户", "数据", "stat", "trend"],
    "🤖机器人专项": ["robot", "机器人", "humanoid", "Boston Dynamics", "Figure"],
    "🧠大模型专项": ["llm", "gpt", "大模型", "模型", "llama", "gemini", "claude"],
    "🇨🇳中文区AI": ["中文","中国","清华","阿里","百度","腾讯","李沐","机器之心"],
    "🎓论文热点": ["paper", "arxiv", "research", "论文"],
    "💰融资动态": ["funding","融资","investment","raised","IPO"]
}

def classify(text):
    t = (text or "").lower()
    tags = []
    for cat, keys in CATEGORIES.items():
        for k in keys:
            if k.lower() in t:
                tags.append(cat)
                break
    if not tags:
        tags = ["🔥热视频评分"]
    return tags
