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
        "住所": "",
        "運営責任者名": "",
        "URL": "",
    }
    # Select the element using a class
    element_class = '.sc-grid-content-tail.responsive-grid'
    element = page.query_selector(element_class)
    
    # Check if the element contains the text "出品者"
    if element and "出品者" in element.text_content():
        # Find the span with the desired text and retrieve the href attribute
        selector = 'span:has-text("出品者")'
        element = page.query_selector(selector)
        # Find the <a> tag within the <span> and get the href attribute
        link = element.query_selector('a')
        href = link.get_attribute('href')
        page.goto(f"https://www.amazon.co.jp{href}")

        page.wait_for_timeout(random.randint(500, 1000))

        # Select the parent div element containing the text "特定商取引法に基づく表記"
        selector = 'div:has-text("特定商取引法に基づく表記")'
        seller_info_section = page.query_selector(selector)

        if seller_info_section:
            address = "\n".join(
                [el.inner_text() for el in seller_info_section.query_selector_all('.indent-left span')]
            ) if seller_info_section.query_selector('.indent-left span') else "Not found"

            responsible_person = get_next_sibling_text(seller_info_section.query_selector('span:has-text("運営責任者名:")'))

            result["住所"] = address
            result["運営責任者名"] = responsible_person

            # Select the element using the id
            selector = '#seller-info-storefront-link a'
            seller_store_info = page.query_selector(selector)

            if seller_store_info:
                # Extract the href path from the selected element
                href_path = seller_store_info.get_attribute('href')
                # Go to store page
                page.goto(f"https://www.amazon.co.jp{href_path}")

                # Select the element using the id
                selector = '#apb-desktop-browse-search-see-all'
                see_all = page.query_selector(selector)
                if see_all:
                    # Extract the href path from the selected element
                    href_path = see_all.get_attribute('href')
                    result["URL"] = f"https://www.amazon.co.jp{href_path}"
                    print("correctly get seller info")
                else:
                    print("See all URL not found.")
            else :
                print("Seller store information not found.")
        else:
            print("Seller information section not found.")
    else:
        print("The element does not contain the text '出品者'.")
    return result