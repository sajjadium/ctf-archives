from selenium import webdriver
from selenium.webdriver.common.by import By
# import chromedriver_binary
from threading import Thread
import time


def run_bot(user, password):
    thread = Thread(target=run, args=(user, password))
    thread.daemon = True
    thread.start()


def run(user, password):
    time.sleep(2)

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17')
    # TODO: remove this line
    options.add_argument('--disable-web-security')  # CORS bypass for testing

    while True:
        try:
            driver = webdriver.Chrome(options=options)
            driver.get("http://127.0.0.1:8000/")
            # populate the form
            driver.find_element(By.ID, "user").send_keys(user)
            driver.find_element(By.ID, "password").send_keys(password)
            # submit the form
            driver.find_element(By.ID, "submit").click()
            # wait for the page to load
            time.sleep(2)
            # print the page source
            while True:
                # check if the page has changed
                if driver.current_url != "http://127.0.0.1:8000/dashboard":
                    driver.get("http://127.0.0.1:8000/dashboard")
                else:
                    time.sleep(30)
                    driver.refresh()
        except Exception as e:
            print(e)
            time.sleep(10)
            pass
