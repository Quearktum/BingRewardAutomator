from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time
import math


from config import TIMEOUT, WAIT_TIME


def reward_search(search_queries, driver):
    wait = WebDriverWait(driver, TIMEOUT)

    completed_searches = 0

    try:
        for search_query in search_queries:
            try:
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[-1])

                driver.get("https://www.bing.com/")
                search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))

                search_box.send_keys(search_query + Keys.ENTER)
                print(f"Performed search: {search_query}")

                # Wait on results page
                time.sleep(WAIT_TIME)

                driver.close()
                driver.switch_to.window(driver.window_handles[0])

                completed_searches += 1

            except Exception as e:
                print(f"Error during search '{search_query}': {e}")
                return completed_searches

        print(f"Completed {completed_searches} out of {len(search_queries)} searches.")
        return completed_searches

    except Exception as e:
        print(f"Fatal error: {e}")
        return completed_searches
