'''Miniclip Handling Module'''

import cv2
import numpy as np

import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import chromedriver_autoinstaller
import Config.eight_ball_lookup as lookup


class MiniclipHandling:
    '''Responsible for handling miniclip logic'''

    chromedriver_autoinstaller.install()

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(chrome_options=chrome_options)

    login_locator = '//a[contains(text(), "Login")]'
    facebook_page_locator = '//a[contains(text(), "8 Ball Pool Fan Page")]'

    modal_locator = '//iframe[@class="mc-modal-iframe"]'
    modal_email_locator = '//*[@id="form-email"]'
    modal_password_locator = '//*[@id="form-password"]'
    model_remember_email = '//*[@id="form-remember"]'
    modal_sign_in_locator = '//*[@id="btn-submit-signin"]'

    def is_element_present(self, locator):
        try:
            return self.driver.find_element_by_xpath(locator).is_displayed()
        except NoSuchElementException:
            return False

    def is_game_open(self):
        '''Responsible for checking if the web browser was opened successfully'''

        return self.is_element_present(self.facebook_page_locator)

    def open_game(self):
        '''Opening a selenium web browser based on a url'''

        self.driver.get(lookup.URL)

    def is_login_present(self):
        '''Checking if log in is allowed'''

        return self.is_element_present(self.login_locator)

    def log_in_user(self, email, password):
        '''Logging in using an email and password'''

        login_element = self.driver.find_element_by_xpath(self.login_locator)
        login_element.click()

        # Switch to login modal
        modal_frame = self.driver.find_element_by_xpath(self.modal_locator)
        self.driver.switch_to.frame(modal_frame)

        time.sleep(random.randint(3, 10))

        WebDriverWait(self.driver, lookup.MODAL_WAIT).until(EC.presence_of_element_located((By.XPATH, self.modal_sign_in_locator)))

        modal_email_element = self.driver.find_element_by_xpath(self.modal_email_locator)
        modal_email_element.send_keys(email)

        time.sleep(random.randint(3, 10))

        modal_password_element = self.driver.find_element_by_xpath(self.modal_password_locator)
        modal_password_element.send_keys(password)

        model_remember_email_element = self.driver.find_element_by_xpath(self.model_remember_email)
        model_remember_email_element.click()

        time.sleep(random.randint(3, 10))

        sign_in_element = self.driver.find_element_by_xpath(self.modal_sign_in_locator)
        sign_in_element.click()

        # Switching back to main frame
        self.driver.switch_to.frame(None)

    def getWindowScreenshot(self):
        '''Responsible for getting a screenshot of the selenium browser'''

        screenshot = self.driver.get_screenshot_as_png()
        np_screenshot = np.frombuffer(screenshot, np.uint8)

        return cv2.imdecode(np_screenshot, cv2.IMREAD_COLOR)
