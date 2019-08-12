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

        return pyautogui.locateOnScreen(self.lookup.url_path, confidence=.6) is not None

    async def open_game(self):
        '''Opening an incognito web browser based on a url'''

        webbrowser.get(self.lookup.chrome_path).open_new(self.lookup.url)

    def is_logged_in(self):
        '''Checking if log in is allowed'''

        return pyautogui.locateOnScreen(self.lookup.sign_up_login, confidence=.6) is None

    def log_in_user(self, email, password):
        '''Logging in using an email and password'''

        login_coordinate = pyautogui.locateOnScreen(self.lookup.sign_up_login, confidence=.6)

        if login_coordinate is not None:
            pyautogui.click(login_coordinate)

            while pyautogui.locateOnScreen(self.lookup.log_in_loading, confidence=.6) is not None:
                time.sleep(1)

            time.sleep(1.5) # Wait for the pop up to completely show

            email_coordinate = pyautogui.locateOnScreen(self.lookup.email, confidence=.6)
            pyautogui.click(email_coordinate)
            pyautogui.typewrite(email)

            password_coordinate = pyautogui.locateOnScreen(self.lookup.password, confidence=.6)
            pyautogui.click(password_coordinate)
            pyautogui.typewrite(password)

            time.sleep(1.5) # Wait for any errors to show up on screen

            sign_in_coordinate = pyautogui.locateOnScreen(self.lookup.sign_in, confidence=.6)
            pyautogui.click(sign_in_coordinate)

        return pyautogui.locateOnScreen(self.lookup.sign_up_login, confidence=.6) is None
