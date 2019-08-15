'''Eight Ball Module'''

class EightBallLookup:
    '''Eight Ball Lookup is  is responsible for handling application settings'''

    # Base Configurations

    base_path = 'Config\\Images\\'

    low_confidence = 0.5
    high_confidence = 0.7

    # URL Look Ups

    url = 'https://www.miniclip.com/games/8-ball-pool-multiplayer/en/focus/'
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s --incognito'

    # Mineclip Image Checking

    url_path = base_path + 'Url.PNG'

    sign_up_login = base_path + 'SignUpLogin.PNG'
    log_in_loading = base_path + 'LogInLoading.PNG'
    email = base_path + 'Email.PNG'
    password = base_path + 'Password.PNG'
    sign_in = base_path + 'SignIn.PNG'

    back_button = base_path + 'BackButton.PNG'
    close_button = base_path + 'CloseButton.PNG'
    menu_button = base_path + 'MenuButton.PNG'

    # Pop Up Text

    monitor_one_text = 'Make sure the web browser is opened on monitor one'

    already_logged_in = 'User has already logged in'
    successful_log_in = 'You have successfully logged in'
    error_during_log_in = 'An error was encountered during log in'

    already_opened_game = 'Game is already opened'
