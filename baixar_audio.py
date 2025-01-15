import os
from yt_dlp import YoutubeDL
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC
import platform
import time

def get_default_download_folder():
    """Retorna a pasta de download padrão do sistema."""
    home = os.path.expanduser("~")
    if platform.system() == "Windows":
        return os.path.join(home, "Downloads")
    else:
        return os.path.join(home, "Downloads")

def download_audio_with_progress(url, format="mp3", progress_callback=None):
    """Baixa o áudio com suporte a atualizações de progresso e adiciona metadados."""
    download_folder = get_default_download_folder()

    ydl_opts = {
        "format": "bestaudio/best",  # Baixar melhor áudio
        "outtmpl": os.path.join(download_folder, "%(title)s.%(ext)s"),
        "progress_hooks": [
            lambda d: (
                progress_callback(
                    progress=(d.get("downloaded_bytes", 0) / d.get("total_bytes", 1)) * 100,
                    message="Baixando música...",
                    title=d.get("info_dict", {}).get("title", "Desconhecido"),
                )
                if d["status"] == "downloading" and progress_callback
                else progress_callback(
                    progress=100,
                    message="Download concluído!",
                    title=d.get("info_dict").get("title", "Desconhecido"),
                )
                if d["status"] == "finished" and progress_callback
                else None
            )
        ],
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",  # Converte para MP3
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get("title", "Desconhecido")
        artist = info.get("uploader", "Desconhecido")
        output_file = os.path.join(download_folder, f"{title}.mp3")

        add_metadata(output_file, title, artist)
        set_creation_time(output_file)  # Define a data de criação corretamente

        return title

def add_metadata(file_path, title, artist):
    """Adiciona metadados ID3 ao arquivo MP3 baixado."""
    try:
        audio = MP3(file_path, ID3=ID3)
        audio.add_tags()
    except Exception:
        pass  # Ignorar se as tags já existirem

    audio.tags.add(TIT2(encoding=3, text=title))  # Título
    audio.tags.add(TPE1(encoding=3, text=artist))  # Artista
    audio.tags.add(TALB(encoding=3, text="Desconhecido"))  # Álbum
    audio.tags.add(TDRC(encoding=3, text="2025"))  # Ano
    audio.save()

def set_creation_time(file_path):
    """Altera a data de criação, modificação e acesso do arquivo."""
    current_time = time.time()

    # Muda a data de acesso e modificação (funciona no Linux/macOS/Windows)
    os.utime(file_path, (current_time, current_time))

    # Muda a data de criação no Windows
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

def main():
    """Função principal para testar o download."""
    print("Escolha uma opção:")
    print("1 - Baixar áudio de um vídeo (MP3)")
    print("2 - Baixar áudios de uma playlist (MP3)")
    
    choice = input("Digite sua escolha (1 ou 2): ")
    url = input("Digite a URL: ")

    if choice == "1":
        print("Iniciando download...")

        # Define um callback para progresso
        def progress_callback(progress, message, title):
            print(f"[{progress:.2f}%] {message} - {title}")

        title = download_audio_with_progress(url, progress_callback=progress_callback)
        print(f"Download de {title} concluído com sucesso!")
    elif choice == "2":
        print("Iniciando download da playlist...")

        # Define um callback para progresso
        def progress_callback(progress, message, title):
            print(f"[{progress:.2f}%] {message} - {title}")

        title = download_audio_with_progress(url, progress_callback=progress_callback)
        print(f"Download da playlist {title} concluído com sucesso!")
    else:
        print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()
