import random
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from config import SITE_URL, CART_URL, USER_AGENT
from functions.enter_asin_code import enter_asin_code
from functions.detail_page import go_detail_page
from functions.basic_data import get_basic_data
from functions.cart_page import go_cart_page
from functions.seller_info import get_seller_info

def human_pause(page):
    page.wait_for_timeout(random.randint(800, 3000))

def scrap_info(asin_code):
    output_json = {
        "ASIN": asin_code,
        "商品名": "",
        "メーカー名": "",
        "販売業者": "",
        "住所": "",
        "運営責任者名": "",
        "店舗名": "",
        "URL": ""
    }
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent=USER_AGENT,
            viewport={"width": random.randint(1200, 1400), "height": random.randint(700, 900)}
        )
        page = context.new_page()
        page = browser.new_page()
        stealth_sync(page)
        page.goto(SITE_URL, timeout=0)

        # Enter ASIN code
        enter_asin_code(page, asin_code)

        # Go to detail page
        page = go_detail_page(page)

        basic_data = get_basic_data(page)

        output_json["商品名"] = basic_data.get("商品名", "")
        output_json["メーカー名"] = basic_data.get("メーカー名", "")

        go_cart_page(page)

        result = get_seller_info(page)
        output_json["販売業者"] = result.get("販売業者", "")
        output_json["住所"] = result.get("住所", "")
        output_json["運営責任者名"] = result.get("運営責任者名", "")
        output_json["店舗名"] = result.get("店舗名", "")
        output_json["URL"] = result.get("URL", "")
        
        browser.close()

    return output_json