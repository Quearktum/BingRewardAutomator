from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from num_search_need import num_search_need
from search_query import get_search_query, execute_prompt
from daily_sets import daily_sets
from more_activities import more_activities
from reward_search import reward_search


search_queries = [] 

if __name__ == "__main__":  
    driver = webdriver.Edge()
    
    # TO-DO: Explore on Bing with id="explore-on-bing" <a>class="ds-card-sec ng-scope"
    
    # Complete daily sets
    daily_sets(driver)
    
    # Complete More Activities
    more_activities(driver)
    
    # Daily PC Search
    search_times = num_search_need(driver)
    
    if (search_times > 0):
        prompt = get_search_query(search_times)
        search_queries = execute_prompt(prompt)
        
        reward_search(search_queries, driver)
    
    # Cleanup
    print("Job completed, quitting...")
    driver.quit()
