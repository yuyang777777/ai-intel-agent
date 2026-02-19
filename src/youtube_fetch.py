# src/youtube_fetch.py
import os
import requests
from datetime import datetime, timedelta, timezone

YOUTUBE_KEY = os.getenv("YOUTUBE_API_KEY")
SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"

def iso_24h_ago():
    t = datetime.now(timezone.utc) - timedelta(hours=24)
    return t.isoformat()

def fetch_videos_for_query(query, max_results=50):
    params = {
        "key": YOUTUBE_KEY,
        "part": "snippet",
        "q": query,
        "order": "date",
        "publishedAfter": iso_24h_ago(),
        "type": "video",
        "maxResults": max_results
    }
    r = requests.get(SEARCH_URL, params=params).json()
    items = r.get("items", [])
    vids = []
    ids = [it["id"]["videoId"] for it in items if it["id"].get("videoId")]
    if not ids:
        return vids

    params2 = {
        "key": YOUTUBE_KEY,
        "part": "snippet,statistics,contentDetails",
        "id": ",".join(ids)
    }
    r2 = requests.get(VIDEO_URL, params=params2).json()
    for it in r2.get("items", []):
        snippet = it["snippet"]
        stats = it.get("statistics", {})
        vids.append({
            "id": it["id"],
            "title": snippet.get("title",""),
            "description": snippet.get("description",""),
            "channel": snippet.get("channelTitle",""),
            "published_at": snippet.get("publishedAt"),
            "views": int(stats.get("viewCount", 0)),
            "likes": int(stats.get("likeCount", 0)) if stats.get("likeCount") else 0,
            "comments": int(stats.get("commentCount", 0)) if stats.get("commentCount") else 0,
            "duration": it.get("contentDetails", {}).get("duration", "")
        })
    return vids

def fetch_all(channels_or_queries):
    allv = []
    for q in channels_or_queries:
        try:
            v = fetch_videos_for_query(q)
            allv.extend(v)
        except Exception as e:
            print("fetch error for", q, e)
    seen = set()
    uniq = []
    for it in allv:
        vid = it.get("id") or it.get("id", {}).get("videoId")
        if vid not in seen:
            seen.add(vid)
            uniq.append(it)
    return uniq
