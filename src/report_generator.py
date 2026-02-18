# src/report_generator.py
from collections import defaultdict

def build_sections(items):
    sections = defaultdict(list)
    for it in items:
        for cat in it.get("categories", ["🔥热视频评分"]):
            sections[cat].append(it)
        if it.get("score",0) >= 15:
            sections["📈趋势变化跟踪"].append(it)
    return sections

def render_markdown(sections):
    md = "# 🤖 AI情报日报\n\n"
    for sec in ["🔥热视频评分","📈趋势变化跟踪","🤖机器人专项","🧠大模型专项","🇨🇳中文区AI","🎓论文热点","💰融资动态"]:
        items = sections.get(sec, [])
        if not items:
            continue
        md += f"## {sec}\n"
        for it in sorted(items, key=lambda x: x["score"], reverse=True)[:10]:
            md += f"- **{it['title']}** | {it['channel']} | ⭐{it['score']} | 👀{it['views']} | {it['published_at']}\n"
        md += "\n"
    return md
