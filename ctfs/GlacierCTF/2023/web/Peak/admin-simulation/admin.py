#!/usr/bin/env python3
import sys, requests
import os
from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime


from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display


import urllib3
urllib3.disable_warnings()

class AdminAutomation:
    host = os.environ.get("HOST", "http://web")
    timeout = int(os.environ.get("TIMEOUT", "5"))
    driver = None
    _username = 'admin'
    _password = '' 
    
    display = Display(visible=0, size=(800, 600))
    display.start()

    def __init__(self, password:str=''):
        
        chrome_options = self._set_chrome_options()
        service = Service(executable_path=r'/usr/bin/chromedriver')
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.set_page_load_timeout(self.timeout) 

        self._password = password
        if self._password == '':
            raise Exception('No password for admin configured!')

    def _set_chrome_options(self):
        '''
        Sets chrome options for Selenium:
        - headless browser is enabled
        - sandbox is disbaled
        - dev-shm usage is disabled
        - SSL certificate errors are ignored
        '''
        chrome_options = webdriver.ChromeOptions()
        
        options = [
        '--headless',
        '--no-sandbox', '--disable-dev-shm-usage', '--ignore-certificate-errors', 
        '--disable-extensions', '--no-first-run', '--disable-logging',
        '--disable-notifications', '--disable-permissions-api', '--hide-scrollbars',
        '--disable-gpu', '--window-size=800,600', '--disable-xss-auditor'
        ]

        
        for option in options:
            chrome_options.add_argument(option)
        return chrome_options

    def login(self) -> bool:
        '''
        Login as admin
        - Returns: `True` if successful and `False` of unsuccessful
        '''       
        self.driver.get(f'{self.host}/login.php')

        
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
        self.driver.find_element('name', 'username').send_keys('admin')
        
        
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
        self.driver.find_element('name', 'password').send_keys(self._password)
        
        
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.NAME, 'button')))
        self.driver.find_element('name', 'button').click()
        
        
        if self.driver.current_url != f'{self.host}/':
            return False
        
        print(f'[{datetime.now()}] Successfully logged in!\r\n')
        return True

    def read_messages(self):
        
        print(f'[{datetime.now()}] Checking messages...')
        self.driver.get(f'{self.host}/admin/support.php')

        if self.driver.current_url != f'{self.host}/admin/support.php':
            raise Exception("Cannot access support.php! Session probably expired!")

        links = [element.get_attribute('href') for element in self.driver.find_elements('name', 'inbox-header')]
        if len(links) > 0:
            for link in links:
                if link:
                    try:
                        self.driver.get(link)

                        if self.driver.current_url == link:
                            print(f'[{datetime.now()}] Visiting: {self.driver.current_url}\r\n')
                        else:
                            print(f'[{datetime.now()}] After visiting {link}, got redirect to: {self.driver.current_url}\r\n')
                    except Exception as ex:
                        '''Timeout or other exception occurred on url.
                        '''
                        print(f'[{datetime.now()}] Error after visiting: {link} (Current URL: {self.driver.current_url}). Error: {ex}\r\n')
        
    def close(self):
        
        if self.driver:
            self.driver.close()
            self.driver.quit()
            self.driver = None
        if self.display:
            self.display.stop()

if __name__ == '__main__':  
    
    os.system('pkill -f chrome')
    os.system('pkill -f Xvfb')

    admin = None
    try:
        if len(sys.argv) < 2:
            raise Exception('Specify a password!')
        admin = AdminAutomation(sys.argv[1])
        
        tries = 0
        while not admin.login():
            if tries > 5:
                raise Exception('Could not login!')
            tries += 1
            sleep(1)
        
        while True:
            admin.read_messages()
            sleep(5)
        
        admin.close()
        quit()
    except Exception as ex:
        print(f'[-] Error: {ex}')
        
        if admin is not None:
            admin.close()
        quit()
