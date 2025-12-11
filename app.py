import requests
import re
import logging
from flask import Flask, jsonify, redirect

app = Flask(__name__)

# Configure logging to stdout (Portainer will capture this)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

ATV_PAGE = "https://www.atv.com.tr/canli-yayin"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://www.atv.com.tr/",
    "Origin": "https://www.atv.com.tr",
    "Accept": "*/*",
}

def resolve_atv_stream():
    logging.info("Fetching ATV page: %s", ATV_PAGE)
    try:
        resp = requests.get(ATV_PAGE, headers=HEADERS, timeout=10)
        logging.info("ATV page status: %s", resp.status_code)
        if resp.status_code != 200:
            logging.warning("Failed to fetch ATV page, status=%s", resp.status_code)
            return None

        # Log a snippet of the HTML for debugging
        logging.debug("ATV page snippet: %s", resp.text[:500])

        match = re.search(r'https://[^\s"]+\.m3u8[^\s"]*', resp.text)
        if match:
            stream_url = match.group(0)
            logging.info("Resolved stream URL: %s", stream_url)
            return stream_url
        else:
            logging.warning("No .m3u8 link found in ATV page HTML")
    except Exception as e:
        logging.exception("Error resolving ATV stream")
    return None

@app.route("/atv")
def atv():
    logging.info("Incoming request to /atv")
    stream_url = resolve_atv_stream()
    if not stream_url:
        logging.error("Could not resolve ATV stream")
        return jsonify({"error": "Could not resolve ATV stream"}), 500
    logging.info("Redirecting client to stream: %s", stream_url)
    return redirect(stream_url, code=302)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6288)
