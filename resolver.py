from playwright.sync_api import sync_playwright

ATV_URL = "https://www.atv.com.tr/canli-yayin"

def get_atv_url():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-software-rasterizer",
                "--autoplay-policy=no-user-gesture-required",
                "--disable-blink-features=AutomationControlled"
            ]
        )
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1920, "height": 1080},
            extra_http_headers={
                "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
                "Referer": "https://www.atv.com.tr/",
                "Origin": "https://www.atv.com.tr"
            }
        )
        page = context.new_page()

        final_url = None

        page.on("request", lambda req: print(f"[resolver] Request: {req.method} {req.url}"))
        page.on("response", lambda resp: print(f"[resolver] Response: {resp.url} status={resp.status}"))

        def on_request_finished(request):
            try:
                resp = request.response()
                if not resp:
                    return
                url = resp.url
                if ".m3u8" in url and "st=" in url and "e=" in url:
                    nonlocal final_url
                    final_url = url
                    print("[resolver] >>> Captured signed stream URL:", final_url)
            except Exception as e:
                print("[resolver] Error inspecting request:", e)

        page.on("requestfinished", on_request_finished)

        print("[resolver] Navigating to", ATV_URL)
        page.goto(ATV_URL, timeout=60000)

        page.wait_for_timeout(40000)
        browser.close()

        if not final_url:
            print("[resolver] No signed m3u8 URL captured after timeout")
        return final_url

if __name__ == "__main__":
    url = get_atv_url()
    print("Returned URL:", url)
