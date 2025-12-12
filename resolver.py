from playwright.sync_api import sync_playwright

ATV_URL = "https://www.atv.com.tr/canli-yayin"

def resolve_final_cdn_url():
    with sync_playwright() as p:
        # headless=True for container use; set False if you want to see the browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        final_url = None

        # Log every request
        def on_request(request):
            print(f"[resolver] Request: {request.method} {request.url}")

        # Log finished requests and capture signed m3u8
        def on_request_finished(request):
            try:
                resp = request.response()
                if not resp:
                    return
                url = resp.url
                status = resp.status
                print(f"[resolver] Finished: {url} (status {status})")
                if (
                    ".m3u8" in url
                    and "st=" in url
                    and "e=" in url
                ):
                    nonlocal final_url
                    final_url = url
                    print("[resolver] >>> Captured signed stream URL:", final_url)
            except Exception as e:
                print("[resolver] Error inspecting request:", e)

        page.on("request", on_request)
        page.on("requestfinished", on_request_finished)

        print("[resolver] Navigating to", ATV_URL)
        page.goto(ATV_URL, timeout=60000)

        # Allow time for player to initialise and request playlists
        page.wait_for_timeout(40000)

        browser.close()

        if not final_url:
            print("[resolver] No signed m3u8 URL captured after timeout")

if __name__ == "__main__":
    resolve_final_cdn_url()
