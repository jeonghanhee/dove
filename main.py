import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from src.app import DoveApp
from src.gui.window_launcher import open_gui

def main():
    qt_app = QApplication(sys.argv)
    qt_app.setQuitOnLastWindowClosed(False)
    
    dove = DoveApp()
    dove.run()

    def check_tray_request():
        if dove.tray.window_to_open:
            window_name = dove.tray.window_to_open
            dove.tray.window_to_open = None
            open_gui(window_name)

    timer = QTimer()
    timer.timeout.connect(check_tray_request)
    timer.start(100)

    sys.exit(qt_app.exec())

if __name__ == "__main__":
    main()