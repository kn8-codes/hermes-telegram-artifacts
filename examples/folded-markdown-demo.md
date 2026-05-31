# Folded Markdown Viewer Demo

A short sample document for testing the folded Markdown viewer.

## What changed

- Long Markdown can be folded by heading.
- The first section opens by default.
- Telegram theme colors are used through Mini App CSS variables.

## Why it matters

This makes long agent outputs easier to read on Telegram:

- catch-up packets
- meeting notes
- contribution reports
- research summaries
- decision logs

## Example code

```bash
python3 scripts/generate-folded-markdown-viewer.py \
  --file examples/folded-markdown-demo.md \
  --title "Folded Markdown Demo"
```

## Next step

Send the generated HTML with `scripts/send-artifact.py` once the artifact server has an HTTPS endpoint.
