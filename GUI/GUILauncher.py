import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import (QWidget, QMessageBox)
from PyQt5.QtCore import QCoreApplication

from Config.EightBallLookup import EightBallLookup
from Logic.MiniclipHandling import MiniclipHandling
from Logic.EightBallHandling import EightBallHandling

class GUILauncher:
    eightBallLookup = EightBallLookup()
    miniclipHandling = MiniclipHandling()
    eightBallHandling = EightBallHandling()

    def createMainWindow(self):
        app = QtWidgets.QApplication(sys.argv)

        self.window = uic.loadUi('GUI\\Layouts\\MainWindow.ui')

        yPosition = app.desktop().screenGeometry().width() - self.window.width()
        self.window.move(yPosition, 0)

        self.window.openGameButton.clicked.connect(self.openGameButton)
        self.window.logInButton.clicked.connect(self.logInButton)
        self.window.playGamebutton.clicked.connect(self.playGameButton)

        self.interaction(True)

        self.window.show()
        sys.exit(app.exec_())

    def interaction(self, isEnabled):
        self.window.playGamebutton.setEnabled(isEnabled)

        if self.miniclipHandling.isGameOpen(self.eightBallLookup):
            self.window.openGameButton.setEnabled(False)
        else:
            self.window.openGameButton.setEnabled(isEnabled)

        if self.miniclipHandling.isUserLoggedIn(self.eightBallLookup):
            self.window.logInButton.setEnabled(False)
        else:
            self.window.logInButton.setEnabled(isEnabled)

    def openGameButton(self):
        self.interaction(False)

        if self.miniclipHandling.isGameOpen(self.eightBallLookup):
            self.miniclipHandling.openGame(self.eightBallLookup)
            self.showPopUp(self.eightBallLookup.monitorOneText)

        self.interaction(True)
    
    def logInButton(self):
        self.interaction(False)

        if not self.miniclipHandling.isUserLoggedIn(self.eightBallLookup):
            self.logInWindow = uic.loadUi('GUI\\Layouts\\LogInWindow.ui')
            
            self.logInWindow.logInButton.clicked.connect(self.logInButton)
            self.logInWindow.cancelButton.clicked.connect(self.logInWindow.close)

            self.logInWindow.show()

        self.interaction(True)
    
    def logInButton(self):
        self.interaction(False)

        username = self.logInWindow.emailField.text()
        password = self.logInWindow.passwordField.text()

        if self.miniclipHandling.logInUser(self.eightBallLookup, username, password):
            self.showPopUp(self.eightBallLookup.successfulLogIn)
            self.logInWindow.close
        else:
            self.showPopUp(self.eightBallLookup.errorDuringLogIn)

        self.interaction(True)

    def playGameButton(self):
        self.interaction(False)

        if self.eightBallHandling.isGameLoaded(self.eightBallLookup):
            self.showPopUp("Game has loaded with a logged in account")
        else:
            self.showPopUp("User has not logged in")

        self.interaction(True)
    
    def showPopUp(self, message):
        alert = QMessageBox()
        alert.setText(message)
        alert.exec_()
