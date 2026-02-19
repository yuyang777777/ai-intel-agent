from collections import defaultdict

def build_sections(items):
    sections = defaultdict(list)
    for it in items:
        # 使用 AI 返回的标签，如果没有则归类到“综合热点”
        cats = it.get("categories", ["🔥 综合热点"])
        # 如果 cats 是字符串（AI 有时会返回字符串），转成列表
        if isinstance(cats, str): cats = [cats]
        
        for cat in cats:
            sections[cat].append(it)
    return sections

def render_markdown(sections):
    md = "# 🤖 AI & 机器人每日情报\n\n"
    md += "> 💡 本简报由 DeepSeek AI 自动翻译并根据热度评分生成\n\n"
    
    # 按照重要程度排序显示
    order = ["🧠大模型", "🤖机器人", "🇨🇳中国AI", "🔥热点", "🎓论文", "💰融资"]
    
    for sec in order:
        items = sections.get(sec, [])
        if not items:
            continue
        
        md += f"### {sec}\n"
        # 每个板块只取评分最高的前 5 条，避免信息过载
        sorted_items = sorted(items, key=lambda x: x.get("score", 0), reverse=True)[:5]
        
        for it in sorted_items:
            # 这里的 it['title'] 已经是我们在 daily_run 里处理过的中文摘要了
            md += f"🔹 {it['title']}\n"
            md += f"  - *来源: {it['channel']} | 热度评分: {it.get('score', 0)}*\n"
        md += "\n"
        
    md += "---\n*回复“更多”查看详细视频链接*"
    return md
