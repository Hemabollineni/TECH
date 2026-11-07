
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.maximize_window()

wait = WebDriverWait(driver, 20)

driver.get("https://www.amazon.in")

# Find search box
search_box = wait.until(
    EC.element_to_be_clickable(
        (By.ID, "twotabsearchtextbox")
    )
)

# Search for iPhone
search_box.send_keys("iPhone")
search_box.send_keys(Keys.ENTER)

# Wait for search results
wait.until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, "[data-component-type='s-search-result']")
    )
)

# Find all product containers
products = driver.find_elements(
    By.CSS_SELECTOR,
    "[data-component-type='s-search-result']"
)

print("\nIPHONE SEARCH RESULTS\n")

count = 0

for product in products:

    try:
        name = product.find_element(
            By.CSS_SELECTOR,
            "h2 span"
        ).text

        try:
            price = product.find_element(
                By.CSS_SELECTOR,
                ".a-price .a-offscreen"
            ).text
        except:
            price = "Price not available"

        print("Product:", name)
        print("Price:", price)
        print("-" * 50)

        count += 1

        if count == 10:
            break

    except:
        continue

driver.quit()
