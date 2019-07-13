import pyautogui # Image detection on screen

class EightBallHandling:
    def isGameLoaded(self):
        input("Press Enter once the game has loaded")

        while True:
            backButtonCoordinate = pyautogui.locateOnScreen('images\\EightBall_BackButton.PNG', confidence=.8)
            closeButtonCoordinate = pyautogui.locateOnScreen('images\\EightBall_CloseButton.PNG', confidence=.8)

            if closeButtonCoordinate is not None:
                pyautogui.click(closeButtonCoordinate)
            elif backButtonCoordinate is not None:
                pyautogui.click(backButtonCoordinate)
            else:
                break

        return pyautogui.locateOnScreen('images\\EightBall_OneVsOneButton.PNG', confidence=.8) is not None
