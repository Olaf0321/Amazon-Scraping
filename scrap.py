import random
from functions.enter_asin_code import enter_asin_code
from functions.cart_page import go_cart_page
from functions.seller_info import get_seller_info
from functions.product_name import get_product_name

def human_pause(page):
    page.wait_for_timeout(random.randint(800, 3000))

def scrap_info(page, asin_code, st, cur):
    output_json = {
        "ASIN": asin_code,
        "商品名": "",
        "住所": "",
        "運営責任者名": "",
        "URL": ""
    }
    
    try:
        if st != cur: page.go_back()
        human_pause(page)
        # Enter ASIN code
        enter_asin_code(page, asin_code)

        # Get product name
        output_json["商品名"] = get_product_name(page)

        human_pause(page)

        # Go to cart page
        page = go_cart_page(page)

        human_pause(page)

        # Get seller info
        result = get_seller_info(page)
        output_json["住所"] = result.get("住所", "")
        output_json["運営責任者名"] = result.get("運営責任者名", "")
        output_json["URL"] = result.get("URL", "")

        human_pause(page)
    except TimeoutError:
        print("Error: Timeout occurred while loading the page.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return output_json