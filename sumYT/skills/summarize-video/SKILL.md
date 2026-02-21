---
name: summarize-video
description: This skill should be used when the user asks to "summarize a YouTube video", "get a summary of this video", "what is this video about", "summarize this", or provides a YouTube URL and asks for a summary, transcript analysis, or key points.
---

# YouTube Video Summarizer

Fetch a timed transcript from a YouTube URL and produce a structured markdown summary
with timestamped chapters, tables, and key takeaways. Save the result and enter follow-up Q&A mode.

## Workflow

### Step 1: Fetch video metadata

Use `WebFetch` on the YouTube URL to extract metadata from the page HTML:
- Video title (from `<title>` or `og:title`)
- Channel name (from `og:site_name` or the channel link)
- Duration (from `og:video:duration` or visible on the page)
- Video ID (see Video ID Extraction below) — needed for all timestamp links

If duration is not available from the page, leave it as `N/A` in the document header.

### Step 2: Fetch timed transcript

Run the transcript script via Bash. Use the bare video ID (e.g. `dQw4w9WgXcQ`) extracted in Step 1 — not the full URL:

```bash
python3 "$(git rev-parse --show-toplevel)/sumYT/skills/summarize-video/scripts/get_transcript.py" <video_id>
```

`git rev-parse --show-toplevel` resolves the absolute repository root regardless of your current working directory.

The script outputs a JSON array of snippets:
```json
[{"text": "Hello", "start": 0.0, "duration": 1.54}, ...]
```

Each snippet has:
- `text`: the spoken text
- `start`: timestamp in seconds (float)
- `duration`: duration in seconds (float)

Convert `start` seconds to `[M:SS]` format for display:
- `M = floor(start / 60)`
- `SS = floor(start % 60)` (zero-padded to 2 digits)

Example: `start=92.5` → `[1:32]`

If the script exits with a non-zero code, report the error to the user (the video may have no transcript, be unavailable, or have transcripts disabled).

Detect language from the transcript text (French, English, Spanish, etc.) — the summary will be written in this language.

To convert a `[M:SS]` timestamp back to seconds for YouTube links: `seconds = minutes * 60 + seconds`.

### Step 3: Segment into chapters

Divide the timed transcript into 3-10 chapters based on topic shifts:
- Look for transition phrases ("now let's talk about", "moving on", "next", "in this section", etc.)
- Look for topic or subject changes in the content
- Prefer natural boundaries over arbitrary time splits
- Each chapter needs: a start timestamp from the `[M:SS]` markers, converted to seconds for links

For videos under 10 minutes: 3-5 chapters is appropriate.
For videos over 1 hour: up to 10 chapters.

### Step 4: Compose the markdown document

Read `references/output-template.md` first, then follow it exactly.

Key rules:
- No emojis anywhere in the document
- Language matches the video transcript language
- Timestamp links format: `https://youtu.be/<VIDEO_ID>?t=<seconds>` (integer seconds)
- Use tables for structured/comparative data; use prose paragraphs for narrative content
- Key Takeaways section always at the end: 3-7 bullets

### Step 5: Save the file

Generate a slug from the video title:
- Lowercase
- Replace spaces and non-alphanumeric characters with hyphens
- Collapse consecutive hyphens into one
- Trim to 60 characters maximum

Save path: `.claude/output/sumYT/YYYY-MM-DD_<slug>.md`

Create the directory if it does not exist.

### Step 6: Enter follow-up mode

After saving, confirm to the user:

> Summary saved to `.claude/output/sumYT/<filename>.md`. Ask me anything about the video — I can search the web or fetch sources to go deeper.

When answering follow-up questions:
- Use `WebSearch` to find related information, context, or fact-checks
- Use `WebFetch` to retrieve specific pages or sources referenced in the video
- Cite sources inline: [Source Name](URL)
- Do not re-summarize the entire video — answer only the specific question asked
- Keep answers focused and concise

## Video ID Extraction

Extract the video ID from the URL before composing the document:

| URL Format | Where the ID is |
|------------|-----------------|
| `https://www.youtube.com/watch?v=ABC123` | `v` query parameter |
| `https://youtu.be/ABC123` | last path segment |
| `https://youtube.com/watch?v=ABC123&t=60` | `v` query parameter |
| `https://www.youtube.com/embed/ABC123` | last path segment |

Use the extracted ID for all timestamp links: `https://youtu.be/<VIDEO_ID>?t=<seconds>`

## Prerequisites

The `youtube-transcript-api` Python package must be installed:

```bash
pip install youtube-transcript-api
```

No Node.js or MCP server is required.

## References

- **`references/output-template.md`** — Exact markdown format to replicate for every summary
