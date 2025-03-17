import random

def enter_asin_code(page, asin_code):
    # Click on the search box
    search_box_selector = "input[type='text'][id='twotabsearchtextbox']"
    search_box = page.locator(search_box_selector)
    search_box.click()
    
    page.wait_for_timeout(random.randint(100, 200))

    for _ in range(20):  # Adjust based on text length
        search_box.press("Backspace")
    
    # Optionally, type some text
    for char in asin_code:
        page.keyboard.press(char)
        page.wait_for_timeout(random.randint(100, 200))
    
    # Press Enter to search
    search_box.press("Enter")
    print("correctly searched")
    return True