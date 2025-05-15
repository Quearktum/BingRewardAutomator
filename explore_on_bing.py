import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import REWARD_URL, TIMEOUT, WAIT_TIME
from helper import try_with_retry, load_page, find_search_box
from search_query import explore_on_bing_query, execute_prompt


def explore_on_bing(driver):
    wait = WebDriverWait(driver, TIMEOUT)

    try:
        try_with_retry(lambda: load_page(driver, wait, REWARD_URL))
        
        wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ds-card-sec .ng-scope"))
        )
        
        tasks = driver.find_elements(By.CSS_SELECTOR, "#explore-on-bing .mee-icon-AddMedium")
        print(f"Found {len(tasks)} task(s) in Explore on Bing")
        
        for task in tasks:
            try:
                task_link = task.find_element(By.XPATH, "./ancestor::a")
                
                # Get the search query
                task_text = task_link.find_element(By.CSS_SELECTOR, ".c-paragraph-4") \
                           .text.removeprefix("Search on Bing for ")
                query = execute_prompt(explore_on_bing_query(task_text))
                
                task_link.click()
                driver.switch_to.window(driver.window_handles[-1])
                
                search_box = try_with_retry(lambda: find_search_box(driver, wait))
                search_box.clear()
                search_box.send_keys(query[0])
                time.sleep(0.2)
                search_box.send_keys(Keys.ENTER)
                
                time.sleep(WAIT_TIME)
                
                print(f"Performed search: {query[0]}")
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                
            except Exception as e:
                print(f"Error processing task: {e}")
                continue  # Changed from break to continue to process other tasks
                
        return "Explore on Bing tasks completed successfully."
        
    except Exception as e:
        print(f"Error completing Explore on Bing: {e}")
        return None