'''Start Module'''

from GUI.gui_launcher import GUILauncher
from Logic.item_detection import ItemDetection

if __name__ == '__main__':
    GUI_LAUNCHER = GUILauncher()
    GUI_LAUNCHER.create_main_window()

    # ITEM_DETECTION = ItemDetection()
    # ITEM_DETECTION.identify_parameters(True, False)
    # ITEM_DETECTION.detection_video('Training\\Game Footage.mp4', True, False)
