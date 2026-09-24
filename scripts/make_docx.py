"""Converts a CV written in simple Markdown into a Harvard-style, ATS-friendly .docx (and optionally a PDF).

Usage:
    python scripts/make_docx.py <folder>/cv.md <folder>/CV_Name_Company.docx [--pdf]

Supported Markdown:
    # Full Name                    → name, centered
    lines before the first ##      → contact lines, centered
    ## SECTION                     → section heading, uppercase with a rule
    ### Organization || City       → entry line: bold left text, right-aligned text
    _Role title_ || Jan 2024 – Now → second entry line: left text, right-aligned text
    - text                         → bullet
    **bold**, _italic_             → inline formatting
    any other line                 → paragraph

--pdf converts the .docx with LibreOffice (soffice) or, on Windows, Microsoft Word, when available.
Python standard library only.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
FONT = "Times New Roman"
TEXT_WIDTH = 12240 - 2 * 1080  # letter width minus side margins, in twips

CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
</Types>"""

RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
</Relationships>"""

DOC_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
</Relationships>"""


def style(sid: str, name: str, size: int, bold: bool = False, before: int = 0, after: int = 0,
          border: bool = False, caps: bool = False, center: bool = False, outline: int | None = None) -> str:
    rpr = ("<w:b/>" if bold else "") + ("<w:caps/>" if caps else "") + f'<w:sz w:val="{size}"/>'
    ppr = f'<w:spacing w:before="{before}" w:after="{after}"/>'
    if border:
        ppr += '<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="1" w:color="000000"/></w:pBdr>'
    if center:
        ppr += '<w:jc w:val="center"/>'
    if outline is not None:
        ppr += f'<w:keepNext/><w:outlineLvl w:val="{outline}"/>'
    return (f'<w:style w:type="paragraph" w:styleId="{sid}"><w:name w:val="{name}"/>'
            f'<w:basedOn w:val="Normal"/><w:qFormat/><w:pPr>{ppr}</w:pPr><w:rPr>{rpr}</w:rPr></w:style>')


STYLES = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles {W}>
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}" w:cs="{FONT}" w:eastAsia="{FONT}"/><w:sz w:val="22"/><w:lang w:val="en-US"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:after="0" w:line="252" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>
{style("Title", "Title", 32, bold=True, after=40, center=True)}
{style("Contact", "Contact", 21, after=20, center=True)}
{style("Heading1", "heading 1", 22, bold=True, before=200, after=80, border=True, caps=True, outline=0)}
{style("Entry", "Entry", 22, before=100, outline=1)}
<w:style w:type="paragraph" w:styleId="ListBullet"><w:name w:val="List Bullet"/><w:basedOn w:val="Normal"/><w:qFormat/>
<w:pPr><w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr><w:spacing w:before="20" w:after="20"/><w:ind w:left="360" w:hanging="260"/></w:pPr></w:style>
</w:styles>"""

NUMBERING = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering {W}>
<w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="singleLevel"/>
<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="•"/><w:lvlJc w:val="left"/>
<w:pPr><w:ind w:left="360" w:hanging="260"/></w:pPr><w:rPr><w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}"/></w:rPr></w:lvl>
</w:abstractNum>
<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>
</w:numbering>"""


def runs(text: str, bold: bool = False) -> str:
    """Inline **bold** and _italic_ → runs."""
    out = []
    for token in re.split(r"(\*\*.+?\*\*|(?<![\w])_.+?_(?![\w]))", text):
        if not token:
            continue
        b, i = bold, False
        if token.startswith("**") and token.endswith("**"):
            token, b = token[2:-2], True
        elif token.startswith("_") and token.endswith("_") and len(token) > 2:
            token, i = token[1:-1], True
        props = ("<w:b/>" if b else "") + ("<w:i/>" if i else "")
        rpr = f"<w:rPr>{props}</w:rPr>" if props else ""
        out.append(f'<w:r>{rpr}<w:t xml:space="preserve">{escape(token)}</w:t></w:r>')
    return "".join(out)


def paragraph(text: str, style_id: str = "", bold: bool = False) -> str:
    ppr = f'<w:pStyle w:val="{style_id}"/>' if style_id else ""
    if "||" in text:
        left, right = (s.strip() for s in text.split("||", 1))
        ppr += f'<w:tabs><w:tab w:val="right" w:pos="{TEXT_WIDTH}"/></w:tabs>'
        content = runs(left, bold) + "<w:r><w:tab/></w:r>" + runs(right, bold)
    else:
        content = runs(text, bold)
    return f"<w:p><w:pPr>{ppr}</w:pPr>{content}</w:p>"


def convert(markdown: str) -> tuple[str, str]:
    body, title, in_header = [], "", True
    for raw in markdown.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("### "):
            body.append(paragraph(line[4:], "Entry", bold=True))
        elif line.startswith("## "):
            in_header = False
            body.append(paragraph(line[3:], "Heading1"))
        elif line.startswith("# "):
            title = title or line[2:]
            body.append(paragraph(line[2:], "Title"))
        elif re.match(r"^[-*•] ", line):
            body.append(paragraph(line[2:], "ListBullet"))
        elif in_header and title:
            body.append(paragraph(line, "Contact"))
        else:
            body.append(paragraph(line))
    section = ('<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
               '<w:pgMar w:top="1008" w:right="1080" w:bottom="1008" w:left="1080" w:header="0" w:footer="0" w:gutter="0"/></w:sectPr>')
    document = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {W}><w:body>'
                + "".join(body) + section + "</w:body></w:document>")
    return document, title


def core(title: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            f"<dc:title>{escape(title)} — CV</dc:title><dc:creator>{escape(title)}</dc:creator>"
            f'<dcterms:created xsi:type="dcterms:W3CDTF">{stamp}</dcterms:created></cp:coreProperties>')


def to_pdf(docx: Path) -> Path | None:
    """Converts with LibreOffice or, on Windows, Microsoft Word. Returns None if neither is available."""
    pdf = docx.with_suffix(".pdf")
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if soffice:
        subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", str(docx.parent), str(docx)],
                       check=False, capture_output=True, timeout=120)
    elif os.name == "nt":
        script = (f"$w = New-Object -ComObject Word.Application; $w.Visible = $false; "
                  f"$d = $w.Documents.Open('{docx.resolve()}', $false, $true); "
                  f"$d.SaveAs2('{pdf.resolve()}', 17); $d.Close($false); $w.Quit()")
        subprocess.run(["powershell", "-NoProfile", "-Command", script], check=False, capture_output=True, timeout=120)
    return pdf if pdf.exists() else None


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--pdf"]
    if len(args) != 2:
        print(__doc__)
        return 2
    source, target = Path(args[0]), Path(args[1])
    document, title = convert(source.read_text(encoding="utf-8"))
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", RELS)
        z.writestr("word/_rels/document.xml.rels", DOC_RELS)
        z.writestr("word/document.xml", document)
        z.writestr("word/styles.xml", STYLES)
        z.writestr("word/numbering.xml", NUMBERING)
        z.writestr("docProps/core.xml", core(title))
    print(f"Created {target}")
    if "--pdf" in sys.argv:
        pdf = to_pdf(target)
        print(f"Created {pdf}" if pdf else "PDF not created: install LibreOffice, or open the .docx and export it as PDF.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
