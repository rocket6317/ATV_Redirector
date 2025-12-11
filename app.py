import logging
import time
from flask import Flask, jsonify, redirect
from playwright.sync_api import sync_playwright

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

ATV_URL = "https://www.atv.com.tr/canli-yayin"

def resolve_atv_stream():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page()
        page.goto(ATV_URL, timeout=60000)
        try:
            req = page.wait_for_request(lambda r: ".m3u8" in r.url, timeout=20000)
            stream_url = req.url
            logging.info("Resolved ATV stream: %s", stream_url)
            browser.close()
            return stream_url
        except Exception as e:
            logging.error("Failed to resolve ATV stream: %s", e)
            browser.close()
            return None

@app.route("/")
def index():
    return jsonify({"message": "ATV Redirector running", "endpoints": ["/atv", "/health"]})

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/atv", strict_slashes=False)
def atv():
    stream_url = resolve_atv_stream()
    if not stream_url:
        return jsonify({"error": "Could not resolve ATV stream"}), 500
    return redirect(stream_url, code=302)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6288)
