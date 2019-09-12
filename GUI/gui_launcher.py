'''GUI Launcher Module'''

import sys
import asyncio

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QWidget

import Config.eight_ball_lookup as lookup

from Logic.eight_ball_handling import EightBallHandling
from Logic.miniclip_handling import MiniclipHandling

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

        self.update_main_window_buttons()

        self.window.show()
        sys.exit(app.exec_())

    def update_main_window_buttons(self):
        '''Handles which main window buttons are enabled'''

        self.window.openGameButton.setEnabled(False)
        self.window.logInButton.setEnabled(False)
        self.window.playGamebutton.setEnabled(False)

        if not self.miniclipHandling.is_game_open():
            self.window.openGameButton.setEnabled(True)
        elif not self.miniclipHandling.is_logged_in():
            self.window.logInButton.setEnabled(True)
        elif not self.eightBallHandling.is_game_loaded():
            self.window.playGamebutton.setEnabled(True)

    def open_game_button(self):
        '''Responsible for opening the game'''

        if not self.miniclipHandling.is_game_open():
            asyncio.run(self.miniclipHandling.open_game())
            self.show_pop_up(lookup.MONITOR_ONE_TEXT)
        else:
            self.show_pop_up(lookup.ALREADY_OPENED_GAME)

        self.update_main_window_buttons()

    def create_log_in_window(self):
        '''Responsible for loading the log in window'''

        if not self.miniclipHandling.is_logged_in():
            self.login_window = uic.loadUi('GUI\\Layouts\\LogInWindow.ui')

            self.login_window.logInButton.clicked.connect(self.log_in_button)
            self.login_window.cancelButton.clicked.connect(self.login_window.close)

            self.login_window.show()
        else:
            self.show_pop_up(self.login_window.already_opened_game)

        self.update_main_window_buttons()

    def log_in_button(self):
        '''Responsible for handling the logging in miniclip'''

        username = self.login_window.emailField.text()
        password = self.login_window.passwordField.text()

        if self.miniclipHandling.log_in_user(username, password):
            self.show_pop_up(lookup.SUCCESSFUL_LOGIN)
            self.login_window.close
        else:
            self.show_pop_up(lookup.ERROR_DURING_LOGIN)

        self.update_main_window_buttons()

    def play_game_button(self):
        '''Handling the access game'''

        if self.miniclipHandling.is_logged_in():
            self.eightBallHandling.access_menu()

            if self.eightBallHandling.is_game_loaded():
                self.show_pop_up("Game is in main menu with a successful log in")
            else:
                self.show_pop_up("Game is not in main menu but with a successful log in")
        else:
            self.show_pop_up("User has not logged in")

        self.update_main_window_buttons()

    def show_pop_up(self, message):
        '''Opens a dialog box'''

        alert = QMessageBox()
        alert.setText(message)
        alert.exec_()
