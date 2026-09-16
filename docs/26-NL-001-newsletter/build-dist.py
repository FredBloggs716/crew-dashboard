#!/usr/bin/env python3
"""Build the standalone, offline copy of the Site Report.

`newsletter.html` is written for the Artifact platform, which wraps it in a
document skeleton (charset, viewport, a small reset) and serves `assets/`
alongside it. A file someone downloads gets neither, so this script produces a
genuinely self-contained page:

  * wraps the fragment in a real HTML document with an explicit UTF-8 charset
    (without it browsers read the em-dashes as Latin-1 and you get mojibake)
  * re-creates the reset the platform would have provided
  * inlines every image as a data URI, downscaled and re-encoded first
  * inlines the brand typefaces as WOFF2 data URIs, so the page needs no
    network at all — Google Fonts is unreachable from some networks and the
    fallback ruins a branded document
  * adds print rules and A4 paper, so "Save as PDF" lays out properly

Usage:  python3 build-dist.py          (then optionally print to PDF, see README)
"""
import base64
import io
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).parent
ASSETS = HERE / "assets"
DIST = HERE / "dist"
SRC = HERE / "newsletter.html"
OUT = DIST / "LGH-Site-Report-Issue-01.html"

# name -> (max width px, encode as)
IMAGES = {
    "lgh-mark.png": (165, "png"),
    "logo-primary.png": (354, "png"),
    "aerial-site.jpg": (1700, "jpg"),
    "site-foundations-wide.jpg": (1600, "jpg"),
    "fleet-row.jpg": (1700, "jpg"),
    "timbertoft-drawing.png": (2000, "jpg"),
}

FONT_CSS = (
    "https://fonts.googleapis.com/css2"
    "?family=Archivo:wght@700;800"
    "&family=IBM+Plex+Sans:wght@400;600;700"
    "&family=IBM+Plex+Mono:wght@600&display=swap"
)
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# The reset the Artifact platform injects, which a downloaded file must carry.
RESET = """
  :root{color-scheme:light dark}
  body{margin:0}
  img{max-width:100%}
  [hidden]{display:none!important}
"""

PRINT = """
  @page{size:A4;margin:12mm 10mm}
  @media print{
    body{background:#fff}
    .masthead,.hero,footer,.stat,.job,.kit-item,.pools{-webkit-print-color-adjust:exact;print-color-adjust:exact}
    /* object-fit is unreliable in Chromium's print path — let the hero run at
       its natural ratio instead of being cropped into a fixed-ratio box */
    .hero figure{aspect-ratio:auto;max-height:none;height:auto}
    .hero figure img{height:auto;object-fit:fill}
    .job,.kit-item,.lrow,.pools,.drawing,.band-photo,.stats{break-inside:avoid}
    /* overflow:hidden makes these unfragmentable, which strands half-pages of
       white space — let the ledger break between its rows instead */
    .ledger{overflow:visible}
    .sec-head{break-after:avoid}
    section{padding-block:26px 0}
  }
"""


def fetch(url, ua=False):
    cmd = ["curl", "-sS", "--fail"]
    if ua:
        cmd += ["-A", UA]
    return subprocess.run(cmd + [url], capture_output=True, check=True).stdout


def inline_images(html):
    from PIL import Image
    for name, (maxw, mode) in IMAGES.items():
        im = Image.open(ASSETS / name)
        if im.width > maxw:
            im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
        buf = io.BytesIO()
        if mode == "jpg":
            im.convert("RGB").save(buf, "JPEG", quality=82, optimize=True, progressive=True)
            mime = "image/jpeg"
        else:
            im.save(buf, "PNG", optimize=True)
            mime = "image/png"
        data = buf.getvalue()
        uri = f"data:{mime};base64,{base64.b64encode(data).decode()}"
        before = html
        html = html.replace(f'src="assets/{name}"', f'src="{uri}"')
        if html == before:
            sys.exit(f"image referenced nowhere in the page: {name}")
        print(f"  {name:26} {(ASSETS/name).stat().st_size/1024:7.0f} KB -> {len(data)/1024:6.0f} KB")
    return html


def font_faces():
    css = fetch(FONT_CSS, ua=True).decode()
    blocks = re.findall(r"/\*\s*([\w\-\[\]]+)\s*\*/\s*(@font-face\s*\{[^}]*\})", css)
    cache, faces = {}, []
    for subset, blk in blocks:
        if subset != "latin":          # latin only keeps this ~95 KB rather than ~1 MB
            continue
        fam = re.search(r"font-family:\s*'([^']+)'", blk).group(1)
        weight = re.search(r"font-weight:\s*(\d+)", blk).group(1)
        url = re.search(r"url\((https[^)]+\.woff2)\)", blk).group(1)
        cache.setdefault(url, fetch(url))
        b64 = base64.b64encode(cache[url]).decode()
        faces.append(
            f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{weight};"
            f"font-display:swap;src:url(data:font/woff2;base64,{b64}) format('woff2')}}"
        )
    if not faces:
        sys.exit("no latin @font-face blocks found — Google Fonts CSS format changed?")
    print(f"  fonts: {len(faces)} faces from {len(cache)} files, "
          f"{sum(len(v) for v in cache.values())/1024:.0f} KB")
    return "\n".join(faces)


def main():
    html = SRC.read_text()
    title = re.search(r"<title>(.*?)</title>", html).group(1)

    print("images:")
    html = inline_images(html)
    print("typefaces:")
    faces = font_faces()

    # strip the network font links; everything must be embedded
    html = re.sub(r'<link rel="preconnect"[^>]*>\s*', "", html)
    html = re.sub(r'<link href="https://fonts\.googleapis\.com[^>]*>\s*', "", html)

    html = html.replace("<style>", "<style>\n" + RESET + "\n/* brand typefaces */\n" + faces + "\n", 1)
    html = html.replace("</style>", PRINT + "</style>", 1)

    doc = ('<!doctype html>\n<html lang="en-GB">\n<head>\n'
           '<meta charset="UTF-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
           f"{html}\n</head>\n<body>\n</body>\n</html>\n")
    # newsletter.html carries its own <title> and <style> then body markup; the
    # browser moves the stray body content out of <head> on its own, but be tidy:
    doc = doc.replace("</head>\n<body>\n</body>\n</html>", "</body>\n</html>")
    doc = doc.replace("<header class=", "</head>\n<body>\n<header class=", 1)

    leaks = [u for u in re.findall(r"https?://[^\s\"')]+", doc) if "claude.ai" not in u]
    if leaks:
        sys.exit(f"page still reaches the network: {leaks[:3]}")

    DIST.mkdir(exist_ok=True)
    OUT.write_text(doc)
    print(f"\nwrote {OUT.relative_to(HERE)}  {OUT.stat().st_size/1024/1024:.2f} MB  (fully offline)")


if __name__ == "__main__":
    main()
