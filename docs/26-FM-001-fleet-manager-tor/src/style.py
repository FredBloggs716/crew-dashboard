"""LG Howson document house style — composed components."""
from lib_ooxml import *

W = CONTENT_W          # 9412
GUTTER = 624           # clause-number gutter

BODY_KW = dict(font=BODY, sz=20, color=STEEL)
SMALL_KW = dict(font=BODY, sz=18, color=MUTE)

_bookmark_id = [100]


def bookmark(name, content):
    _bookmark_id[0] += 1
    i = _bookmark_id[0]
    return (f'<w:bookmarkStart w:id="{i}" w:name="{name}"/>{content}'
            f'<w:bookmarkEnd w:id="{i}"/>')


# ------------------------------------------------------------------ headings
def h1(number, title, anchor=None, page_break=False):
    """Numbered section heading: crimson numeral, ink title, hairline rule under."""
    content = ''
    if number:
        content += run(number, font=DISPLAY, sz=26, b=True, color=CRIMSON)
        content += tab_run(font=DISPLAY, sz=26, color=CRIMSON)
    content += run(title, font=DISPLAY, sz=26, b=True, color=INK)
    p = para(
        content,
        style="Heading1",
        keep_next=True, keep_lines=True, page_break=page_break,
        before=440, after=160, line=300, line_rule="exact",
        left=GUTTER, hanging=GUTTER,
        tabs=[("left", GUTTER)],
        borders={'bottom': (8, CRIMSON, 6)},
        outline=0,
    )
    return bookmark(anchor, p) if anchor else p


def h2(title):
    return para(
        run(title, font=DISPLAY, sz=21, b=True, color=CRIMSON_DK),
        style="Heading2", keep_next=True, keep_lines=True,
        before=320, after=120, line=280, line_rule="exact",
        left=GUTTER, outline=1,
    )


def appendix_h1(label, title, anchor=None):
    """Appendix opener: crimson eyebrow label above a large Archivo title."""
    out = [para(
        run(label.upper(), font=DISPLAY, sz=17, b=True, color=CRIMSON, spacing=60),
        page_break=True, keep_next=True, before=0, after=60,
        line=240, line_rule="exact",
    )]
    title_run = run(title, font=DISPLAY, sz=32, b=True, color=INK)
    if anchor:
        title_run = bookmark(anchor, title_run)
    out.append(para(
        title_run,
        keep_next=True, before=0, after=200, line=380, line_rule="exact",
        borders={'bottom': (8, CRIMSON, 8)}, outline=0,
    ))
    return ''.join(out)


# -------------------------------------------------------------------- clauses
def clause(number, text, after=140):
    """Hanging-indent clause: number sits in the left gutter."""
    content = run(number, font=BODY, sz=20, b=True, color=CRIMSON_DK)
    content += tab_run(font=BODY, sz=20)
    content += rich(text, BODY_KW)
    return para(content, before=0, after=after, line=272, line_rule="auto",
                left=GUTTER, hanging=GUTTER, tabs=[("left", GUTTER)])


def body(text, after=140, left=GUTTER, **over):
    kw = dict(BODY_KW)
    kw.update(over)
    return para(rich(text, kw), before=0, after=after, line=272, left=left)


def bullet(text, after=70, left=GUTTER + 340, lead="–"):
    content = run(lead, font=BODY, sz=20, b=True, color=CRIMSON)
    content += tab_run(font=BODY, sz=20)
    content += rich(text, BODY_KW)
    return para(content, before=0, after=after, line=268,
                left=left, hanging=280, tabs=[("left", left)])


# ---------------------------------------------------------------- part divider
def part_divider(kicker, title):
    """Full-width crimson band introducing Part A / Part B."""
    inner = para(
        run(kicker, font=DISPLAY, sz=17, b=True, color="F2B8B8", spacing=80),
        before=0, after=40, line=220, line_rule="exact",
    ) + para(
        run(title, font=DISPLAY, sz=27, b=True, color=WHITE, spacing=10),
        before=0, after=0, line=330, line_rule="exact",
    )
    return table(
        [row([cell(inner, W, shade=CRIMSON, valign="center",
                   margins=(200, 300, 210, 300))], height=1000)],
        [W],
        borders={'top': None, 'left': None, 'bottom': None, 'right': None,
                 'insideH': None, 'insideV': None},
    )


