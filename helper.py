import time

def try_with_retry(action_func, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            return action_func()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            print(f"Attempt {attempt+1} failed, retrying: {e}")
            time.sleep(1)
            
def load_page(driver, wait, url):
    driver.get(url)
    wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
