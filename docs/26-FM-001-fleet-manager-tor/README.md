# 26-FM-001 · Fleet Manager and Mechanical Services — Terms of Reference

LGH-branded rebuild of the Terms of Reference. **Wording is unchanged from v1.0** —
this is a presentation and branding pass only.

| File | Use |
|---|---|
| `LGH_Fleet_Manager_Terms_of_Reference_26-FM-001.docx` | Editable master (Word) |
| `LGH_Fleet_Manager_Terms_of_Reference_26-FM-001.pdf` | Issue copy, fonts embedded |

## Brand tokens

Taken from the crew dashboard (`index.html`) so print and screen match.

| Token | Value | Use |
|---|---|---|
| Crimson | `#B11722` | Rules, section numbers, table headers, part dividers |
| Crimson dark | `#8E1019` | Clause numbers, sub-headings, page numbers |
| Crimson tint | `#FBEAEB` | Outstanding fill-in fields |
| Crimson pale | `#FDF6F6` | Table banding, callouts |
| Ink | `#16191C` | Headings |
| Steel | `#23272B` | Body text |
| Mute | `#6B7177` | Header, footer, captions |
| Line | `#E4E7EA` | Table rules |

Type: **Archivo** (display/headings), **IBM Plex Sans** (body), **IBM Plex Mono**
(document reference). Install Archivo and IBM Plex Sans locally or Word will
substitute. The PDF has both embedded.

## Layout conventions

- A4, 22 mm margins. Unnumbered cover; running header and footer from page 2.
- Contents page uses `PAGEREF` fields — page numbers update themselves.
- Clause numbers sit in a 11 mm left gutter, hanging indent.
- Anything still to be agreed is shown in a tinted box: `[ name ]`, `£[    ]`.
- Part A / Part B open with a full-width crimson divider.

## Regenerating

Requires Python 3 only — the OOXML is written directly, no Word or LibreOffice.

```bash
cd src && python3 build.py
```

Edit `content.py` for wording, `style.py` for house style, `lib_ooxml.py` for
low-level XML. `src/media/lgh-mark.png` is the LGH mark used on the cover.

Optional checks (need LibreOffice and Poppler):

```bash
soffice --headless --convert-to pdf LGH_Fleet_Manager_Terms_of_Reference_26-FM-001.docx
pdftoppm -jpeg -r 72 *.pdf page
```
