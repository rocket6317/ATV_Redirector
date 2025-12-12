from flask import Flask, Response
from resolver import get_atv_url

app = Flask(__name__)

@app.route("/atv")
def atv():
    stream_url = get_atv_url()
    if not stream_url:
        return Response("No 1080p stream URL found", status=404)

    m3u_content = f"""#EXTM3U
#EXTINF:-1, ATV Live (1080p)
{stream_url}
"""

    return Response(
        m3u_content,
        mimetype="audio/x-mpegurl",
        headers={
            "Content-Disposition": "attachment; filename=atv.m3u"
        }
    )
