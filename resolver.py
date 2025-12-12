from playwright.sync_api import sync_playwright

ATV_URL = "https://www.atv.com.tr/canli-yayin"

def get_atv_url():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        final_url = None

        def on_request_finished(request):
            nonlocal final_url
            resp = request.response()
            if resp:
                url = resp.url
                if ".m3u8" in url and "atv_" in url and "st=" in url and "e=" in url:
                    final_url = url

        page.on("requestfinished", on_request_finished)
        page.goto(ATV_URL, timeout=60000)
        page.wait_for_timeout(25000)
        browser.close()

        return final_url
