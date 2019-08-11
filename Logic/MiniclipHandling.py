import time # Stop program for a number of seconds
import webbrowser  # Web browser
import pyautogui  # Image detection on screen

class MiniclipHandling:
    def isGameOpen(self, lookup):
        return pyautogui.locateOnScreen(lookup.urlPath, confidence=.6) is not None            
    
    def openGame(self, lookup):
        webbrowser.get(lookup.chromePath).open_new(lookup.url)
    
    def isUserLoggedIn(self, lookup):
        return pyautogui.locateOnScreen(lookup.signUpLogin, confidence=.6) is not None

    def logInUser(self, lookup, email, password):
        signUpLoginCoordinate = pyautogui.locateOnScreen(lookup.signUpLogin, confidence=.6)
        
        if signUpLoginCoordinate is not None:
            pyautogui.click(signUpLoginCoordinate)

            while pyautogui.locateOnScreen(lookup.logInLoading, confidence=.6) is not None:
                time.sleep(0.5)
            
            emailCoordinate = pyautogui.locateOnScreen(lookup.email, confidence=.6)
            pyautogui.click(emailCoordinate)
            pyautogui.typewrite(email)
        
            passwordCoordinate = pyautogui.locateOnScreen(lookup.password, confidence=.6)
            pyautogui.click(passwordCoordinate)
            pyautogui.typewrite(password)

            time.sleep(0.25) # Wait for any errors to show up on screen

            signInCoordinate = pyautogui.locateOnScreen(lookup.signIn, confidence=.6)
            pyautogui.click(signInCoordinate)

            return pyautogui.locateOnScreen(lookup.signUpLogin, confidence=.6) is None
        else:
            return False
