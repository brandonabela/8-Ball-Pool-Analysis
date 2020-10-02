'''GUI Launcher Module'''

import sys
import time
import cv2
import pyautogui

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QComboBox, QMessageBox, QWidget

import Config.eight_ball_lookup as lookup

from Logic.Game.bot import Bot

from Logic.Navigation.miniclip_handling import MiniclipHandling
from Logic.Navigation.eight_ball_handling import EightBallHandling


class GUILauncher:
    '''The GUI Launcher is responsible for handling the GUI of the application'''

    window = {}
    login_window = {}

    miniclipHandling = MiniclipHandling()
    eightBallHandling = EightBallHandling()

    def create_main_window(self):
        '''Responsible for loading the main window'''

        app = QtWidgets.QApplication(sys.argv)

        self.window = uic.loadUi('GUI\\Layouts\\MainWindow.ui')

        y_position = app.desktop().screenGeometry().width() - self.window.width()
        self.window.move(y_position, 0)

        self.window.openGameButton.clicked.connect(self.open_game_button)
        self.window.logInButton.clicked.connect(self.create_log_in_window)
        self.window.playGamebutton.clicked.connect(self.play_game_button)

        self.window.show()
        sys.exit(app.exec_())

    def open_game_button(self):
        '''Responsible for opening the game'''

        if not self.miniclipHandling.is_game_open():
            self.miniclipHandling.open_game()
        else:
            self.show_pop_up(lookup.ALREADY_OPENED_GAME)

    def create_log_in_window(self):
        '''Responsible for loading the log in window'''

        if self.miniclipHandling.is_login_present():
            self.login_window = uic.loadUi('GUI\\Layouts\\LogInScreen.ui')

            self.login_window.logInButton.clicked.connect(self.log_in_button)
            self.login_window.cancelButton.clicked.connect(self.login_window.close)

            self.login_window.show()
        else:
            self.show_pop_up(lookup.ALREADY_OPENED_GAME)

    def log_in_button(self):
        '''Responsible for handling the logging in miniclip'''

        username = self.login_window.emailField.text()
        password = self.login_window.passwordField.text()

        if self.miniclipHandling.log_in_user(username, password):
            self.show_pop_up(lookup.SUCCESSFUL_LOGIN)
        else:
            self.show_pop_up(lookup.ERROR_DURING_LOGIN)

        self.login_window.close

    def play_game_button(self):
        '''Handling the access game'''

        if not self.miniclipHandling.is_game_open():
            self.show_pop_up("User has to access 8 ball website")
        elif self.miniclipHandling.is_login_present():
            self.show_pop_up("User has not logged in")
        else:
            self.eightBallHandling.access_menu()

            if self.eightBallHandling.in_menu():
                self.choose_game()
            else:
                self.show_pop_up("Game is not in main menu but with a successful log in")

    def choose_game(self):
        '''Responsible for displaying a screen to choose an entry fee'''

        self.choose_game_window = uic.loadUi('GUI\\Layouts\\ChooseGame.ui')

        self.choose_game_window.playGameButton.clicked.connect(self.start_game)
        self.choose_game_window.cancelButton.clicked.connect(self.choose_game_window.close)

        self.choose_game_window.show()

    def select_game(self):
        entry_fee = int(self.choose_game_window.feeDropdown.currentText())
        self.choose_game_window.close

        self.eightBallHandling.select_game(entry_fee)
        self.play_game()

    def play_game(self):
        bot = Bot()

        while True:
            windowImage = self.miniclipHandling.getWindowScreenshot()

            # Find Holes if not set

            if not bot.holes:
                bot.find_holes(windowImage)

            # Check if player turn

            if bot.holes:
                print('Perform Game Loop')

            time.sleep(1)

    def start_game(self):
        self.choose_game_window.close

        started_game = self.select_game()

        if started_game:
            self.play_game()

    @staticmethod
    def show_pop_up(message):
        '''Opens a dialogue box'''

        alert = QMessageBox()
        alert.setText(message)
        alert.exec_()
