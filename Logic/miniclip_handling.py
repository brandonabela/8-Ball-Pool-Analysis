'''Miniclip Handling Module'''

import time
import webbrowser

import pyautogui

import Config.eight_ball_lookup as lookup

class MiniclipHandling:
    '''Responsible for handling miniclip logic'''

    @staticmethod
    def is_game_open():
        '''Responsible for checking if the web browser was opened successfully'''

        return pyautogui.locateOnScreen(lookup.URL_PATH, confidence=lookup.MID_CONFIDENCE) is not None

    @staticmethod
    async def open_game():
        '''Opening an incognito web browser based on a url'''

        webbrowser.get(lookup.CHROME_PATH).open_new(lookup.URL)

    @staticmethod
    def is_logged_in():
        '''Checking if log in is allowed'''

        return pyautogui.locateOnScreen(lookup.SIGN_UP_LOGIN, confidence=lookup.MID_CONFIDENCE) is None

    @staticmethod
    def log_in_user(email, password):
        '''Logging in using an email and password'''

        login_coordinate = pyautogui.locateOnScreen(lookup.SIGN_UP_LOGIN, confidence=lookup.MID_CONFIDENCE)

        if login_coordinate is not None:
            pyautogui.click(login_coordinate)

            time.sleep(1) # Wait for the pop up to completely show

            while pyautogui.locateOnScreen(lookup.SIGN_IN, confidence=lookup.MID_CONFIDENCE) is None:
                time.sleep(1)

            email_coordinate = pyautogui.locateOnScreen(lookup.EMAIL, confidence=lookup.MID_CONFIDENCE)
            pyautogui.click(email_coordinate)
            pyautogui.typewrite(email)

            password_coordinate = pyautogui.locateOnScreen(lookup.PASSWORD, confidence=lookup.MID_CONFIDENCE)
            pyautogui.click(password_coordinate)
            pyautogui.typewrite(password)

            time.sleep(2) # Wait for any errors to show up on screen

            sign_in_coordinate = pyautogui.locateOnScreen(lookup.SIGN_IN, confidence=lookup.HIGH_CONFIDENCE)
            pyautogui.click(sign_in_coordinate)

        return pyautogui.locateOnScreen(lookup.SIGN_UP_LOGIN, confidence=lookup.MID_CONFIDENCE) is None
