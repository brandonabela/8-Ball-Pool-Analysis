import time # Timer
import pyautogui # Image detection on screen
import webbrowser # Web browser 

class MiniclipHandling:
    def isGameOpen(self, gameUrl, gameUrlPath):
        urlCoordinate = pyautogui.locateOnScreen(gameUrlPath, confidence=.6)

        if urlCoordinate is None:
            chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s --incognito'
            webbrowser.get(chrome_path).open_new(gameUrl)

    def isUserLoggedIn(self):
        signedInCoordinate = pyautogui.locateOnScreen('images\\SignedIn.PNG', confidence=.6)

        if signedInCoordinate is not None:
            pyautogui.click(signedInCoordinate)
            return input("Log in with your account and press enter")

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

def main():
    eightBallUrl = 'https://www.miniclip.com/games/8-ball-pool-multiplayer/en/focus/'
    eightBallUrlPath = 'images\\8BallURL.PNG'

    miniclipHandling = MiniclipHandling()
    miniclipHandling.isGameOpen(eightBallUrl, eightBallUrlPath)
    miniclipHandling.isUserLoggedIn()

    eightBallHandling = EightBallHandling()

    if eightBallHandling.isGameLoaded():
        print("Game has loaded with a logged in account")
    else:
        print("User has not logged in")

if __name__ == '__main__':
    main()
