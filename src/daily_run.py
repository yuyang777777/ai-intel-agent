# src/daily_run.py
import json
import os
from youtube_fetch import fetch_all
from scoring import total_score
from classifier import classify
from report_generator import build_sections, render_markdown
import requests

def run():
    with open("channels.json","r",encoding="utf-8") as f:
        channels = json.load(f)

    vids = fetch_all(channels)
    items = []
# ... 前面的代码保持不变 ...
    for v in vids:
        # 1. 组合标题和描述，发给 DeepSeek
        content_to_analyze = f"标题: {v.get('title','')} \n描述: {v.get('description','')[:100]}"
        
        # 2. 调用我们在 classifier.py 里改好的 AI 总结函数
        # 注意：现在 classify 函数会返回中文总结和标签
        ai_summary = classify(content_to_analyze) 
        
        # 3. 提取标签（假设 AI 返回格式是 "[标签] 总结内容"）
        # 这里简化处理：直接把 AI 总结后的中文存入 title
        items.append({
            "id": v.get("id"),
            "title": ai_summary, # 这里变成了全中文！
            "channel": v.get("channel"),
            "score": total_score(v),
            "categories": ["🔥热点"] # 简化分类逻辑，由 report_generator 处理
        })
# ... 后面的推送逻辑保持不变 ...

    sections = build_sections(items)
    md = render_markdown(sections)
    with open("daily_report.md","w",encoding="utf-8") as f:
        f.write(md)
    print("生成 daily_report.md 完成")

    # ===== Server酱 推送 =====
    sctkey = os.getenv("SCTKEY")
    if sctkey:
        url = f"https://sctapi.ftqq.com/{sctkey}.send"
        data = {
            "title": "每日 AI 情报",
            "desp": md
        }
        resp = requests.post(url, data=data)
        print("Server酱返回：", resp.status_code, resp.text)
    else:
        print("未设置 SCTKEY，跳过 Server酱推送")

if __name__ == "__main__":
    run()
