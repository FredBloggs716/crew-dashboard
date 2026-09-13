# -*- coding: utf-8 -*-
"""Assemble LGH_Fleet_Manager_Terms_of_Reference_26-FM-001.docx"""
import os, shutil, zipfile
from lib_ooxml import *
import content as C
from style import *

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.join(OUT_DIR, "pkg")
XMLH = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'

MARK_RID = "rIdMark"


# ------------------------------------------------------------------ sectPr
def sect_pr():
    return (
        '<w:sectPr>'
        '<w:headerReference w:type="first" r:id="rIdHdrFirst"/>'
        '<w:footerReference w:type="first" r:id="rIdFtrFirst"/>'
        '<w:headerReference w:type="default" r:id="rIdHdr"/>'
        '<w:footerReference w:type="default" r:id="rIdFtr"/>'
        f'<w:pgSz w:w="{PAGE_W}" w:h="{PAGE_H}"/>'
        f'<w:pgMar w:top="{MARGIN}" w:right="{MARGIN}" w:bottom="{MARGIN}" '
        f'w:left="{MARGIN}" w:header="709" w:footer="624" w:gutter="0"/>'
        '<w:titlePg/>'
        '<w:docGrid w:linePitch="360"/>'
        '</w:sectPr>'
    )


def document():
    body = ''.join([
        C.cover(MARK_RID),
        C.contents(),
        C.part_one(),
        C.part_a(),
        C.part_b(),
        C.acceptance(),
        C.appendices(),
        sect_pr(),
    ])
    return XMLH + f'<w:document {NSDECL}><w:body>{body}</w:body></w:document>'


# ------------------------------------------------------------- header/footer
def header_default():
    p = para(
        run("LG HOWSON LTD", font=DISPLAY, sz=16, b=True, color=CRIMSON, spacing=70)
        + tab_run()
        + run(f"{C.DOC_TITLE}  ·  {C.DOC_SUB}", font=BODY, sz=16, color=MUTE),
        before=0, after=0, line=240, line_rule="exact",
        tabs=[("right", CONTENT_W)],
        borders={'bottom': (8, CRIMSON, 6)},
    )
    return XMLH + f'<w:hdr {NSDECL}>{p}</w:hdr>'


def footer_default():
    left = (run(C.DOC_REF, font=MONO, sz=15, color=MUTE)
            + run(f"  ·  v{C.DOC_VER}  ·  {C.DOC_STATE}  ·  {C.DOC_DATE}",
                  font=BODY, sz=15, color=MUTE))
    right = (run("Page ", font=BODY, sz=15, color=MUTE)
             + field("PAGE", font=BODY, sz=15, b=True, color=CRIMSON_DK)
             + run(" of ", font=BODY, sz=15, color=MUTE)
             + field("NUMPAGES", font=BODY, sz=15, b=True, color=CRIMSON_DK))
    p = para(left + tab_run() + right,
             before=0, after=0, line=240, line_rule="exact",
             tabs=[("right", CONTENT_W)],
             borders={'top': (4, LINE, 8)})
    return XMLH + f'<w:ftr {NSDECL}>{p}</w:ftr>'


def blank_hdr():
    return XMLH + f'<w:hdr {NSDECL}>{para(before=0, after=0, line=20, line_rule="exact")}</w:hdr>'


def blank_ftr():
    return XMLH + f'<w:ftr {NSDECL}>{para(before=0, after=0, line=20, line_rule="exact")}</w:ftr>'


# -------------------------------------------------------------------- styles
def styles():
    def hstyle(sid, name, sz, color, outline):
        return (
            f'<w:style w:type="paragraph" w:styleId="{sid}">'
            f'<w:name w:val="{name}"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/>'
            '<w:qFormat/>'
            '<w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="360" w:after="140"/>'
            f'<w:outlineLvl w:val="{outline}"/></w:pPr>'
            f'<w:rPr><w:rFonts w:ascii="{DISPLAY}" w:hAnsi="{DISPLAY}" w:cs="{DISPLAY}"/>'
            f'<w:b/><w:bCs/><w:color w:val="{color}"/>'
            f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr></w:style>'
        )

    return XMLH + f'''<w:styles {NSDECL}>
<w:docDefaults><w:rPrDefault><w:rPr>
<w:rFonts w:ascii="{BODY}" w:hAnsi="{BODY}" w:cs="{BODY}" w:eastAsia="{BODY}"/>
<w:color w:val="{STEEL}"/><w:sz w:val="20"/><w:szCs w:val="20"/>
<w:lang w:val="en-GB" w:eastAsia="en-GB" w:bidi="ar-SA"/>
</w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:widowControl/>
<w:spacing w:after="140" w:line="272" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>
{hstyle("Heading1", "heading 1", 26, INK, 0)}
{hstyle("Heading2", "heading 2", 21, CRIMSON_DK, 1)}
<w:style w:type="paragraph" w:styleId="Header"><w:name w:val="header"/><w:basedOn w:val="Normal"/>
<w:pPr><w:spacing w:after="0"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Footer"><w:name w:val="footer"/><w:basedOn w:val="Normal"/>
<w:pPr><w:spacing w:after="0"/></w:pPr></w:style>
<w:style w:type="table" w:default="1" w:styleId="TableNormal"><w:name w:val="Normal Table"/>
<w:tblPr><w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:left w:w="0" w:type="dxa"/>
<w:bottom w:w="0" w:type="dxa"/><w:right w:w="0" w:type="dxa"/></w:tblCellMar></w:tblPr></w:style>
<w:style w:type="numbering" w:default="1" w:styleId="NoList"><w:name w:val="No List"/></w:style>
</w:styles>'''


