from playwright.sync_api import sync_playwright
from config import SITE_URL
import random

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
        page = browser.new_page()
        page.goto(SITE_URL)
        human_pause(page)

        # Enter ASIN code
        enter_asin_code(page)  # login into Instagram
        human_pause(page)

        while 1:
            click_search_icon(page)
            human_pause(page)

            fill_search_input(page, search_words)
            human_pause(page)

            result = select_unused_link_from_search_results(page)  # Refactor the function properly
            human_pause(page)

            if result == False:
                continue

            # message_button = page.locator("div[role='button']:has-text('Message')")
            # message_button.wait_for(state="visible", timeout=0)

            if validate_user_selection(page, link, keyword) == True:
                human_pause(page)
                # message_button.click()
                print("correctly checked: validate")
            else:
                continue
            human_pause(page)
            send_message(page, message)
            human_pause(page)
            if dms_hours == "50DMs/24Hours":
                # sleep(1728)
                human_pause(page)
            elif dms_hours == "25DMs/12Hours":
                # sleep(1728)
                human_pause(page)
            elif dms_hours == "10DMs/8Hours":
                # sleep(2880)
                human_pause(page)

        browser.close()

    return output_json