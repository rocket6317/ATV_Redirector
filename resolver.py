from playwright.sync_api import sync_playwright

ATV_URL = "https://www.atv.com.tr/canli-yayin"

def get_atv_url():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,  # try False if still no URL
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
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
                if ".m3u8" in url:
                    print("[resolver] >>> Captured m3u8:", url)
                    if "1080p" in url:
                        final_url = url
            except Exception:
                pass

        page.on("requestfinished", on_request_finished)

        print("[resolver] Navigating to", ATV_URL)
        page.goto(ATV_URL, timeout=60000, wait_until="domcontentloaded")

        page.wait_for_timeout(25000)  # give player time

        browser.close()

        if not final_url:
            print("[resolver] No 1080p m3u8 URL captured")
        return final_url
