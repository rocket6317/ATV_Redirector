import requests
import re
from flask import Flask, jsonify, redirect

app = Flask(__name__)

ATV_PAGE = "https://www.atv.com.tr/canli-yayin"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://www.atv.com.tr/",
    "Origin": "https://www.atv.com.tr",
    "Accept": "*/*",
}

def resolve_atv_stream():
    """
    Fetch ATV live page with browser-like headers and extract the .m3u8 link.
    """
    try:
        resp = requests.get(ATV_PAGE, headers=HEADERS, timeout=10)
        match = re.search(r'https://[^\s"]+\.m3u8[^\s"]*', resp.text)
        if match:
            return match.group(0)
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
