from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import math

# Constants
REWARD_URL = "https://rewards.bing.com/"
TOTAL_DAILY_POINTS_PC = 90  
POINTS_PER_SEARCH = 3 

search_queries = [
    "python programming",
    "machine learning",
    "space exploration",
    "quantum computing",
    "artificial intelligence",
]
# Q: Want to add more queries or use an API for dynamic queries?

driver = webdriver.Edge()
wait = WebDriverWait(driver, 10)

try:
    # Navigate to points breakdown page
    driver.get(REWARD_URL + "pointsbreakdown")
    time.sleep(2) 

    points_element = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//a[@id='pointsCounters_pcSearchLevel2_0']/ancestor::div[1]//p[contains(@class, 'pointsDetail') and contains(@class, 'c-subheading-3') and contains(@class, 'ng-binding')]/b",
            )
        )
    )
    current_points = int(points_element.text.strip()) 
    print(f"Current points: {current_points}")

    searches_needed = math.ceil((TOTAL_DAILY_POINTS_PC - current_points) / POINTS_PER_SEARCH)
    print(f"Searches needed: {searches_needed}")


    for i in range(searches_needed):
        # Open new tab
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])

        driver.get("https://www.bing.com/")
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
        query = random.choice(search_queries)
        search_box.send_keys(query + Keys.ENTER)
        print(f"Performed search {i+1}: {query}")

        # Wait on results page
        time.sleep(5)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

finally:
    # Clean up
    driver.quit()