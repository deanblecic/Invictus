"""Iz HTML-a brodskog dnevnika s claude.ai gradi stranice za GitHub Pages:
  index.html   - knjiga koja se lista po danima (iz predloška scripts/book.template.html)
  dnevnik.html - karta i cijeli dnevnik na jednoj stranici
Upotreba: python3 scripts/sync.py <putanja-do-html-a-s-claude.ai>"""
import re, sys, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")

# --- dnevnik.html (cijela stranica s kartom) ---
if src.lstrip().lower().startswith("<!doctype"):
    full = src
else:
    head = ('<!doctype html>\n<html lang="hr">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<meta name="description" content="Brodski dnevnik SY INVICTUS: karta rute i sva javljanja.">\n'
            '<style>[hidden]{display:none!important}</style>\n')
    body = src[src.index('<title>'):] if '<title>' in src else src
    i = body.index('<div class="wrap">')
    full = head + body[:i] + '</head>\n<body>\n' + body[i:] + '\n</body>\n</html>\n'
    full = full.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
# poveznica natrag na knjigu
full = full.replace('<span class="sig">SY INVICTUS · Around the World</span>\n  <span>Sastavljeno',
                    '<span class="sig">SY INVICTUS · Around the World</span>\n  <a href="./" style="color:var(--track)">Otvori dnevnik kao knjigu ›</a>\n  <span>Sastavljeno', 1)
(root / "dnevnik.html").write_text(full, encoding="utf-8")

# --- index.html (knjiga) ---
def block(start, end):
    a = src.index(start)
    b = src.index(end, a) + len(end)
    return src[a:b]

data = "\n".join([
    block("const P={", "};"),
    *re.findall(r"^P\.\w+=\[[^\]]*\];", src, re.M),
    block("const LEGS=[", "\n];"),
    block("const E=[", "\n];"),
    block("const Q={", "\n};"),
])
m = re.search(r'<div class="stats">\s*(.*?)\s*</div>\s*</header>', src, re.S)
stats = m.group(1) if m else ""

tpl = (root / "scripts" / "book.template.html").read_text(encoding="utf-8")
out = tpl.replace("/*@DATA@*/", data).replace("<!--@STATS@-->", stats)
(root / "index.html").write_text(out, encoding="utf-8")
print("index.html (knjiga) i dnevnik.html ažurirani:", len(out), "+", len(full), "znakova")