# ------------------------------------------------------------------- callout
def callout(text, label=None, tone="crimson"):
    fill, bar, txt = {
        "crimson": (CRIMSON_PALE, CRIMSON, STEEL),
        "grey": (BG, "C2C6CA", STEEL),
    }[tone]
    inner = ''
    if label:
        inner += para(
            run(label.upper(), font=DISPLAY, sz=16, b=True, color=CRIMSON, spacing=60),
            before=0, after=60, line=200, line_rule="exact",
        )
    inner += para(rich(text, dict(font=BODY, sz=19, color=txt)),
                  before=0, after=0, line=264)
    return table(
        [row([cell(inner, W, shade=fill, valign="center",
                   borders={'left': (24, bar)},
                   margins=(170, 260, 170, 260))])],
        [W],
        borders={'top': None, 'left': (24, bar), 'bottom': None, 'right': None,
                 'insideH': None, 'insideV': None},
    )


# -------------------------------------------------------------------- tables
def tcell_text(text, sz=19, b=False, color=STEEL, font=BODY, jc=None):
    return para(rich(text, dict(font=font, sz=sz, b=b, color=color)),
                before=40, after=40, line=256, jc=jc)


def data_table(headers, rows_data, widths, aligns=None, min_height=None):
    """Crimson header row, hairline separators, alternating pale bands."""
    aligns = aligns or [None] * len(widths)
    rs = [row([
        cell(tcell_text(h, sz=17, b=True, color=WHITE, font=DISPLAY, jc=aligns[i]),
             widths[i], shade=CRIMSON, margins=(110, 150, 110, 150))
        for i, h in enumerate(headers)
    ], header=True)]
    for n, r in enumerate(rows_data):
        shade = CRIMSON_PALE if n % 2 else None
        rs.append(row([
            cell(tcell_text(c, b=(i == 0 and len(widths) > 2), color=(INK if i == 0 and len(widths) > 2 else STEEL),
                            jc=aligns[i]),
                 widths[i], shade=shade, margins=(110, 150, 110, 150))
            for i, c in enumerate(r)
        ], height=min_height))
    return table(rs, widths, borders={
        'top': None, 'left': None, 'bottom': (4, LINE),
        'insideH': (4, LINE_SOFT), 'insideV': None,
    })


def field_table(pairs, label_w=3100, indent=0, total=None):
    """Two-column label/value: tinted bold label column, value column open."""
    total = total or W - indent
    value_w = total - label_w
    rs = []
    for i, (k, v) in enumerate(pairs):
        rs.append(row([
            cell(tcell_text(k, b=True, color=INK), label_w, shade=CRIMSON_PALE,
                 margins=(110, 150, 110, 150)),
            cell(tcell_text(v), value_w, margins=(110, 150, 110, 150)),
        ]))
    return table(rs, [label_w, value_w], indent=indent, borders={
        'top': (4, LINE), 'left': None, 'bottom': (4, LINE), 'right': None,
        'insideH': (4, LINE_SOFT), 'insideV': (4, LINE_SOFT),
    })


def signature_block(heading, pairs):
    out = para(
        run(heading, font=DISPLAY, sz=19, b=True, color=CRIMSON_DK),
        before=0, after=100, line=260, left=GUTTER,
    )
    label_w = 2600
    value_w = W - GUTTER - label_w
    rs = []
    for k in pairs:
        rs.append(row([
            cell(tcell_text(k, b=True, color=INK), label_w, shade=CRIMSON_PALE,
                 margins=(150, 150, 150, 150)),
            cell(para(after=0), value_w, margins=(150, 150, 150, 150)),
        ], height=740))
    out += table(rs, [label_w, value_w], indent=GUTTER, borders={
        'top': (4, "C2C6CA"), 'left': (4, "C2C6CA"), 'bottom': (4, "C2C6CA"),
        'right': (4, "C2C6CA"), 'insideH': (4, LINE), 'insideV': (4, "C2C6CA"),
    })
    return out


# ------------------------------------------------------------------ contents
def toc_entry(label, target, indent=0, bold=False):
    content = run(label, font=BODY, sz=20, b=bold, color=(INK if bold else STEEL))
    content += tab_run(font=BODY, sz=20, color=MUTE)
    content += (f'<w:r>{rpr(font=BODY, sz=19, color=CRIMSON_DK, b=True)}'
                '<w:fldChar w:fldCharType="begin"/></w:r>'
                f'<w:r>{rpr(font=BODY, sz=19, color=CRIMSON_DK, b=True)}'
                f'<w:instrText xml:space="preserve"> PAGEREF {target} \\h </w:instrText></w:r>'
                f'<w:r>{rpr(font=BODY, sz=19, color=CRIMSON_DK, b=True)}'
                '<w:fldChar w:fldCharType="separate"/></w:r>'
                f'<w:r>{rpr(font=BODY, sz=19, color=CRIMSON_DK, b=True)}<w:t>0</w:t></w:r>'
                f'<w:r>{rpr(font=BODY, sz=19, color=CRIMSON_DK, b=True)}'
                '<w:fldChar w:fldCharType="end"/></w:r>')
    return para(content, before=0, after=90, line=264,
                left=indent, tabs=[("right", W, "dot")])
