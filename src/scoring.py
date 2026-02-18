# src/scoring.py
import math
from datetime import datetime, timezone
from dateutil import parser

AI_KEYWORDS = {
    "大模型": 5, "AGI": 5, "LLM": 4, "GPT": 4, "Claude": 4, "Gemini": 4,
    "AI": 3, "人工智能": 3, "机器学习": 3, "模型": 2, "算法": 2, "数据": 1,
    "robot": 3, "机器人": 3, "humanoid": 3, "robotics":3
}

def hours_since(published_at):
    if not published_at:
        return 9999
    t = parser.isoparse(published_at)
    return (datetime.now(timezone.utc) - t).total_seconds()/3600.0

def heat_score(views=0, likes=0, comments=0):
    return views*0.0001 + likes*0.01 + comments*0.02

def ai_relevance(text):
    text = (text or "").lower()
    s = 0
    for k,w in AI_KEYWORDS.items():
        if k.lower() in text:
            s += w
    return s

def total_score(item):
    text = f"{item.get('title','')} {item.get('description','')}"
    ai_score = ai_relevance(text)
    heat = heat_score(item.get("views",0), item.get("likes",0), item.get("comments",0))
    hours = max(1.0, hours_since(item.get("published_at")))
    fresh = 1.0 / (hours/24.0 + 1.0)
    authority = 1.0
    if item.get("channel") in ["OpenAI","DeepMind","Two Minute Papers","Yannic Kilcher","Boston Dynamics"]:
        authority = 1.4
    final = ai_score*2.0 + heat + fresh*2.0 + authority*1.5
    return round(final, 3)
