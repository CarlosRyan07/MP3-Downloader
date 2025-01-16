from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from baixar_audio import download_audio_with_progress

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
        def progress_callback(progress, message, title):
            socketio.emit("progress", {"progress": progress, "message": message, "title": title})

        title = download_audio_with_progress(url, format=format, progress_callback=progress_callback)
        return jsonify({"success": True, "title": title})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    socketio.run(app, debug=True)
