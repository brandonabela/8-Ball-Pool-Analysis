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
