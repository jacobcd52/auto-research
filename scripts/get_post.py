"""Print the full plaintext of a LessWrong post: python3 scripts/get_post.py <postId> [max_chars]"""
import json, re, sys, html, urllib.request
pid = sys.argv[1]; n = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
q = '{ post(input:{selector:{_id:"%s"}}){result{title contents{html}}}}' % pid
req = urllib.request.Request("https://www.lesswrong.com/graphql", json.dumps({"query": q}).encode(),
                             {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
r = json.load(urllib.request.urlopen(req, timeout=90))["data"]["post"]["result"]
h = r["contents"]["html"]
h = re.sub(r'<a [^>]*href="([^"]*)"[^>]*>(.*?)</a>', r'\2 [\1]', h, flags=re.S)
t = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"</(p|h\d|li|div)>", "\n", h)))
print(r["title"]); print(re.sub(r"[ \t]+", " ", t)[:n])
