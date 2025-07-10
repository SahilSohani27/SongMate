import yt_dlp
import os
import zipfile
import shutil
from typing import Tuple

DOWNLOAD_DIR = ".songMate/downloads"
ZIP_DIR = ".songMate/zips"


def download_single_audio(url: str) -> str:
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'noplaylist': True,
    }

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get('title', 'downloaded_song')
        return os.path.join(DOWNLOAD_DIR, f"{title}.mp3")


def download_playlist_audio(url: str) -> Tuple[str, str]:
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    downloaded_files = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        
        playlist_title = info.get('title', 'playlist').replace(" ", "_").replace("/", "_")

        if 'entries' in info:
            for entry in info['entries']:
                title = entry.get('title', 'downloaded_song')
                downloaded_files.append(os.path.join(DOWNLOAD_DIR, f"{title}.mp3"))
        else:
            title = info.get('title', 'downloaded_song')
            downloaded_files.append(os.path.join(DOWNLOAD_DIR, f"{title}.mp3"))

    
    os.makedirs(ZIP_DIR, exist_ok=True)
    zip_path = os.path.join(ZIP_DIR, f"{playlist_title}.zip")
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for file in downloaded_files:
            zipf.write(file, arcname=os.path.basename(file))

    return zip_path, f"{playlist_title}.zip"


def cleanup_temp_files():
    
    if os.path.exists(DOWNLOAD_DIR):
        shutil.rmtree(DOWNLOAD_DIR, ignore_errors=True)
    if os.path.exists(ZIP_DIR):
        shutil.rmtree(ZIP_DIR, ignore_errors=True)

