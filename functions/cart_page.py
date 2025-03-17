import random
from config import CART_URL

def go_cart_page(page):
    page.locator("#a-autoid-1-announce").click()
    page.wait_for_timeout(random.randint(500, 1000))
    page.goto(CART_URL)
    return page