import json, hashlib, re, sys, pathlib

ROOT = pathlib.Path(__file__).parent
PREFIX = {"talk": "t", "feel": "f", "food": "s", "travel": "r", "errand": "e",
          "biz": "b", "email": "m", "phrasal": "p", "idiom": "i",
          "color": "c", "taste": "x"}

existing = json.loads((ROOT / "data/existing.json").read_text())
cards = []
for r in existing:
    id_, line, en, ans, ko, note, *rest = r + [None] * (7 - len(r))
    cards.append([id_, line, en, ans, ko, note, rest[0] or []])

problems = []
for line, pre in PREFIX.items():
    p = ROOT / f"data/{line}.txt"
    if not p.exists():
        continue
    for n, raw in enumerate(p.read_text().splitlines(), 1):
        if not raw.strip():
            continue
        parts = [x.strip() for x in raw.split(" | ")]
        parts = [x for x in parts if x != ""] if len(parts) > 4 else parts
        if len(parts) < 4:
            problems.append(f"{line}:{n} fields {raw}")
            continue
        en, ans, ko, note = parts[:4]
        if en.count("___") != 1:
            problems.append(f"{line}:{n} blank {en}")
            continue
        answers = [a.strip() for a in ans.split("/") if a.strip()]
        h = hashlib.sha1(en.lower().encode()).hexdigest()[:6]
        cards.append([pre + h, line, en, answers[0], ko, note, answers[1:]])

notes = {}
for f in sorted((ROOT / "data").glob("notes_*.txt")):
    for raw in f.read_text().splitlines():
        if " ||| " in raw:
            k, v = raw.split(" ||| ", 1)
            notes[k.strip()] = v.strip()
used = set()
for c in cards:
    if c[2] in notes:
        c[5] = notes[c[2]]; used.add(c[2])
for k in notes:
    if k not in used:
        problems.append("note not matched: " + k)

seen, out = {}, []
for c in cards:
    key = re.sub(r"\W+", " ", c[2].lower()).strip()
    if key in seen:
        problems.append(f"duplicate sentence: {c[2]}  ({seen[key]} / {c[0]})")
        continue
    seen[key] = c[0]
    out.append(c)
ids = [c[0] for c in out]
assert len(ids) == len(set(ids)), "id clash"

counts = {}
for c in out:
    counts[c[1]] = counts.get(c[1], 0) + 1
print("total", len(out), counts)
weak = [c for c in out if not re.search("[가-힣]", c[5]) or len(c[5]) < 14]
print("weak notes left", len(weak))
for c in weak: print("  WEAK", c[0], c[2], "|", c[5])
print("\n".join(problems) or "no problems")

tpl = (ROOT / "template.html").read_text()
js = json.dumps(out, ensure_ascii=False, separators=(",", ":"))
page = tpl.replace("/*@@CARDS@@*/", js)
# 1) Claude 아티팩트용 (머리말은 게시할 때 자동으로 붙어요)
(ROOT.parent / "toronto-talk.html").write_text(page.replace("/*@@HOSTED@@*/false", "false"))
# 2) GitHub Pages용: 완전한 HTML 문서 + 홈 화면 앱 설정
hosted = page.replace("/*@@HOSTED@@*/false", "true")
title_end = hosted.index("</title>") + len("</title>")
head = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Toronto Talk">
<meta name="theme-color" content="#eef2f5" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0e161d" media="(prefers-color-scheme: dark)">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="icon" type="image/png" href="icon-192.png">
"""
reset = "<style>html{-webkit-text-size-adjust:100%}:root{padding-top:calc(env(safe-area-inset-top,0px) + 48px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n"
rest = hosted[title_end:]
style_end = rest.index("</style>") + len("</style>")
doc = head + hosted[:title_end] + "\n" + reset + rest[:style_end] + "\n</head>\n<body>\n" + rest[style_end:] + "\n</body>\n</html>\n"
site = ROOT / "site"; site.mkdir(exist_ok=True)
(site / "index.html").write_text(doc)
