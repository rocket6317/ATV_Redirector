from flask import Flask, jsonify, redirect
import requests
import re

app = Flask(__name__)

ATV_PAGE = "https://www.atv.com.tr/canli-yayin"

def resolve_atv_stream():
    """
    Fetch ATV live page and extract the .m3u8 link.
    """
    resp = requests.get(ATV_PAGE, headers={"User-Agent": "Mozilla/5.0"})
    match = re.search(r'https://[^\s"]+\.m3u8[^\s"]*', resp.text)
    if match:
        return match.group(0)
    return None

@app.route("/atv")
def atv():
    """
    Redirect to the current ATV stream link.
    """
    stream_url = resolve_atv_stream()
    if not stream_url:
        return jsonify({"error": "Could not resolve ATV stream"}), 500
    return redirect(stream_url, code=302)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6288)
