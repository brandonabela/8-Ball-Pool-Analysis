'''Start Module'''

from GUI.gui_launcher import GUILauncher
from Logic.detection_training import DetectionTraining

if __name__ == '__main__':
    GUI_LAUNCHER = GUILauncher()
    GUI_LAUNCHER.create_main_window()

    # DETECTION_TRAINING = DetectionTraining()
    # DETECTION_TRAINING.detection_on_video('Training\\Game Footage.mp4', True, False)
