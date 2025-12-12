from playwright.sync_api import sync_playwright
import sys

ATV_URL = "https://www.atv.com.tr/canli-yayin"

def get_atv_url():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        final_url = None

        def on_request_finished(request):
            nonlocal final_url
            try:
                resp = request.response()
                if not resp:
                    return
                url = resp.url
                # Log every request to stdout (Portainer will capture this)
                print(f"[resolver] Saw request: {url}", file=sys.stdout, flush=True)

                # Look for signed playlist
                if ".m3u8" in url and "st=" in url and "e=" in url:
                    final_url = url
                    print(f"[resolver] Captured signed m3u8: {final_url}", file=sys.stdout, flush=True)
            except Exception as e:
                print(f"[resolver] Error inspecting request: {e}", file=sys.stderr, flush=True)

        page.on("requestfinished", on_request_finished)
        page.goto(ATV_URL, timeout=60000)
        page.wait_for_timeout(60000)  # wait long enough for signed URL
        browser.close()

        if not final_url:
            print("[resolver] No signed m3u8 URL captured", file=sys.stderr, flush=True)
        return final_url
