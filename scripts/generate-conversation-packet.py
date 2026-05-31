#!/usr/bin/env python3
"""Generate a folded conversation packet artifact from JSON.

JSON shape:
{
  "title": "Today catch-up",
  "generated_at": "2026-05-31T12:00:00Z",
  "cards": [
    {
      "question": "What happened?",
      "summary": "Short answer",
      "status": "needs_decision|done|blocked|parked",
      "tags": ["artifact"],
      "artifacts": ["path or URL"],
      "decisions": ["Approve PR?"],
      "receipts": ["commit abc123"],
      "full": "Longer note"
    }
  ]
}
"""
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

TEMPLATE = Path(__file__).parent.parent / "templates" / "conversation-packet-viewer.html"


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:40] or "conversation-packet"


def main() -> None:
    p = argparse.ArgumentParser(description="Generate conversation packet viewer artifact")
    p.add_argument("--json", "-j", help="Path to packet JSON file")
    p.add_argument("--stdin", action="store_true", help="Read packet JSON from stdin")
    p.add_argument("--title", "-t", help="Override packet title")
    p.add_argument("--out", "-o", help="Output HTML path")
    args = p.parse_args()

    if args.json:
        packet = json.loads(Path(args.json).read_text())
    elif args.stdin:
        packet = json.load(sys.stdin)
    else:
        p.error("Provide --json or --stdin")

    title = args.title or packet.get("title") or "Conversation Packet"
    packet.setdefault("title", title)
    packet.setdefault("generated_at", datetime.now(timezone.utc).isoformat())
    packet.setdefault("cards", [])

    html = TEMPLATE.read_text()
    html = html.replace("{{TITLE}}", title)
    html = html.replace("{{PACKET_JSON}}", json.dumps(packet, ensure_ascii=False))

    out_path = args.out or f"/tmp/conversation-packet-{slugify(title)}.html"
    Path(out_path).write_text(html)
    print(out_path)


if __name__ == "__main__":
    main()
