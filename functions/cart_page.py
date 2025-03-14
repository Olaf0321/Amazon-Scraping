import random
from config import CART_URL

def human_pause(page, st, ed):
    page.wait_for_timeout(random.randint(st, ed))

def go_cart_page(page):
    # Wait for the input box to appear before interacting
    search_box_selector = "input[type='text'][id='twotabsearchtextbox']"
    search_box = page.wait_for_selector(search_box_selector, timeout=0)

    # Click on the search box
    search_box.click()
    search_box.press("Enter")

    # Wait until the button with the given ID appears
    page.wait_for_selector("#a-autoid-1-announce", state="visible", timeout=0)
    human_pause(page, 1000, 3000)

    # Click the button using its ID
    page.locator("#a-autoid-1-announce").click()
    human_pause(page, 3000, 5000)

    page.goto(CART_URL)