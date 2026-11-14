"""Fetch all LessWrong posts from the last year with baseScore >= 50."""
import json, sys, time, urllib.request

URL = "https://www.lesswrong.com/graphql"
AFTER, MIN_KARMA, PAGE = "2025-11-14", 50, 100
Q = """{ posts(input:{terms:{view:"top",limit:%d,offset:%d,after:"%s",karmaThreshold:%d}}){results{
_id title baseScore postedAt slug wordCount commentCount
user{displayName} coauthors{displayName}
tags{name} contents{plaintextDescription}}}}"""

def page(offset):
    body = json.dumps({"query": Q % (PAGE, offset, AFTER, MIN_KARMA)}).encode()
    req = urllib.request.Request(URL, body, {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
    for attempt in range(4):
        try:
            return json.load(urllib.request.urlopen(req, timeout=90))["data"]["posts"]["results"]
        except Exception as e:
            print("retry", offset, e, file=sys.stderr); time.sleep(2 ** attempt * 2)
    raise SystemExit(f"failed at offset {offset}")

out, offset = [], 0
while True:
    rs = page(offset)
    out += rs
    print(offset, len(rs), file=sys.stderr)
    if len(rs) < PAGE: break
    offset += PAGE
seen, posts = set(), []
for p in out:
    if p["_id"] in seen or (p["baseScore"] or 0) < MIN_KARMA: continue
    seen.add(p["_id"])
    posts.append({
        "id": p["_id"], "title": p["title"], "karma": p["baseScore"], "date": p["postedAt"][:10],
        "url": f"https://www.lesswrong.com/posts/{p['_id']}/{p['slug']}",
        "authors": [a["displayName"] for a in [p.get("user")] + (p.get("coauthors") or []) if a],
        "tags": [t["name"] for t in p.get("tags") or []],
        "words": p.get("wordCount"), "comments": p.get("commentCount"),
        "excerpt": ((p.get("contents") or {}).get("plaintextDescription") or "")[:1500],
    })
json.dump(posts, open(sys.argv[1], "w"), indent=1)
print(len(posts), "posts", file=sys.stderr)
