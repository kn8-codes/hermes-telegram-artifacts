#!/usr/bin/env python3
"""Generate a folded markdown viewer artifact.

Usage:
  python3 generate-folded-markdown-viewer.py --file notes.md --title "Meeting notes"
  echo "# Hello" | python3 generate-folded-markdown-viewer.py --stdin --title "Quick note"
  python3 generate-folded-markdown-viewer.py --md "# Title\nSome text" --title "Inline"

The generated HTML folds Markdown into expandable sections by heading.
"""
import argparse
import re
import sys
from pathlib import Path

TEMPLATE = Path(__file__).parent.parent / "templates" / "folded-markdown-viewer.html"


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:40] or "document"


def escape_template_literal(text: str) -> str:
    return text.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")


def main() -> None:
    p = argparse.ArgumentParser(description="Generate folded markdown viewer artifact")
    p.add_argument("--file", "-f", help="Path to markdown file")
    p.add_argument("--md", "-m", help="Inline markdown string")
    p.add_argument("--stdin", action="store_true", help="Read markdown from stdin")
    p.add_argument("--title", "-t", default="Document", help="Viewer title")
    p.add_argument("--fold-level", type=int, default=2, choices=range(1, 7), metavar="1-6", help="Fold on headings up to this level (default: 2)")
    p.add_argument("--out", "-o", help="Output path (default: /tmp/folded-markdown-viewer-<slug>.html)")
    args = p.parse_args()

    if args.file:
        md_data = Path(args.file).read_text()
    elif args.stdin:
        md_data = sys.stdin.read()
    elif args.md:
        md_data = args.md
    else:
        p.error("Provide --file, --md, or --stdin")

    html = TEMPLATE.read_text()
    html = html.replace("{{TITLE}}", args.title)
    html = html.replace("{{MARKDOWN_DATA}}", escape_template_literal(md_data))
    html = html.replace("{{FOLD_LEVEL}}", str(args.fold_level))

    out_path = args.out or f"/tmp/folded-markdown-viewer-{slugify(args.title)}.html"
    Path(out_path).write_text(html)
    print(out_path)


if __name__ == "__main__":
    main()
