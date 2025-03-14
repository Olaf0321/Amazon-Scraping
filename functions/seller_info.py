import random

def human_pause(page, st, ed):
    page.wait_for_timeout(random.randint(st, ed))

# Function to safely extract text content of the next sibling
def get_next_sibling_text(element):
    if element:
        return element.evaluate("el => el.nextSibling ? el.nextSibling.textContent.trim() : 'Not found'")
    return "Not found"

def get_seller_info(page):
    result = {
        "販売業者": "",
        "住所": "",
        "運営責任者名": "",
        "店舗名": "",
        "URL": "",
    }
    # Wait for the element containing the text "出品者" to appear
    selector = 'span:has-text("出品者")'
    page.wait_for_selector(selector, timeout=0)

    # Find the span with the desired text and retrieve the href attribute
    element = page.query_selector(selector)
    
    if element:
        # Find the <a> tag within the <span> and get the href attribute
        link = element.query_selector('a')
        if link:
            href = link.get_attribute('href')
            human_pause(page, 3000, 5000)
            page.goto(f"https://www.amazon.co.jp{href}")

            # Scroll randomly like a human
            scroll_amount_sum = 0
            for _ in range(random.randint(3, 4)):  
                scroll_amount = random.randint(300, 700)
                scroll_amount_sum += scroll_amount
                page.mouse.wheel(0, scroll_amount)
                human_pause(page, 1000, 3000)

            page.mouse.wheel(0, -scroll_amount_sum)
            human_pause(page, 1000, 3000)

            # Wait for the element containing the text "特定商取引法に基づく表記"
            selector = 'div:has-text("特定商取引法に基づく表記")'
            page.wait_for_selector(selector)

            # Select the parent div element containing the text "特定商取引法に基づく表記"
            seller_info_section = page.query_selector(selector)

            if seller_info_section:
                # Extract information using the helper function
                seller_name = get_next_sibling_text(seller_info_section.query_selector('span:has-text("販売業者:")'))
                address = "\n".join(
                    [el.inner_text() for el in seller_info_section.query_selector_all('.indent-left span')]
                ) if seller_info_section.query_selector('.indent-left span') else "Not found"
                responsible_person = get_next_sibling_text(seller_info_section.query_selector('span:has-text("運営責任者名:")'))
                store_name = get_next_sibling_text(seller_info_section.query_selector('span:has-text("店舗名:")'))

                result["販売業者"] = seller_name
                result["住所"] = address
                result["運営責任者名"] = responsible_person
                result["店舗名"] = store_name
            else:
                print("Seller information section not found.")

            # Select the element using the id
            selector = '#seller-info-storefront-link a'
            page.wait_for_selector(selector, timeout=0)
            element = page.query_selector(selector)

            # Extract the href path from the selected element
            href_path = element.get_attribute('href')

            human_pause(page, 3000, 5000)
            page.goto(f"https://www.amazon.co.jp{href_path}")

            # Select the element using the id
            selector = '#apb-desktop-browse-search-see-all'
            page.wait_for_selector(selector, timeout=0)
            element = page.query_selector('#apb-desktop-browse-search-see-all')

            # Extract the href path from the selected element
            href_path = element.get_attribute('href')
            result["URL"] = f"https://www.amazon.co.jp{href_path}"
            human_pause(page, 3000, 5000)
        else:
            print("No link found inside the span.")
    else:
        print("No span containing '出品者' found.")
    return result