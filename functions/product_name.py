def get_product_name(page) :
    result = ""
    # Define the class selector
    class_selector = "a.a-link-normal.s-line-clamp-4.s-link-style.a-text-normal"
    # Wait for the elements to load
    page.wait_for_selector(class_selector, timeout=5000)

    # Find all 'a' tags with the specified class
    a_tags = page.locator(class_selector)
    print(a_tags)

    print(f"Count: {a_tags.count()}")

    if a_tags.count() > 0:
        result = a_tags.nth(0).locator('h2').inner_text()
    print(f"商品名: {result}")
    return result