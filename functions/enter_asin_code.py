import random

def human_pause(page, st, ed):
    page.wait_for_timeout(random.randint(st, ed))

def enter_asin_code(page, asin_code):
    # Wait for the input box to appear before interacting
    search_box_selector = "input[type='text'][id='twotabsearchtextbox']"
    search_box = page.wait_for_selector(search_box_selector, timeout=0)
    # Scroll randomly like a human
    scroll_amount_sum = 0
    for _ in range(random.randint(3, 6)):  
        scroll_amount = random.randint(300, 700)
        scroll_amount_sum += scroll_amount
        page.mouse.wheel(0, scroll_amount)
        human_pause(page, 1000, 3000)

    page.mouse.wheel(0, -scroll_amount_sum)
    human_pause(page, 1000, 3000)

    # Click on the search box
    search_box.click()
    human_pause(page, 1000, 3000)
    
    # Optionally, type some text
    for char in asin_code:
        page.keyboard.press(char)
        page.wait_for_timeout(random.randint(100, 200))

    human_pause(page, 1000, 3000)
    
    # Press Enter to search
    search_box.press("Enter")
    print("correctly searched")
    return True