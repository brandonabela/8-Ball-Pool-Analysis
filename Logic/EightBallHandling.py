import pyautogui # Image detection on screen
import time # Stop program for a number of seconds

class EightBallHandling:
    def isGameLoaded(self, lookup):
        while True:
            backButtonCoordinate = pyautogui.locateOnScreen(lookup.backButton, confidence=.8)
            closeButtonCoordinate = pyautogui.locateOnScreen(lookup.closeButton, confidence=.8)

            if closeButtonCoordinate is not None:
                pyautogui.click(closeButtonCoordinate)
                time.sleep(0.25)
            elif backButtonCoordinate is not None:
                pyautogui.click(backButtonCoordinate)
                time.sleep(0.25)
            else:
                break

        return pyautogui.locateOnScreen(lookup.OneVsOneButton, confidence=.8) is not None
