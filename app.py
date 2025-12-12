from flask import Flask, redirect
from resolver import get_atv_url
import sys

app = Flask(__name__)

@app.route("/atv")
def atv():
    print("[app] /atv endpoint called", file=sys.stdout, flush=True)
    url = get_atv_url()
    if url:
        print(f"[app] Redirecting to {url}", file=sys.stdout, flush=True)
        return redirect(url, code=302)
    print("[app] Failed to resolve ATV stream", file=sys.stderr, flush=True)
    return "Failed to resolve ATV stream", 500

@app.route("/health")
def health():
    print("[app] /health endpoint called", file=sys.stdout, flush=True)
    return "OK", 200
