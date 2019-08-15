'''Eight Ball Handling Module'''

import time
import pyautogui

from Config.eight_ball_lookup import EightBallLookup

class EightBallHandling:
    '''Responsible for handling the 8 ball game'''

    lookup = EightBallLookup()

    def is_game_loaded(self):
        '''Responsible for checking if game loaded successfully'''

        return pyautogui.locateOnScreen(self.lookup.menu_button, confidence=self.lookup.low_confidence) is not None

    def access_menu(self):
        '''Responsible for attempting to access the game main menu'''

        while True:
            back_coordinate = pyautogui.locateOnScreen(self.lookup.back_button, confidence=self.lookup.high_confidence)
            close_coordinate = pyautogui.locateOnScreen(self.lookup.close_button, confidence=self.lookup.high_confidence)

            if close_coordinate is not None:
                pyautogui.click(close_coordinate)
                time.sleep(0.5)
            elif back_coordinate is not None:
                pyautogui.click(back_coordinate)
                time.sleep(0.5)
            else:
                break

        return pyautogui.locateOnScreen(self.lookup.menu_button, confidence=self.lookup.low_confidence) is not None
