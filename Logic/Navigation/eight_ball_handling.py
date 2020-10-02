'''Eight Ball Handling Module'''

import time
import pyautogui

from ctypes import windll

import Config.eight_ball_lookup as lookup


class EightBallHandling:
    '''Responsible for handling the 8 ball game'''

    user32 = windll.user32
    user32.SetProcessDPIAware()

    @staticmethod
    def in_menu():
        '''Responsible for checking if game loaded successfully'''

        return pyautogui.locateOnScreen(lookup.MENU_BUTTON, confidence=lookup.MID_CONFIDENCE) is not None

    @staticmethod
    def access_menu():
        '''Responsible for attempting to access the game main menu'''

        while True:
            back_coordinate = pyautogui.locateOnScreen(lookup.BACK_BUTTON, confidence=lookup.HIGH_CONFIDENCE)
            close_coordinate = pyautogui.locateOnScreen(lookup.CLOSE_BUTTON, confidence=lookup.HIGH_CONFIDENCE)

            if close_coordinate is not None:
                pyautogui.click(close_coordinate)
                time.sleep(0.5)
            elif back_coordinate is not None:
                pyautogui.click(back_coordinate)
                time.sleep(0.5)
            else:
                break

        return pyautogui.locateOnScreen(lookup.MENU_BUTTON, confidence=lookup.MID_CONFIDENCE) is not None

    @staticmethod
    def select_game(entry_fee):
        '''Responsible for attempting to select a game based on the entry fee'''

        game_image = None

        if entry_fee == 50:
            game_image = lookup.GAME_FEE_50
        elif entry_fee == 100:
            game_image = lookup.GAME_FEE_100
        elif entry_fee == 500:
            game_image = lookup.GAME_FEE_500

        oneOnOneButton = pyautogui.locateOnScreen(lookup.MENU_BUTTON, confidence=lookup.MID_CONFIDENCE)
        pyautogui.click(oneOnOneButton)

        time.sleep(2)

        while True:
            game_selection = pyautogui.locateOnScreen(game_image, confidence=lookup.LOW_CONFIDENCE)
            previous_button = pyautogui.locateOnScreen(lookup.PREVIOUS_BUTTON, confidence=lookup.HIGH_CONFIDENCE)

            if game_selection is not None:
                pyautogui.click(game_selection)
            elif previous_button is not None:
                pyautogui.click(previous_button)
                time.sleep(1)
            else:
                break
