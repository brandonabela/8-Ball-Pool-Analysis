'''Eight Ball Handling Module'''

import time
import pyautogui

import Config.eight_ball_lookup as lookup


class EightBallHandling:
    '''Responsible for handling the 8 ball game'''

    @staticmethod
    def is_game_loaded():
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
