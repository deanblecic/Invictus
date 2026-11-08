# Brodski dnevnik SY INVICTUS

Put oko svijeta katamaranom SY INVICTUS, javljanje po javljanje.

- Knjiga koja se lista po danima: https://deanblecic.github.io/Invictus/
- Karta i cijeli dnevnik: https://deanblecic.github.io/Invictus/dnevnik.html

Izvorni tekstovi objava su u `data/tekstovi.json` (ključ "d.m hh:mm"). `scripts/sync.py <html s claude.ai>` iz dnevnika na claude.ai gradi `index.html` (knjiga, predložak `scripts/book.template.html`) i `dnevnik.html`.
