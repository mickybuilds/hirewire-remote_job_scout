"""Prints the text of a .docx file. Usage: python scripts/docx_text.py <file.docx>"""

import re
import sys
import zipfile
from xml.etree import ElementTree

NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def text(path: str) -> str:
    with zipfile.ZipFile(path) as z:
        root = ElementTree.fromstring(z.read("word/document.xml"))
    lines = []
    for p in root.iter(NS + "p"):
        parts = []
        for run in p.iter(NS + "r"):
            for e in run:
                if e.tag == NS + "t":
                    parts.append(e.text or "")
                elif e.tag == NS + "tab":
                    parts.append("	")
        line = "".join(parts)
        style = p.find(f"{NS}pPr/{NS}pStyle")
        if p.find(f"{NS}pPr/{NS}numPr") is not None or (style is not None and "List" in style.get(NS + "val", "")):
            line = "- " + line
        lines.append(line)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        raise SystemExit(2)
    sys.stdout.reconfigure(encoding="utf-8")
    print(text(sys.argv[1]))
