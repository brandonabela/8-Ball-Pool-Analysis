'''Eight Ball Lookup Module'''

# Base Configurations

BASE_PATH = 'Config\\Images\\'
BALL_PATH = BASE_PATH + 'Balls\\'

MID_CONFIDENCE = 0.5
HIGH_CONFIDENCE = 0.7

BALL_RADIUS = 10
BALL_DIAMETER = BALL_RADIUS * 2.2

# URL

URL = 'https://www.miniclip.com/games/8-ball-pool-multiplayer/en/focus/'
CHROME_PATH = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s --incognito'

# Mineclip Image Checking

MODAL_WAIT = 30

BACK_BUTTON = BASE_PATH + 'BackButton.PNG'
CLOSE_BUTTON = BASE_PATH + 'CloseButton.PNG'
MENU_BUTTON = BASE_PATH + 'MenuButton.PNG'

# Output Path

TRAINING_FOLDER = 'Training\\'

HOLE_TRAINING_PATH = 'Parameters\\Holes\\'
BALL_TRAINING_PATH = 'Parameters\\Balls\\'

# Pop Up Text

MONITOR_ONE_TEXT = 'Make sure the web browser is opened on monitor one'

ALREADY_LOGGED_IN = 'User has already logged in'
SUCCESSFUL_LOGIN = 'You have successfully logged in'
ERROR_DURING_LOGIN = 'An error was encountered during log in'

ALREADY_OPENED_GAME = 'Game is already opened'
