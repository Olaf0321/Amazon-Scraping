import random

def human_pause(page, st, ed):
    page.wait_for_timeout(random.randint(st, ed))

def go_cart_page(page):
    # Wait for the input box to appear before interacting
    search_box_selector = "input[type='text'][id='twotabsearchtextbox']"
    search_box = page.wait_for_selector(search_box_selector, timeout=0)

    # Click on the search box
    search_box.click()
    human_pause(page, 1000, 2000)
    search_box.press("Enter")