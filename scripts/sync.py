"""Pretvara HTML brodskog dnevnika s claude.ai u samostalnu index.html za GitHub Pages.
Upotreba: python3 scripts/sync.py <putanja-do-html-a-s-claude.ai>"""
import sys, pathlib
src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
if src.lstrip().lower().startswith("<!doctype"):
    doc = src  # već je cijeli dokument
else:
    head = ('<!doctype html>\n<html lang="hr">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<meta name="description" content="Brodski dnevnik SY INVICTUS: put oko svijeta katamaranom.">\n'
            '<style>[hidden]{display:none!important}</style>\n')
    i = src.index('<div class="wrap">')
    doc = head + src[:i] + '</head>\n<body>\n' + src[i:] + '\n</body>\n</html>\n'
    doc = doc.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
out = pathlib.Path(__file__).resolve().parent.parent / "index.html"
out.write_text(doc, encoding="utf-8")
print("index.html ažuriran,", len(doc), "znakova")
