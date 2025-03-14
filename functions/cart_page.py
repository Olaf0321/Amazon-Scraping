import random

def human_pause(page):
    page.wait_for_timeout(random.randint(5000, 10000))

def go_cart_page(page):
    # Wait for the input box to appear before interacting
    search_box = page.wait_for_selector("input[type='text'][id='twotabsearchtextbox']", timeout=0)

    # Click on the search box
    search_box.click()

    human_pause(page)
    search_box.press("Enter")