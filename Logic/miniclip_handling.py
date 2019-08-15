'''Miniclip Handling Module'''

import time
import webbrowser

import pyautogui

from Config.eight_ball_lookup import EightBallLookup

class MiniclipHandling:
    '''Responsible for handling miniclip logic'''

    lookup = EightBallLookup()

    def is_game_open(self):
        '''Responsible for checking if the web browser was opened successfully'''

        return pyautogui.locateOnScreen(self.lookup.url_path, confidence=self.lookup.low_confidence) is not None

    async def open_game(self):
        '''Opening an incognito web browser based on a url'''

        webbrowser.get(self.lookup.chrome_path).open_new(self.lookup.url)

    def is_logged_in(self):
        '''Checking if log in is allowed'''

        return pyautogui.locateOnScreen(self.lookup.sign_up_login, confidence=self.lookup.low_confidence) is None

    def log_in_user(self, email, password):
        '''Logging in using an email and password'''

        login_coordinate = pyautogui.locateOnScreen(self.lookup.sign_up_login, confidence=self.lookup.low_confidence)

        if login_coordinate is not None:
            pyautogui.click(login_coordinate)

            time.sleep(1) # Wait for the pop up to completely show

            while pyautogui.locateOnScreen(self.lookup.log_in_loading, confidence=self.lookup.low_confidence) is not None:
                time.sleep(1)

            email_coordinate = pyautogui.locateOnScreen(self.lookup.email, confidence=self.lookup.low_confidence)
            pyautogui.click(email_coordinate)
            pyautogui.typewrite(email)

            password_coordinate = pyautogui.locateOnScreen(self.lookup.password, confidence=self.lookup.low_confidence)
            pyautogui.click(password_coordinate)
            pyautogui.typewrite(password)

            time.sleep(2) # Wait for any errors to show up on screen

            sign_in_coordinate = pyautogui.locateOnScreen(self.lookup.sign_in, confidence=self.lookup.high_confidence)
            pyautogui.click(sign_in_coordinate)

        return pyautogui.locateOnScreen(self.lookup.sign_up_login, confidence=self.lookup.low_confidence) is None
