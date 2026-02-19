import os
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
    
    all_items_with_links = [] # 用于最后汇总所有链接

    for sec in order:
        items = sections.get(sec, [])
        if not items:
            continue
        
        md += f"### {sec}\n"
        # 每个板块只取评分最高的前 5 条
        sorted_items = sorted(items, key=lambda x: x.get("score", 0), reverse=True)[:5]
        
        for it in sorted_items:
            # 获取视频 ID 拼接链接
            video_url = f"https://www.youtube.com/watch?v={it.get('id')}"
            
            # 这里的 it['title'] 是 AI 处理后的中文
            md += f"🔹 {it['title']}\n"
            # 在来源后面直接加上 [🔗 查看视频] 链接
            md += f"  - *来源: {it['channel']} | 评分: {it.get('score', 0)} | [📺 观看视频]({video_url})*\n"
            
            all_items_with_links.append(it)
        md += "\n"
    
    # 修改底部栏，既然无法真的“回复”，我们就把功能直接做在页面上
    md += "---\n"
    md += "#### 📌 更多操作\n"
    md += f"- [查看完整视频列表(共{len(all_items_with_links)}条)]({os.getenv('GITHUB_SERVER_URL', 'https://github.com')}/{os.getenv('GITHUB_REPOSITORY', '')}/actions)\n"
    md += "- 💡 提示：点击蓝色文字即可直接跳转 YouTube"
    
    return md
