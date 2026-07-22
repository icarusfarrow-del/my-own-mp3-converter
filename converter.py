#!/usr/bin/env python3
"""
yt2mp3.py - Download audio from a YouTube link and save it as an MP3.

Usage:
    python3 yt2mp3.py <youtube-url> [output-directory]

Requires:
    pip install yt-dlp
    ffmpeg installed and available on PATH
"""

import argparse
import shutil
import sys
from pathlib import Path

try:
    from yt_dlp import YoutubeDL
except ImportError:
    print("Error: yt-dlp is not installed. Run: pip install yt-dlp", file=sys.stderr)
    sys.exit(1)


def check_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        print(
            "Error: ffmpeg is not installed or not on your PATH.\n"
            "Install it first, e.g.:\n"
            "  macOS:   brew install ffmpeg\n"
            "  Ubuntu:  sudo apt install ffmpeg\n"
            "  Windows: winget install ffmpeg",
            file=sys.stderr,
        )
        sys.exit(1)


def is_url(text: str) -> bool:
    return text.strip().lower().startswith(("http://", "https://", "www."))


def download_mp3(query: str, outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)

    # If it's not a URL, treat it as a search term and grab the top YouTube result.
    target = query if is_url(query) else f"ytsearch1:{query}"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(outdir / "%(title)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "0",  # best quality
            },
            {"key": "FFmpegMetadata"},
            {"key": "EmbedThumbnail"},
        ],
        "writethumbnail": True,
        "quiet": False,
        "noplaylist": True,
        "default_search": "ytsearch1",
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(target, download=False)
        if "entries" in info:
            entry = info["entries"][0]
            print(f"Found: {entry.get('title')} ({entry.get('webpage_url')})")
        ydl.download([target])


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a YouTube link (or song search) to an MP3 file."
    )
    parser.add_argument("url", help="YouTube video URL, or a song/search query")
    parser.add_argument(
        "output_dir",
        nargs="?",
        default=str(Path.home() / "Downloads"),
        help="Directory to save the MP3 in (default: ~/Downloads)",
    )
    args = parser.parse_args()

    check_ffmpeg()

    if is_url(args.url):
        print("Downloading and converting to MP3...")
    else:
        print(f'Searching YouTube for "{args.url}"...')
    download_mp3(args.url, Path(args.output_dir))
    print(f"Done. Saved in: {args.output_dir}")


if __name__ == "__main__":
    main()
