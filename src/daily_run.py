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
    # 在 daily_run.py 的循环里改这一段
for v in vids:
    raw_content = v.get("title","") + " " + v.get("description","")
    # 调用我们改好的 AI 总结函数
    ai_summary = classify(raw_content) 
    
    items.append({
        "title": ai_summary, # 这里直接用 AI 总结后的中文
        "channel": v.get("channel"),
        "score": total_score(v),
        "url": f"https://www.youtube.com/watch?v={v.get('id')}"
    })

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
