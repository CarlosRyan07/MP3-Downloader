import os
from yt_dlp import YoutubeDL
import platform
import time
import requests  # Para baixar a thumbnail

def get_default_download_folder():
    """Retorna a pasta de download padrão do sistema."""
    home = os.path.expanduser("~")
    return os.path.join(home, "Downloads")

def set_creation_time(file_path):
    """Altera a data de criação, modificação e acesso do arquivo."""
    current_time = time.time()
    os.utime(file_path, (current_time, current_time))
    if platform.system() == "Windows":
        try:
            import win32file
            import pywintypes
            handle = win32file.CreateFile(
                file_path,
                win32file.GENERIC_WRITE,
                win32file.FILE_SHARE_WRITE,
                None,
                win32file.OPEN_EXISTING,
                0,
                None,
            )
            creation_time = pywintypes.Time(current_time)
            win32file.SetFileTime(handle, creation_time, None, None)
            handle.close()
        except ImportError:
            print("Aviso: pywin32 não está instalado. A data de criação não foi alterada.")

def progress_hook_wrapper(d, progress_callback):
    """Wrapper para o progress hook, que envia também downloaded_bytes e total_bytes."""
    if progress_callback:
        if d["status"] == "downloading":
            total_bytes = d.get("total_bytes") or d.get("total_bytes_estimate", 1)
            progress_callback(
                progress=(d.get("downloaded_bytes", 0) / total_bytes) * 100,
                message="Baixando música...",
                title=d.get("info_dict", {}).get("title", "Desconhecido"),
                downloaded_bytes=d.get("downloaded_bytes", 0),
                total_bytes=total_bytes
            )
        elif d["status"] == "finished":
            progress_callback(
                progress=100,
                message="Download concluído!",
                title=d.get("info_dict", {}).get("title", "Desconhecido"),
                downloaded_bytes=d.get("downloaded_bytes", 0),
                total_bytes=d.get("total_bytes", 1)
            )

def download_audio_with_progress(url, format="mp3", progress_callback=None):
    """Baixa o áudio ou playlist com suporte a atualizações de progresso."""
    download_folder = get_default_download_folder()

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(download_folder, "%(title)s.%(ext)s"),
        "progress_hooks": [
            lambda d: progress_hook_wrapper(d, progress_callback)
        ],
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "noplaylist": False,  # Permitir download de playlists
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        # Caso seja uma playlist, info['entries'] conterá uma lista de músicas
        if "entries" in info:
            titles = []
            for entry in info["entries"]:
                title = entry.get("title", "Desconhecido")
                output_file = os.path.join(download_folder, f"{title}.{format}")
                if os.path.exists(output_file):
                    set_creation_time(output_file)
                titles.append(title)
            return titles  # Retorna a lista de títulos
        else:
            title = info.get("title", "Desconhecido")
            output_file = os.path.join(download_folder, f"{title}.{format}")
            if os.path.exists(output_file):
                set_creation_time(output_file)
            return title

# Função main para teste via terminal (opcional)
def main():
    print("Escolha uma opção:")
    print("1 - Baixar áudio de um vídeo (MP3)")
    print("2 - Baixar áudios de uma playlist (MP3)")
    
    choice = input("Digite sua escolha (1 ou 2): ")
    url = input("Digite a URL: ")

    def progress_callback(progress, message, title, downloaded_bytes=None, total_bytes=None):
        print(f"[{progress:.2f}%] {message} - {title}")

    if choice == "1":
        print("Iniciando download...")
        title = download_audio_with_progress(url, progress_callback=progress_callback)
        print(f"Download de {title} concluído com sucesso!")
    elif choice == "2":
        print("Iniciando download da playlist...")
        titles = download_audio_with_progress(url, progress_callback=progress_callback)
        print(f"Download da playlist {titles} concluído com sucesso!")
    else:
        print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()
