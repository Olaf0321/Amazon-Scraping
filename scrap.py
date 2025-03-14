import random
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from config import SITE_URL, CART_URL, USER_AGENT
from functions.enter_asin_code import enter_asin_code
from functions.detail_page import go_detail_page
from functions.basic_data import get_basic_data
from functions.cart_page import go_cart_page

def human_pause(page):
    page.wait_for_timeout(random.randint(800, 3000))

# Function to safely extract text content of the next sibling
def get_next_sibling_text(element):
    if element:
        return element.evaluate("el => el.nextSibling ? el.nextSibling.textContent.trim() : 'Not found'")
    return "Not found"

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
        human_pause(page)

        # Wait until the button with the given ID appears
        page.wait_for_selector("#a-autoid-1-announce", state="visible", timeout=30000)

        # Click the button using its ID
        page.locator("#a-autoid-1-announce").click()
        human_pause(page)

        page.goto(CART_URL)

        # Find the span with the desired text and retrieve the href attribute
        element = page.query_selector('span:has-text("出品者")')
        
        if element:
            # Find the <a> tag within the <span> and get the href attribute
            link = element.query_selector('a')
            if link:
                href = link.get_attribute('href')
                print("Found href:", href)
                page.goto(f"https://www.amazon.co.jp{href}")
                # Select the parent div element containing the text "特定商取引法に基づく表記"
                seller_info_section = page.query_selector('div:has-text("特定商取引法に基づく表記")')

                if seller_info_section:
                    # Extract information using the helper function
                    seller_name = get_next_sibling_text(seller_info_section.query_selector('span:has-text("販売業者:")'))
                    address = "\n".join(
                        [el.inner_text() for el in seller_info_section.query_selector_all('.indent-left span')]
                    ) if seller_info_section.query_selector('.indent-left span') else "Not found"
                    responsible_person = get_next_sibling_text(seller_info_section.query_selector('span:has-text("運営責任者名:")'))
                    store_name = get_next_sibling_text(seller_info_section.query_selector('span:has-text("店舗名:")'))

                    # Print the extracted information
                    output_json["販売業者"] = seller_name
                    output_json["住所"] = address
                    output_json["運営責任者名"] = responsible_person
                    output_json["店舗名"] = store_name
                else:
                    print("Seller information section not found.")

                page.wait_for_timeout(random.randint(10000, 30000))

                # Select the element using the id
                element = page.query_selector('#seller-info-storefront-link a')

                # Extract the href path from the selected element
                href_path = element.get_attribute('href')
                
                print(f"Href path: {href_path}")
                page.goto(f"https://www.amazon.co.jp{href_path}")

                # Select the element using the id
                element = page.query_selector('#apb-desktop-browse-search-see-all')

                # Extract the href path from the selected element
                href_path = element.get_attribute('href')
                output_json["URL"] = f"https://www.amazon.co.jp{href_path}"

                page.wait_for_timeout(random.randint(10000, 30000))
            else:
                print("No link found inside the span.")
        else:
            print("No span containing '出品者' found.")
        
        browser.close()

    return output_json