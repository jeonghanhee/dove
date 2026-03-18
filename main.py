import sys
from PyQt6.QtWidgets import QApplication
from src.app import DoveApp
from src.tray import DoveTray
from src.gui.window_launcher import open_gui

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    dove = DoveApp()
    dove.run()
    
    tray = DoveTray()
    tray.request_open_window.connect(open_gui)
    tray.run()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()