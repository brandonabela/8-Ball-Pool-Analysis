# 8 Ball Pool Bot

This is an Open Source project that aims to build a bot that can play Miniclip's **8 ball pool** through the use of an AI.

When making use of the application make sure the monitor scaling on Windows is set to **100%** otherwise **pyautogui** would not be able to identify the images being searched.

Features:
- [x] Open 8 ball pool in focus mode.
- [x] Check if the user is logged in.
- [x] GUI app that lets the user open Miniclip, Log In and play the Game.
- [x] Implement game item detection.
- [x] Implement ball classification.
- [x] Algorithm that finds an optimal path to score.
- [ ] Calculate cue force for a given path.
- [ ] Algorithm for game loop.

Installing Packages using conda:
- conda install -c anaconda pip
- conda install -c selenium
- conda install -c conda-forge opencv
- conda install -c anaconda pyqt
- conda install -c conda-forge pyautogui
- conda install -c conda-forge scikit-image
- conda install -c anaconda pylint
