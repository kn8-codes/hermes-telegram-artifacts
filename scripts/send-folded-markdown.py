#!/usr/bin/env python3
"""Generate and send a folded Markdown artifact in one command.

Usage:
  python3 scripts/send-folded-markdown.py notes.md "Meeting Notes" your-domain.com [chat_id] [thread_id]
  echo "# Hi" | python3 scripts/send-folded-markdown.py - "Quick Note" your-domain.com

This is a convenience wrapper around:
  1. generate-folded-markdown-viewer.py
  2. send-artifact.py
"""
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
GENERATE = SCRIPT_DIR / "generate-folded-markdown-viewer.py"
SEND = SCRIPT_DIR / "send-artifact.py"


def main() -> None:
    p = argparse.ArgumentParser(description="Generate and send a folded Markdown Telegram artifact")
    p.add_argument("markdown", help="Markdown file path, or '-' for stdin")
    p.add_argument("title", help="Artifact/viewer title and Telegram button label")
    p.add_argument("host", nargs="?", help="Public HTTPS host for artifact server; may also come from HERMES_DASHBOARD_HOST")
    p.add_argument("chat_id", nargs="?", help="Telegram chat ID; may also come from env")
    p.add_argument("thread_id", nargs="?", help="Telegram topic/thread ID; may also come from env")
    p.add_argument("--fold-level", type=int, default=2, choices=range(1, 7), metavar="1-6", help="Fold on headings up to this level (default: 2)")
    p.add_argument("--keep-html", help="Optional path to keep generated HTML instead of using a temp file")
    p.add_argument("--dry-run", action="store_true", help="Generate HTML and print path, but do not send")
    args = p.parse_args()

    if not GENERATE.exists():
        raise SystemExit(f"ERROR: missing generator: {GENERATE}")
    if not SEND.exists():
        raise SystemExit(f"ERROR: missing sender: {SEND}")

    if args.keep_html:
        out_path = Path(args.keep_html)
        out_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        tmp = tempfile.NamedTemporaryFile(prefix="folded-markdown-", suffix=".html", delete=False)
        tmp.close()
        out_path = Path(tmp.name)

    gen_cmd = [sys.executable, str(GENERATE), "--title", args.title, "--fold-level", str(args.fold_level), "--out", str(out_path)]
    if args.markdown == "-":
        md = sys.stdin.read()
        gen_cmd.extend(["--md", md])
    else:
        gen_cmd.extend(["--file", args.markdown])

    subprocess.run(gen_cmd, check=True, stdout=subprocess.DEVNULL)

    if args.dry_run:
        print(out_path)
        return

    send_cmd = [sys.executable, str(SEND), str(out_path), args.title]
    if args.host:
        send_cmd.append(args.host)
    if args.chat_id:
        send_cmd.append(args.chat_id)
    if args.thread_id:
        send_cmd.append(args.thread_id)

    subprocess.run(send_cmd, check=True)


if __name__ == "__main__":
    main()
