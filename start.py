import time # Timer

from Logic.MiniclipHandling import MiniclipHandling
from Logic.EightBallHandling import EightBallHandling

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
