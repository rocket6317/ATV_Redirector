from playwright.sync_api import sync_playwright

ATV_URL = "https://www.atv.com.tr/canli-yayin"

def get_atv_url():
    with sync_playwright() as p:
        # Use headless=False if you want to replicate your working script exactly.
        browser = p.chromium.launch(headless=False, args=["--no-sandbox", "--disable-dev-shm-usage"])
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
                # Same conditions as your working script
                if (
                    ".m3u8" in url
                    and "atv_" in url
                    and "st=" in url
                    and "e=" in url
                ):
                    final_url = url
                    print("[resolver] >>> Final stream URL:", final_url)
            except Exception:
                pass

        page.on("requestfinished", on_request_finished)

        print("[resolver] Navigating to", ATV_URL)
        page.goto(ATV_URL, timeout=60000)

        # Allow time for player to initialize and request playlists
        page.wait_for_timeout(25000)

        browser.close()

        if not final_url:
            print("[resolver] No signed CDN stream URL captured")
        return final_url
