import random

def human_pause(page, st, ed):
    page.wait_for_timeout(random.randint(st, ed))

# Function to extract value from table based on the given header text
def get_table_value(page, table_id, header_text):
    table = page.query_selector(f"table#{table_id}")
    if not table:
        return "Table not found"

    rows = table.query_selector_all("tr")
    for row in rows:
        header = row.query_selector("th")
        value = row.query_selector("td")
        if header and value:
            header_text_content = header.inner_text().strip()
            if header_text_content == header_text:
                return value.inner_text().strip()
    return "Not found"

def get_basic_data(page):
    # Scroll randomly like a human
    scroll_amount_sum = 0
    for _ in range(random.randint(2, 4)):
        scroll_amount = random.randint(300, 700)
        scroll_amount_sum += scroll_amount
        page.mouse.wheel(0, scroll_amount)
        human_pause(page, 1000, 3000)
    
    page.mouse.wheel(0, -scroll_amount_sum)
    human_pause(page, 1000, 3000)

    result = {
        "商品名": "",
        "メーカー名": "",
    }

    # Wait for the element to be visible before extracting text
    page.locator("span#productTitle").wait_for(state="visible")

    # Select only the <span> element with id "productTitle"
    product_title = page.locator("span#productTitle").first.text_content()
    result["商品名"] = product_title.strip()

    # Wait for the manufacturer table to be visible
    page.locator("#productDetails_techSpec_section_1").wait_for(state="visible")

    # Extract the "メーカー" information
    manufacturer = get_table_value(page, "productDetails_techSpec_section_1", "メーカー")
    result["メーカー名"] = manufacturer

    print("correctly get basic data!")
    return result