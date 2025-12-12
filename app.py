from flask import Flask, redirect
from resolver import get_atv_url

app = Flask(__name__)

@app.route("/atv")
def atv():
    url = get_atv_url()
    if url:
        return redirect(url, code=302)
    return "Failed to resolve ATV stream", 500

@app.route("/health")
def health():
    return "OK", 200
