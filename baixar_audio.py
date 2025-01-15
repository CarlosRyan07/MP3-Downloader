import os
from yt_dlp import YoutubeDL
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC

def get_default_download_folder():
    home = os.path.expanduser("~")
    return os.path.join(home, "Downloads")

def download_audio_with_progress(url, format="mp3", progress_callback=None):
    download_folder = get_default_download_folder()
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(download_folder, "%(title)s.%(ext)s"),
        "nocheckcertificate": True,
        "cachedir": False,
        "progress_hooks": [
            lambda d: progress_callback(
                progress=(d.get("downloaded_bytes", 0) / d.get("total_bytes", 1)) * 100,
                message="Baixando música...",
                title=d.get("info_dict", {}).get("title", "Desconhecido"),
            )
            if d["status"] == "downloading"
            else progress_callback(progress=100, message="Download concluído!", title=d.get("info_dict").get("title", "Desconhecido"))
        ],
        "postprocessors": [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}
        ] if format == "mp3" else [],
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get("title", "Desconhecido")
        artist = info.get("uploader", "Desconhecido")
        output_file = os.path.join(download_folder, f"{title}.mp3")

        if format == "mp3":
            add_metadata(output_file, title, artist)

        return title

def add_metadata(file_path, title, artist):
    try:
        audio = MP3(file_path, ID3=ID3)
        audio.add_tags()
    except Exception:
        pass

    audio.tags.add(TIT2(encoding=3, text=title))
    audio.tags.add(TPE1(encoding=3, text=artist))
    audio.tags.add(TALB(encoding=3, text="Desconhecido"))
    audio.tags.add(TDRC(encoding=3, text="2025"))
    audio.save()
