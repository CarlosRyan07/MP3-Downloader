from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from baixar_audio import download_audio_with_progress
from yt_dlp import YoutubeDL  # Necessário para a rota /get-info

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")
    format = request.form.get("format", "mp3")

    try:
        def progress_callback(progress, message, title, downloaded_bytes=None, total_bytes=None):
            # Envia os dados do progresso para o front-end
            socketio.emit("progress", {
                "progress": progress,
                "message": message,
                "title": title,
                "downloaded_bytes": downloaded_bytes,
                "total_bytes": total_bytes
            })

        title = download_audio_with_progress(url, format=format, progress_callback=progress_callback)
        
        # Se for uma playlist, retorna a lista de títulos
        if isinstance(title, list):
            return jsonify({"success": True, "titles": title})
        
        return jsonify({"success": True, "title": title})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/get-info", methods=["POST"])
def get_info():
    data = request.get_json()
    url = data.get("url")
    try:
        ydl_opts = {}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                "success": True,
                "title": info.get("title", "Desconhecido"),
                "duration": info.get("duration", "Desconhecido"),
                "channel": info.get("uploader", "Desconhecido"),
                "upload_date": info.get("upload_date", "Desconhecido"),
                "thumbnail": info.get("thumbnail", "")
            })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    socketio.run(app, debug=True)
