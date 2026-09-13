"""Minimal OOXML WordprocessingML builder for the LG Howson document house style."""
import re
from xml.sax.saxutils import escape

# ---------------------------------------------------------------- brand tokens
CRIMSON      = "B11722"
CRIMSON_DK   = "8E1019"
CRIMSON_TINT = "FBEAEB"
CRIMSON_PALE = "FDF6F6"
INK          = "16191C"
STEEL        = "23272B"
MUTE         = "6B7177"
LINE         = "E4E7EA"
LINE_SOFT    = "EEF0F2"
BG           = "F4F6F8"
WHITE        = "FFFFFF"

DISPLAY = "Archivo"
BODY    = "IBM Plex Sans"
MONO    = "IBM Plex Mono"

# ------------------------------------------------------------------- geometry
PAGE_W, PAGE_H = 11906, 16838          # A4 in twips
MARGIN         = 1247                   # 22 mm
CONTENT_W      = PAGE_W - 2 * MARGIN    # 9412


def esc(t):
    return escape(str(t))


# ------------------------------------------------------------------ run props
def rpr(font=BODY, sz=20, b=False, color=STEEL, caps=False, spacing=None,
        italic=False, shade=None, underline=False, line_through=False):
    """Emit <w:rPr> in schema order."""
    p = ['<w:rPr>']
    if font:
        p.append(f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:cs="{font}" w:eastAsia="{font}"/>')
    if b:
        p.append('<w:b/><w:bCs/>')
    if italic:
        p.append('<w:i/><w:iCs/>')
    if caps:
        p.append('<w:caps/>')
    if line_through:
        p.append('<w:strike/>')
    if color:
        p.append(f'<w:color w:val="{color}"/>')
    if spacing is not None:
        p.append(f'<w:spacing w:val="{spacing}"/>')
    if sz:
        p.append(f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>')
    if underline:
        p.append('<w:u w:val="single"/>')
    if shade:
        p.append(f'<w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>')
    p.append('</w:rPr>')
    return ''.join(p)


def run(text, **kw):
    return f'<w:r>{rpr(**kw)}<w:t xml:space="preserve">{esc(text)}</w:t></w:r>'


def tab_run(**kw):
    return f'<w:r>{rpr(**kw)}<w:tab/></w:r>'


def brk():
    return '<w:r><w:br/></w:r>'


# --------------------------------------------------------- inline mini-markup
FIELD_RE = re.compile(r'(\[[^\[\]]*\]|\*\*[^*]+\*\*)')


def rich(text, base=None):
    """Parse **bold** and [ fill-in fields ] into styled runs."""
    base = dict(base or {})
    out = []
    for part in FIELD_RE.split(text):
        if not part:
            continue
        if part.startswith('**') and part.endswith('**'):
            kw = dict(base)
            kw['b'] = True
            kw['color'] = INK
            out.append(run(part[2:-2], **kw))
        elif part.startswith('[') and part.endswith(']'):
            kw = dict(base)
            kw['color'] = CRIMSON_DK
            kw['shade'] = CRIMSON_TINT
            kw['b'] = True
            out.append(run(part, **kw))
        else:
            out.append(run(part, **base))
    return ''.join(out)


# ----------------------------------------------------------- paragraph props
def ppr(style=None, before=None, after=None, line=None, line_rule=None,
        left=None, hanging=None, right=None, jc=None, tabs=None, borders=None,
        shade=None, keep_next=False, keep_lines=False, page_break=False,
        outline=None, num=None, contextual=False):
    p = ['<w:pPr>']
    if style:
        p.append(f'<w:pStyle w:val="{style}"/>')
    if keep_next:
        p.append('<w:keepNext/>')
    if keep_lines:
        p.append('<w:keepLines/>')
    if page_break:
        p.append('<w:pageBreakBefore/>')
    if num:
        p.append(f'<w:numPr><w:ilvl w:val="{num[1]}"/><w:numId w:val="{num[0]}"/></w:numPr>')
    if borders:
        p.append('<w:pBdr>')
        for side in ('top', 'left', 'bottom', 'right'):
            if side in borders:
                sz, col, space = borders[side]
                p.append(f'<w:{side} w:val="single" w:sz="{sz}" w:space="{space}" w:color="{col}"/>')
        p.append('</w:pBdr>')
    if shade:
        p.append(f'<w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>')
    if tabs:
        p.append('<w:tabs>')
        for t in tabs:
            leader = f' w:leader="{t[2]}"' if len(t) > 2 and t[2] else ''
            p.append(f'<w:tab w:val="{t[0]}" w:pos="{t[1]}"{leader}/>')
        p.append('</w:tabs>')
    sp = []
    if before is not None:
        sp.append(f'w:before="{before}"')
    if after is not None:
        sp.append(f'w:after="{after}"')
    if line is not None:
        sp.append(f'w:line="{line}"')
        sp.append(f'w:lineRule="{line_rule or "auto"}"')
    if sp:
        p.append(f'<w:spacing {" ".join(sp)}/>')
    ind = []
    if left is not None:
        ind.append(f'w:left="{left}"')
    if right is not None:
        ind.append(f'w:right="{right}"')
    if hanging is not None:
        ind.append(f'w:hanging="{hanging}"')
    if ind:
        p.append(f'<w:ind {" ".join(ind)}/>')
    if contextual:
        p.append('<w:contextualSpacing/>')
    if jc:
        p.append(f'<w:jc w:val="{jc}"/>')
    if outline is not None:
        p.append(f'<w:outlineLvl w:val="{outline}"/>')
    p.append('</w:pPr>')
    return ''.join(p)


def para(content='', **kw):
    return f'<w:p>{ppr(**kw)}{content}</w:p>'


def spacer(h=120):
    return para(after=0, before=0, line=h, line_rule="exact")


# ------------------------------------------------------------------- tables
def cell(content, w, shade=None, borders=None, valign="center", span=None,
         margins=(90, 130, 90, 130)):
    p = ['<w:tc><w:tcPr>', f'<w:tcW w:type="dxa" w:w="{w}"/>']
    if span:
        p.append(f'<w:gridSpan w:val="{span}"/>')
    if borders:
        p.append('<w:tcBorders>')
        for side in ('top', 'left', 'bottom', 'right'):
            if side in borders:
                b = borders[side]
                if b is None:
                    p.append(f'<w:{side} w:val="nil"/>')
                else:
                    sz, col = b
                    p.append(f'<w:{side} w:val="single" w:sz="{sz}" w:color="{col}"/>')
        p.append('</w:tcBorders>')
    if shade:
        p.append(f'<w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>')
    t, l, b_, r = margins
    p.append(f'<w:tcMar><w:top w:type="dxa" w:w="{t}"/><w:left w:type="dxa" w:w="{l}"/>'
             f'<w:bottom w:type="dxa" w:w="{b_}"/><w:right w:type="dxa" w:w="{r}"/></w:tcMar>')
    p.append(f'<w:vAlign w:val="{valign}"/>')
    p.append('</w:tcPr>')
    p.append(content or para(after=0))
    p.append('</w:tc>')
    return ''.join(p)


def row(cells, header=False, height=None, cant_split=True):
    p = ['<w:tr><w:trPr>']
    if height:
        p.append(f'<w:trHeight w:val="{height}" w:hRule="atLeast"/>')
    if cant_split:
        p.append('<w:cantSplit/>')
    if header:
        p.append('<w:tblHeader/>')
    p.append('</w:trPr>')
    p.append(''.join(cells))
    p.append('</w:tr>')
    return ''.join(p)


def table(rows, widths, borders=None, indent=0):
    borders = borders if borders is not None else {
        'top': (4, LINE), 'bottom': (4, LINE),
        'insideH': (4, LINE_SOFT), 'left': None, 'right': None, 'insideV': None,
    }
    p = ['<w:tbl><w:tblPr>', f'<w:tblW w:type="dxa" w:w="{sum(widths)}"/>']
    if indent:
        p.append(f'<w:tblInd w:type="dxa" w:w="{indent}"/>')
    p.append('<w:tblBorders>')
    for side in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        b = borders.get(side, None)
        if b is None:
            p.append(f'<w:{side} w:val="nil"/>')
        else:
            sz, col = b
            p.append(f'<w:{side} w:val="single" w:sz="{sz}" w:color="{col}"/>')
    p.append('</w:tblBorders>')
    p.append('<w:tblLayout w:type="fixed"/>')
    p.append('<w:tblCellMar><w:top w:type="dxa" w:w="0"/><w:left w:type="dxa" w:w="0"/>'
             '<w:bottom w:type="dxa" w:w="0"/><w:right w:type="dxa" w:w="0"/></w:tblCellMar>')
    p.append('<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" '
             'w:lastColumn="0" w:noHBand="0" w:noVBand="1"/>')
    p.append('</w:tblPr><w:tblGrid>')
    for w in widths:
        p.append(f'<w:gridCol w:w="{w}"/>')
    p.append('</w:tblGrid>')
    p.append(''.join(rows))
    p.append('</w:tbl>')
    return ''.join(p)


# --------------------------------------------------------------------- image
def image(rel_id, cx, cy, name="image"):
    return (
        '<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0">'
        f'<wp:extent cx="{cx}" cy="{cy}"/>'
        '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        f'<wp:docPr id="1" name="{name}"/>'
        '<wp:cNvGraphicFramePr><a:graphicFrameLocks '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>'
        '</wp:cNvGraphicFramePr>'
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<pic:nvPicPr><pic:cNvPr id="1" name="{name}"/><pic:cNvPicPr/></pic:nvPicPr>'
        f'<pic:blipFill><a:blip r:embed="{rel_id}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        '<pic:spPr><a:xfrm><a:off x="0" y="0"/>'
        f'<a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
        '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r>'
    )


# --------------------------------------------------------------------- fields
def field(instr, **kw):
    r = rpr(**kw)
    return (f'<w:r>{r}<w:fldChar w:fldCharType="begin"/></w:r>'
            f'<w:r>{r}<w:instrText xml:space="preserve"> {instr} </w:instrText></w:r>'
            f'<w:r>{r}<w:fldChar w:fldCharType="separate"/></w:r>'
            f'<w:r>{r}<w:t>1</w:t></w:r>'
            f'<w:r>{r}<w:fldChar w:fldCharType="end"/></w:r>')


NSDECL = (
    'xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" '
    'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
    'xmlns:o="urn:schemas-microsoft-com:office:office" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
    'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
    'xmlns:v="urn:schemas-microsoft-com:vml" '
    'xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" '
    'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
    'xmlns:w10="urn:schemas-microsoft-com:office:word" '
    'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
    'xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml" '
    'xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" '
    'xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" '
    'xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" '
    'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" '
    'mc:Ignorable="w14 w15 wp14"'
)
