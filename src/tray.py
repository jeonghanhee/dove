import sys
import os
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from pathlib import Path

from .network.auth import JwtToken
from .config_loader import APP_PROG, APP_DESCRIPTION

class DoveTray(QObject):
    request_open_window = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.tray_icon = QSystemTrayIcon()
        self.last_auth_state = JwtToken.exists()

        base_dir = Path(__file__).resolve().parent.parent
        icon_path = str(base_dir / "assets" / "icons" / "dove.ico")
        
        if os.path.exists(icon_path):
            self.tray_icon.setIcon(QIcon(icon_path))
        
        self.update_menu()
        self.tray_icon.setToolTip(APP_DESCRIPTION)

        self.monitor_timer = QTimer(self)
        self.monitor_timer.timeout.connect(self.check_status_change)
        self.monitor_timer.start(1000)

    def check_status_change(self):
        current_state = JwtToken.exists()
        if current_state != self.last_auth_state:
            self.last_auth_state = current_state
            self.update_menu()

    def update_menu(self):
        menu = QMenu()

        auth_label = "Disconnect" if JwtToken.exists() else "Connect"
        auth_action = menu.addAction(auth_label)
        auth_action.triggered.connect(self.handle_auth_click)

        menu.addSeparator()
        
        quit_action = menu.addAction("Quit")
        quit_action.triggered.connect(self.stop)

        self.tray_icon.setContextMenu(menu)

    def handle_auth_click(self):
        self.request_open("connecter_window")
        QTimer.singleShot(100, self.update_menu)

    def request_open(self, window_name):
        self.request_open_window.emit(window_name)
        print(f"Request to open: {window_name}", flush=True)

    def stop(self):
        self.tray_icon.hide()
        sys.exit(0)

    def run(self):
        self.tray_icon.show()