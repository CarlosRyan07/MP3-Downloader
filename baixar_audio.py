import os
from yt_dlp import YoutubeDL
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC
import platform

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
        "format": "bestaudio/best" if format == "mp3" else "best",
        "outtmpl": os.path.join(download_folder, "%(title)s.%(ext)s"),
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
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ] if format == "mp3" else [],
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url)
        title = info.get("title", "Desconhecido")
        artist = info.get("uploader", "Desconhecido")
        output_file = os.path.join(download_folder, f"{title}.mp3")

        if format == "mp3":
            add_metadata(output_file, title, artist)

        return title  # Retorna apenas o título da música

def add_metadata(file_path, title, artist):
    """Adiciona metadados ID3 ao arquivo MP3 baixado."""
    try:
        audio = MP3(file_path, ID3=ID3)
        audio.add_tags()
    except Exception:
        pass  # Se as tags já existirem, continua sem erro

    audio.tags.add(TIT2(encoding=3, text=title))  # Título
    audio.tags.add(TPE1(encoding=3, text=artist))  # Artista
    audio.tags.add(TALB(encoding=3, text="Desconhecido"))  # Álbum
    audio.tags.add(TDRC(encoding=3, text="2025"))  # Ano
    audio.save()

def main():
    """Função principal para testar o download de música com metadados."""
    print("Escolha uma opção:")
    print("1 - Baixar áudio de um vídeo (MP3)")
    print("2 - Baixar áudios de uma playlist (MP3)")
    
    choice = input("Digite sua escolha (1 ou 2): ")
    url = input("Digite a URL: ")

    if choice == "1":
        print("Iniciando download...")
        title = download_audio_with_progress(url)
        print(f"Download de {title} concluído com sucesso!")
    elif choice == "2":
        print("Iniciando download da playlist...")
        title = download_audio_with_progress(url, playlist=True)
        print(f"Download da playlist {title} concluído com sucesso!")
    else:
        print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()
