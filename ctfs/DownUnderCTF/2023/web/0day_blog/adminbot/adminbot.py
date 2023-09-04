from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import logging, os, time
from queue import Queue

USERNAME = "ghostccamm"
# Password is different on challenge instance
PASSWORD = "hmmmm idk what would be good for a passw0rd..."
DRUPAL_HOST = os.environ["DRUPAL_HOST"]

admin_queue = Queue(maxsize=5)
logging.basicConfig(level=logging.INFO)

def get_driver() -> webdriver.Chrome:
    service = Service(executable_path='/usr/bin/chromedriver')
    chrome_args = [
        '--headless',
        '--incognito'
	]

    chrome_options = webdriver.ChromeOptions()
    
    for arg in chrome_args:
        chrome_options.add_argument(arg)
    
    return webdriver.Chrome(service=service, options=chrome_options)


def login(driver: webdriver.Chrome) -> webdriver.Chrome:
    driver.get(f"{DRUPAL_HOST}/user/login")
    time.sleep(1)
    logging.info("logging into website")
    user_input = driver.find_element(By.ID, "edit-name")
    user_input.send_keys(USERNAME)
    pass_input = driver.find_element(By.ID, "edit-pass")
    pass_input.send_keys(PASSWORD)

    submit_button = driver.find_element(By.ID, 'edit-submit')
    submit_button.click()
    time.sleep(5)
    return driver

def timeout_handler():
    raise Exception('Timeout!')

def visit_url(url: str):
    driver = None
    try:
        logging.info("initiating adminbot")
        driver = get_driver()
        driver = login(driver)
        logging.info('visiting {}'.format(url))
        driver.get(url)
            
        time.sleep(10)
    except Exception as _e:
        pass
    finally:
        if not driver is None:
            driver.quit()
        logging.info("done")


def send_the_admin(url):
    visit_url(url)


def worker():
    while True:
        try:
            url = admin_queue.get()[0]
            send_the_admin(url)
        except Exception as e:
            logging.error(e)

        # Only process 1 URL every minute
        time.sleep(60)