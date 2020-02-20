'''Start Module'''

from GUI.gui_launcher import GUILauncher
from Testing.offline_testing import OfflineTesting

if __name__ == '__main__':
    GUI_LAUNCHER = GUILauncher()
    GUI_LAUNCHER.create_main_window()

    # OFFLINE_TESTING = OfflineTesting()
    # OFFLINE_TESTING.optimal_path_video('Testing\\Examples\\Game Footage.mp4', False, True)
