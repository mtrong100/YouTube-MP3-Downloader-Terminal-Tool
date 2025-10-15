import os
import shutil
import subprocess
from pathlib import Path
from yt_dlp import YoutubeDL
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress, BarColumn, TextColumn, DownloadColumn, TransferSpeedColumn
from rich.panel import Panel

console = Console()

def get_downloads_folder() -> Path:
    """Tự động tìm thư mục Downloads của người dùng."""
    home = Path.home()
    for name in ["Downloads", "Tải xuống"]:
        p = home / name
        if p.exists():
            return p
    return home

def ffmpeg_installed() -> bool:
    return shutil.which("ffmpeg") is not None

def progress_hook(d):
    if d["status"] == "downloading":
        total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
        downloaded = d.get("downloaded_bytes", 0)
        progress_bar.update(progress_task, total=total, completed=downloaded)
    elif d["status"] == "finished":
        progress_bar.update(progress_task, completed=progress_bar.tasks[0].total or 1)

def add_metadata_with_thumbnail(file_path: Path, info: dict):
    """Thêm metadata và thumbnail vào MP3 bằng ffmpeg."""
    try:
        title = info.get("title", "Unknown Title")
        artist = info.get("uploader", "Unknown Artist")
        album = info.get("channel", "YouTube")
        date = str(info.get("upload_date", ""))[:8]
        description = info.get("description", "")
        thumb_url = info.get("thumbnail")

        # tải thumbnail
        thumb_path = file_path.with_name(file_path.stem + "_thumb.jpg")
        if thumb_url:
            try:
                import requests
                r = requests.get(thumb_url, timeout=10)
                with open(thumb_path, "wb") as f:
                    f.write(r.content)
                console.print(f"[cyan]🖼️ Đã tải thumbnail[/cyan]")
            except Exception as e:
                console.print(f"[yellow]⚠️ Không thể tải thumbnail: {e}[/yellow]")
                thumb_path = None
        else:
            thumb_path = None

        temp_file = file_path.with_name(file_path.stem + "_meta.mp3")

        # lệnh ffmpeg thêm metadata + ảnh bìa
        cmd = [
            "ffmpeg",
            "-i", str(file_path),
        ]

        if thumb_path and thumb_path.exists():
            cmd += ["-i", str(thumb_path), "-map", "0:a", "-map", "1:v", "-c", "copy", 
                    "-metadata", "title=" + title,
                    "-metadata", "artist=" + artist,
                    "-metadata", "album=" + album,
                    "-metadata", "date=" + date,
                    "-metadata", "comment=" + description,
                    "-disposition:v", "attached_pic",
                    "-id3v2_version", "3",
                    "-y", str(temp_file)]
        else:
            cmd += ["-c", "copy",
                    "-metadata", "title=" + title,
                    "-metadata", "artist=" + artist,
                    "-metadata", "album=" + album,
                    "-metadata", "date=" + date,
                    "-metadata", "comment=" + description,
                    "-id3v2_version", "3",
                    "-y", str(temp_file)]

        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        os.replace(temp_file, file_path)
        if thumb_path and thumb_path.exists():
            thumb_path.unlink(missing_ok=True)

        console.print(f"[green]🎧 Đã thêm metadata và thumbnail vào file MP3[/green]")

    except subprocess.CalledProcessError:
        console.print("[red]⚠️ Lỗi khi chạy ffmpeg để thêm metadata hoặc thumbnail![/red]")
    except Exception as e:
        console.print(f"[red]⚠️ Lỗi khi thêm metadata: {e}[/red]")

def download_youtube_mp3(url: str, outdir: Path):
    """Tải YouTube → MP3, thêm metadata và thumbnail."""
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
        global progress_task, progress_bar
        progress_task = progress.add_task("Đang tải...", total=0)
        progress_bar = progress

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            mp3_file = Path(ydl.prepare_filename(info)).with_suffix(".mp3")
            add_metadata_with_thumbnail(mp3_file, info)

def main():
    console.clear()
    console.print(Panel.fit("[bold magenta]🎵 YT-MP3 Downloader[/bold magenta]", width=40))
    console.print()

    if not ffmpeg_installed():
        console.print("[red]⚠️ ffmpeg chưa được cài hoặc chưa thêm vào PATH.[/red]")
        console.print("Tải tại: https://ffmpeg.org/download.html\n")
        return

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