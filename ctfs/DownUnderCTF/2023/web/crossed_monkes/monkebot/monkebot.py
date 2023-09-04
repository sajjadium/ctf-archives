from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging, os, time
from queue import Queue

monke_queue = Queue(maxsize=5)
monkestorage_host = os.environ.get("MONKESTORAGE_HOST", "http://monkestorage:3000")
logging.basicConfig(level=logging.INFO)

BUTTON_CLICK_TIMEOUT = 5
MAX_VISIT_TIME = 60
WAIT_ITERATIONS = MAX_VISIT_TIME // BUTTON_CLICK_TIMEOUT

# if monke see tab then switch
# but if monke sees too many tabs then no.
# too lazy they will go eat banana
MAX_TAB_SWITCH = 1

def get_driver() -> webdriver.Chrome:
    chrome_args = [
        '--headless',
		'--no-sandbox',
        '--disable-dev-shm-usage',
		'--disable-background-networking',
		'--disable-default-apps',
		'--disable-extensions',
		'--disable-gpu',
		'--disable-sync',
		'--disable-translate',
		'--hide-scrollbars',
		'--metrics-recording-only',
		'--mute-audio',
		'--no-first-run',
		'--safebrowsing-disable-auto-update',
		'--js-flags=--noexpose_wasm,--jitless',
        '--disable-web-security'
	]

    chrome_options = webdriver.ChromeOptions()
    
    for arg in chrome_args:
        chrome_options.add_argument(arg)
    
    return webdriver.Chrome(options=chrome_options)


def login(driver: webdriver.Chrome, cleanup_id: str) -> webdriver.Chrome:
    driver.get(monkestorage_host)
    time.sleep(1)
    logging.info("logging into website")
    user_input = driver.find_element(By.ID, "username")
    user_input.send_keys(os.environ['ADMIN_USERNAME'])
    pass_input = driver.find_element(By.ID, "password")
    pass_input.send_keys(os.environ['ADMIN_PASSWORD'])
    # Needed to add in cleanup script ID
    driver.execute_script("document.getElementById('cleanup_id').removeAttribute('hidden')")
    cleanup_input = driver.find_element(By.ID, "cleanup_id")
    cleanup_input.send_keys(cleanup_id)
    submit_button = driver.find_element(By.ID, 'submit-login')
    submit_button.click()
    time.sleep(1)
    return driver


def cleanup(cleanup_id: str):
    driver = None

    try:
        logging.info("cleaning up monke mess")
        driver = get_driver()
        driver = login(driver, cleanup_id)
        driver.get(f"{monkestorage_host}/cleanup?cleanup_id={cleanup_id}")
        time.sleep(5)
    finally:
        if not driver is None:
            driver.quit()
        logging.info("done cleaning")


def visit_url(url: str, cleanup_id: str):
    total_tab_switch = 0
    driver = None
    try:
        logging.info("initiating monkebot")
        driver = get_driver()
        driver = login(driver, cleanup_id)
        logging.info('visiting {}'.format(url))
        driver.get(url)

        for _i in range(WAIT_ITERATIONS):
            try:
                WebDriverWait(driver, BUTTON_CLICK_TIMEOUT).until(
                    EC.presence_of_element_located((By.TAG_NAME, "button"))
                )
                button_element = driver.find_element(By.TAG_NAME, "button")
                # Monke see button, monke click button
                button_element.click()
            except Exception as e:
                pass

            if total_tab_switch < MAX_TAB_SWITCH and len(driver.window_handles) > 1:
                driver.switch_to.window(driver.window_handles[1])
                total_tab_switch += 1
            
    except Exception as _e:
        pass
    finally:
        if not driver is None:
            driver.quit()
        logging.info("done")


def send_the_monke(url):
    cleanup_id = os.urandom(16).hex()
    visit_url(url, cleanup_id)
    cleanup(cleanup_id)


def monke_worker():
    while True:
        try:
            url = monke_queue.get()[0]
            send_the_monke(url)
        except Exception as e:
            logging.error(e)

        # Only process 1 URL every minute
        time.sleep(60)