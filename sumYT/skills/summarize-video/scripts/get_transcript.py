#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = ["youtube-transcript-api"]
# ///
"""
Fetch a YouTube transcript and output JSON to stdout.

Usage:
    python3 get_transcript.py <video_id> [lang1 lang2 ...]

Output (stdout):
    JSON array of {"text": str, "start": float, "duration": float}

Exit codes:
    0  success
    1  error (message on stderr)
"""
import sys
import json


def main():
    if len(sys.argv) < 2:
        print("Usage: get_transcript.py <video_id> [lang1 lang2 ...]", file=sys.stderr)
        sys.exit(1)

    video_id = sys.argv[1]
    languages = sys.argv[2:] if len(sys.argv) > 2 else ["en"]

    try:
        from youtube_transcript_api import (
            YouTubeTranscriptApi,
            NoTranscriptFound,
            TranscriptsDisabled,
            VideoUnavailable,
        )
    except ImportError:
        print(
            "Error: youtube-transcript-api is not installed.\n"
            "Run via: uv run get_transcript.py <video_id>",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id, languages=languages)
        snippets = [
            {"text": s.text, "start": s.start, "duration": s.duration}
            for s in transcript
        ]
        print(json.dumps(snippets))
    except VideoUnavailable:
        print(f"Error: video '{video_id}' is unavailable or private.", file=sys.stderr)
        sys.exit(1)
    except TranscriptsDisabled:
        print(f"Error: transcripts are disabled for '{video_id}'.", file=sys.stderr)
        sys.exit(1)
    except NoTranscriptFound:
        print(f"Error: no transcript found for languages {languages}.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error fetching transcript: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
