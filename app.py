from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import os
from baixar_audio import download_audio_with_progress  # Certifique-se de que este arquivo está no mesmo diretório

app = Flask(__name__)
app.config['THREADING'] = True  # Garante que o Flask seja seguro para threads
socketio = SocketIO(app, async_mode="threading")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")
    format = request.form.get("format", "mp3")

    try:
        title = None

        def progress_callback(progress, message, title):
            socketio.emit("progress", {"progress": progress, "message": message, "title": title})

        print(f"Iniciando download da URL: {url}")
        title = download_audio_with_progress(url, format=format, progress_callback=progress_callback)

        if title:
            print(f"Download concluído: {title}")
            return jsonify({"success": True, "title": title})
        else:
            raise ValueError("Falha ao baixar o arquivo.")

    except Exception as e:
        print(f"Erro no download: {e}")
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    socketio.run(app, debug=True)
