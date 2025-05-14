import time
import math
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from config import REWARD_URL, TOTAL_DAILY_POINTS_PC, POINTS_PER_SEARCH, TIMEOUT


def num_search_need(driver):
    wait = WebDriverWait(driver, TIMEOUT)

    try:
        # Navigate to points breakdown page
        driver.get(REWARD_URL + "pointsbreakdown")

        points_element = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//a[@id='pointsCounters_pcSearchLevel2_0']/ancestor::div[1]//p[contains(@class, 'pointsDetail') and contains(@class, 'c-subheading-3') and contains(@class, 'ng-binding')]/b",
                )
            )
        )
        time.sleep(1)
        print(f"Points string: {points_element.text}")
        current_points = int(points_element.text) 
        searches_needed = math.ceil(
            (TOTAL_DAILY_POINTS_PC - current_points) / POINTS_PER_SEARCH
        )
        
        print(f"Searches needed: {searches_needed}")

        return searches_needed

    except Exception as e:
        print(f"Error getting number search needed: {e}")
        return 0
