#!/usr/bin/env python3
# ytmp3_simple.py
# Clean minimal YouTube → MP3 downloader for terminal
# Requires: pip install yt-dlp rich

import os
import shutil
from pathlib import Path
from time import sleep
from yt_dlp import YoutubeDL
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress, BarColumn, TextColumn, DownloadColumn, TransferSpeedColumn
from rich.panel import Panel

console = Console()

def get_downloads_folder() -> Path:
    """Tự động tìm thư mục Downloads của người dùng."""
    home = Path.home()
    candidates = [home / "Downloads", home / "Tải xuống"]
    for c in candidates:
        if c.exists():
            return c
    return home

def ffmpeg_installed() -> bool:
    return shutil.which("ffmpeg") is not None

def download_youtube_mp3(url: str, outdir: Path):
    """Tải YouTube → MP3 với chất lượng tốt nhất."""
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(outdir / "%(title)s.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
        "progress_hooks": [progress_hook],
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "320",
        }],
    }

    with Progress(
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
        console=console,
        transient=True,
    ) as progress:
        global progress_task
        progress_task = progress.add_task("Đang tải...", total=0)
        global progress_bar
        progress_bar = progress

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

def progress_hook(d):
    if d['status'] == 'downloading':
        total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
        downloaded = d.get('downloaded_bytes', 0)
        progress_bar.update(progress_task, total=total, completed=downloaded)
    elif d['status'] == 'finished':
        progress_bar.update(progress_task, completed=progress_bar.tasks[0].total or 1)

def main():
    console.clear()
    console.print(Panel.fit("[bold magenta]🎵 YT-MP3 Downloader[/bold magenta]", width=40))
    console.print()

    # Kiểm tra ffmpeg
    if not ffmpeg_installed():
        console.print("[red]⚠️ ffmpeg chưa được cài hoặc chưa thêm vào PATH.[/red]")
        console.print("Cài đặt tại: https://ffmpeg.org/download.html\n")
        return

    # Nhập link YouTube
    url = Prompt.ask("[bold green]Nhập link YouTube[/bold green]")
    if not url.strip():
        console.print("[red]❌ Bạn chưa nhập link.[/red]")
        return

    outdir = get_downloads_folder()

    try:
        download_youtube_mp3(url.strip(), outdir)
    except Exception as e:
        console.print(f"[red]Lỗi khi tải: {e}[/red]")
        return

    # Tìm file mới nhất vừa tải
    latest_file = max(outdir.glob("*.mp3"), key=lambda p: p.stat().st_mtime)
    size_mb = latest_file.stat().st_size / (1024 * 1024)
    console.print()
    console.print(Panel.fit(
        f"[bold green]✅ Tải thành công![/bold green]\n\n"
        f"[bold]Tên file:[/bold] {latest_file.name}\n"
        f"[bold]Kích thước:[/bold] {size_mb:.2f} MB\n"
        f"[bold]Vị trí:[/bold] {latest_file.parent}",
        title="[cyan]Hoàn tất[/cyan]",
        border_style="green"
    ))

if __name__ == "__main__":
    main()
