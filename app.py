# app.py
import logging
import time
from flask import Flask, jsonify, redirect
from playwright.sync_api import sync_playwright

app = Flask(__name__)

# Structured logging to stdout for Portainer
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

ATV_URL = "https://www.atv.com.tr/canli-yayin"

# Match headers you captured from DevTools (mobile UA helps)
BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36",
    "Accept": "*/*",
    "Referer": "https://www.atv.com.tr/",
    "Origin": "https://www.atv.com.tr",
}

def resolve_atv_stream(max_wait_ms=25000, retries=2):
    """
    Launch headless Chromium, load ATV live page, and capture the first .m3u8 network request.
    Returns the signed .m3u8 URL or None.
    """
    attempt = 0
    while attempt <= retries:
        attempt += 1
        logging.info("Resolving ATV stream (attempt %d/%d)", attempt, retries + 1)
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True, args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                ])
                context = browser.new_context(
                    user_agent=BROWSER_HEADERS["User-Agent"],
                    extra_http_headers=BROWSER_HEADERS,
                    locale="tr-TR",
                )
                page = context.new_page()

                # Log requests for visibility
                def log_request(req):
                    if ".m3u8" in req.url:
                        logging.info("Observed .m3u8 request: %s", req.url)
                page.on("request", log_request)

                logging.info("Navigating to %s", ATV_URL)
                page.goto(ATV_URL, timeout=60000, wait_until="domcontentloaded")

                # Some sites require a brief delay to let the player bootstrap
                start = time.time()
                logging.info("Waiting for .m3u8 network request up to %d ms", max_wait_ms)
                try:
                    req = page.wait_for_request(
                        lambda r: ".m3u8" in r.url,
                        timeout=max_wait_ms
                    )
                    stream_url = req.url
                    logging.info("Resolved stream URL: %s", stream_url)
                    browser.close()
                    return stream_url
                except Exception as e:
                    logging.warning("No .m3u8 seen within %d ms (elapsed=%.1fs): %s",
                                    max_wait_ms, time.time() - start, e)
                    browser.close()
        except Exception as e:
            logging.exception("Playwright failure on attempt %d: %s", attempt, e)

        if attempt <= retries:
            backoff = 2 * attempt
            logging.info("Retrying after %ds...", backoff)
            time.sleep(backoff)

    logging.error("Failed to resolve ATV stream after %d attempts", retries + 1)
    return None

@app.route("/atv")
def atv():
    logging.info("Incoming request to /atv")
    stream_url = resolve_atv_stream()
    if not stream_url:
        logging.error("Could not resolve ATV stream")
        return jsonify({"error": "Could not resolve ATV stream"}), 500
    logging.info("Redirecting to stream: %s", stream_url)
    return redirect(stream_url, code=302)

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    # Use 0.0.0.0 so Portainer/Gluetun can expose it
    app.run(host="0.0.0.0", port=6288)
