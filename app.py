import yt_dlp
from flask import Flask, jsonify, redirect

app = Flask(__name__)

ATV_URL = "https://www.atv.com.tr/canli-yayin"

def resolve_atv_stream():
    """
    Use yt-dlp to extract the current ATV stream URL.
    """
    ydl_opts = {"quiet": True, "skip_download": True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(ATV_URL, download=False)
            return info.get("url")
    except Exception as e:
        print(f"Error resolving ATV stream: {e}")
        return None

@app.route("/atv")
def atv():
    stream_url = resolve_atv_stream()
    if not stream_url:
        return jsonify({"error": "Could not resolve ATV stream"}), 500
    return redirect(stream_url, code=302)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6288)
