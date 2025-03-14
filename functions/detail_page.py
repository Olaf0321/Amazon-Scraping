import random

def human_pause(page):
    page.wait_for_timeout(random.randint(5000, 10000))

def go_detail_page(page):
    # Wait until all product links are loaded
    product_selector = "a.a-link-normal.s-line-clamp-4.s-link-style.a-text-normal"
    page.wait_for_selector(product_selector, timeout=0)

    # Scroll randomly like a human
    for _ in range(random.randint(3, 6)):  
        scroll_amount = random.randint(300, 700)
        page.mouse.wheel(0, scroll_amount)
        human_pause(page)

    # Wait for the a link to be visible using class
    links = page.query_selector_all(product_selector)

    # Extract and print href attributes
    hrefs = [link.get_attribute("href") for link in links if link.get_attribute("href")]

    human_pause(page)
    for href in hrefs:
        print(href)
        page.goto(f"https://www.amazon.co.jp{href}", timeout=0)
        break
    
    return page