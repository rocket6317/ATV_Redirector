from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from playwright.sync_api import sync_playwright

ATV_URL = "https://www.atv.com.tr/canli-yayin"

def clean_url(url: str) -> str:
    """Remove &app=... and &ce=... from query string."""
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    qs.pop("app", None)
    qs.pop("ce", None)
    new_query = urlencode(qs, doseq=True)
    return urlunparse(parsed._replace(query=new_query))

def get_atv_urls():
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

        urls = []

        def on_request_finished(request):
            try:
                resp = request.response()
                if not resp:
                    return
                url = resp.url
                if ".m3u8" in url:
                    cleaned = clean_url(url)
                    urls.append(cleaned)
                    print("[resolver] >>> Captured m3u8 stream URL:", cleaned)
            except Exception as e:
                print("[resolver] Error inspecting request:", e)

        page.on("requestfinished", on_request_finished)

        print("[resolver] Navigating to", ATV_URL)
        page.goto(ATV_URL, timeout=60000)

        page.wait_for_timeout(40000)
        browser.close()

        if not urls:
            print("[resolver] No m3u8 URLs captured after timeout")
        return urls

if __name__ == "__main__":
    urls = get_atv_urls()
    print("Returned URLs:", urls)
