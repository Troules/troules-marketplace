---
name: summarize-video
description: This skill should be used when the user asks to "summarize a YouTube video", "get a summary of this video", "what is this video about", "summarize this", or provides a YouTube URL and asks for a summary, transcript analysis, or key points.
---

# YouTube Video Summarizer

Fetch a timed transcript from a YouTube URL and produce a structured markdown summary
with timestamped chapters, tables, and key takeaways. Save the result and enter follow-up Q&A mode.

## Workflow

### Step 1: Fetch video metadata

Call `mcp__plugin_sumYT_youtube-transcript__get_video_info` with the URL.

Extract:
- Video title
- Channel name
- Duration (convert to H:MM:SS format)
- Video ID (see Video ID Extraction below) — needed for all timestamp links

### Step 2: Fetch full timed transcript

Call `mcp__plugin_sumYT_youtube-transcript__get_timed_transcript` with the URL.

Handle pagination:
- If the response contains `next_cursor`, call again passing `next_cursor` to get the next page
- Repeat until no `next_cursor` is returned
- Concatenate all pages into one full timed transcript

Detect language from the transcript text (French, English, Spanish, etc.) — the summary will be written in this language.

### Step 3: Segment into chapters

Divide the timed transcript into 5-10 chapters based on topic shifts:
- Look for transition phrases ("now let's talk about", "moving on", "next", "in this section", etc.)
- Look for topic or subject changes in the content
- Prefer natural boundaries over arbitrary time splits
- Each chapter needs: a start timestamp in seconds, and a descriptive title

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

## MCP Tool Names

The exact tool names depend on how Claude Code normalizes the plugin and server names.
If tool calls fail, run `/mcp` in Claude Code to see the actual registered names.

Expected names (verify with `/mcp` after installation):
- `mcp__plugin_sumYT_youtube-transcript__get_video_info`
- `mcp__plugin_sumYT_youtube-transcript__get_timed_transcript`

## References

- **`references/output-template.md`** — Exact markdown format to replicate for every summary
