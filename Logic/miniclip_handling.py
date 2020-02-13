'''Miniclip Handling Module'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import Config.eight_ball_lookup as lookup

class MiniclipHandling:
    '''Responsible for handling miniclip logic'''

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(chrome_options=chrome_options)

    login_locator = '//a[contains(text(), "Login")]'
    facebook_page_locator = '//a[contains(text(), "8 Ball Pool Fan Page")]'

    modal_locator = '//iframe[@class="mc-modal-iframe"]'
    modal_email_locator = '//*[@id="form-email"]'
    modal_password_locator = '//*[@id="form-password"]'
    modal_sign_in_locator = '//*[@id="btn-submit-signin"]'

    def is_element_present(self, locator):
        try:
            return self.driver.find_element_by_xpath(locator).is_displayed()
        except:
            return False

    def is_game_open(self):
        '''Responsible for checking if the web browser was opened successfully'''

        return self.is_element_present(self.facebook_page_locator)

    def open_game(self):
        '''Opening a selenium web browser based on a url'''

        self.driver.get(lookup.URL)

    def is_logged_in(self):
        '''Checking if log in is allowed'''

        return not self.is_element_present(self.login_locator)

    def log_in_user(self, email, password):
        '''Logging in using an email and password'''

        login_element = self.driver.find_element_by_xpath(self.login_locator)
        login_element.click()

        # Switch to login modal
        modal_frame = self.driver.find_element_by_xpath(self.modal_locator)
        self.driver.switch_to.frame(modal_frame)

        WebDriverWait(self.driver, lookup.MODAL_WAIT).until(EC.presence_of_element_located((By.XPATH, self.modal_sign_in_locator)))

        modal_email_element = self.driver.find_element_by_xpath(self.modal_email_locator)
        modal_email_element.send_keys(email)

        modal_password_element = self.driver.find_element_by_xpath(self.modal_password_locator)
        modal_password_element.send_keys(password)

        sign_in_element = self.driver.find_element_by_xpath(self.modal_sign_in_locator)
        sign_in_element.click()

        # Switching back to main frame
        self.driver.switch_to.frame(None)