def settings():
    return XMLH + f'''<w:settings {NSDECL}>
<w:zoom w:percent="100"/>
<w:defaultTabStop w:val="624"/>
<w:characterSpacingControl w:val="doNotCompress"/>
<w:updateFields w:val="true"/>
<w:compat><w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat>
<w:themeFontLang w:val="en-GB"/>
</w:settings>'''


def font_table():
    def f(n, family="swiss", pitch="variable"):
        return (f'<w:font w:name="{n}"><w:family w:val="{family}"/>'
                f'<w:pitch w:val="{pitch}"/></w:font>')
    return XMLH + (f'<w:fonts {NSDECL}>{f(BODY)}{f(DISPLAY)}'
                   f'{f(MONO, "modern", "fixed")}{f("Arial")}{f("Calibri")}</w:fonts>')


def content_types():
    return XMLH + '''<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Default Extension="png" ContentType="image/png"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
<Override PartName="/word/fontTable.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.fontTable+xml"/>
<Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>
<Override PartName="/word/header2.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>
<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>
<Override PartName="/word/footer2.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>'''


def root_rels():
    return XMLH + '''<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>'''


def doc_rels():
    B = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    return XMLH + f'''<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rIdStyles" Type="{B}/styles" Target="styles.xml"/>
<Relationship Id="rIdSettings" Type="{B}/settings" Target="settings.xml"/>
<Relationship Id="rIdFonts" Type="{B}/fontTable" Target="fontTable.xml"/>
<Relationship Id="rIdHdr" Type="{B}/header" Target="header1.xml"/>
<Relationship Id="rIdHdrFirst" Type="{B}/header" Target="header2.xml"/>
<Relationship Id="rIdFtr" Type="{B}/footer" Target="footer1.xml"/>
<Relationship Id="rIdFtrFirst" Type="{B}/footer" Target="footer2.xml"/>
<Relationship Id="{MARK_RID}" Type="{B}/image" Target="media/lgh-mark.png"/>
</Relationships>'''


def core():
    return XMLH + f'''<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<dc:title>{C.DOC_TITLE} — {C.DOC_SUB}</dc:title>
<dc:subject>{C.DOC_REF} v{C.DOC_VER} {C.DOC_STATE}</dc:subject>
<dc:creator>LG Howson Ltd</dc:creator>
<cp:keywords>fleet; terms of reference; LG Howson; {C.DOC_REF}</cp:keywords>
<dc:description>Terms of Reference for the Fleet Manager and Mechanical Services role.</dc:description>
<cp:lastModifiedBy>LG Howson Ltd</cp:lastModifiedBy>
<cp:revision>2</cp:revision>
<cp:category>Governance</cp:category>
<dcterms:created xsi:type="dcterms:W3CDTF">2026-09-13T16:19:16Z</dcterms:created>
<dcterms:modified xsi:type="dcterms:W3CDTF">2026-09-13T16:19:16Z</dcterms:modified>
</cp:coreProperties>'''


def app():
    return XMLH + '''<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
<Application>Microsoft Office Word</Application><Company>LG Howson Ltd</Company>
<AppVersion>16.0000</AppVersion></Properties>'''


def main():
    if os.path.isdir(PKG):
        shutil.rmtree(PKG)
    files = {
        "[Content_Types].xml": content_types(),
        "_rels/.rels": root_rels(),
        "docProps/core.xml": core(),
        "docProps/app.xml": app(),
        "word/_rels/document.xml.rels": doc_rels(),
        "word/document.xml": document(),
        "word/styles.xml": styles(),
        "word/settings.xml": settings(),
        "word/fontTable.xml": font_table(),
        "word/header1.xml": header_default(),
        "word/header2.xml": blank_hdr(),
        "word/footer1.xml": footer_default(),
        "word/footer2.xml": blank_ftr(),
    }
    for path, data in files.items():
        full = os.path.join(PKG, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(data)
    os.makedirs(os.path.join(PKG, "word/media"), exist_ok=True)
    shutil.copy(os.path.join(OUT_DIR, "media/lgh-mark.png"),
                os.path.join(PKG, "word/media/lgh-mark.png"))

    out = os.path.join(OUT_DIR, "LGH_Fleet_Manager_Terms_of_Reference_26-FM-001.docx")
    if os.path.exists(out):
        os.remove(out)
    order = ["[Content_Types].xml", "_rels/.rels"] + [k for k in files if k not in
                                                      ("[Content_Types].xml", "_rels/.rels")]
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for path in order:
            z.write(os.path.join(PKG, path), path)
        z.write(os.path.join(PKG, "word/media/lgh-mark.png"), "word/media/lgh-mark.png")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
