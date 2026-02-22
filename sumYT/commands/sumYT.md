---
description: Summarize a YouTube video with chapters, timestamps, and markdown output
argument-hint: "<youtube-url>"
allowed-tools: ["Bash", "Write", "WebSearch", "WebFetch"]
---

# /sumYT — YouTube Video Summarizer

User request: **"$ARGUMENTS"**

## Instructions

Use the `summarize-video` skill to fulfill this request:

1. **Parse the URL** from `$ARGUMENTS`. If no URL is provided, ask: "Please provide a YouTube URL."
2. **Follow the `summarize-video` skill** step by step:
   - Fetch video metadata
   - Fetch full timed transcript (handle pagination)
   - Detect language
   - Segment into chapters
   - Compose markdown document using `references/output-template.md`
   - Save to `.claude/output/sumYT/`
   - Enter follow-up mode

## Requirements

**Python 3.12+** and **[uv](https://docs.astral.sh/uv/)** must be available. Dependencies install automatically on first use via `uv run` — no manual setup needed.
