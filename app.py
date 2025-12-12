from flask import Flask, Response
from resolver import get_atv_urls

app = Flask(__name__)

@app.route("/atv")
def atv():
    urls = get_atv_urls()
    if not urls:
        return Response("No stream URLs found", status=404)

    # Use the last captured URL (most recent)
    stream_url = urls[-1]

    # Build M3U content
    m3u_content = f"""#EXTM3U
#EXTINF:-1, ATV Live
{stream_url}
"""

    return Response(
        m3u_content,
        mimetype="audio/x-mpegurl",
        headers={
            "Content-Disposition": "attachment; filename=atv.m3u"
        }
    )
