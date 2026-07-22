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


def download_mp3(url: str, outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)

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
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert a YouTube link to an MP3 file.")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument(
        "output_dir",
        nargs="?",
        default=str(Path.home() / "Music" / "yt2mp3"),
        help="Directory to save the MP3 in (default: ~/Music/yt2mp3)",
    )
    args = parser.parse_args()

    check_ffmpeg()

    print("Downloading and converting to MP3...")
    download_mp3(args.url, Path(args.output_dir))
    print(f"Done. Saved in: {args.output_dir}")


if __name__ == "__main__":
    main()
