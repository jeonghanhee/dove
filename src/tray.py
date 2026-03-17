import pystray
import sys
import threading
import time
from PIL import Image
from pathlib import Path
from .network.auth import JwtToken
from .config_loader import APP_PROG, APP_DESCRIPTION

class DoveTray:
    def __init__(self):
        self.icon = None
        self.window_to_open = None

    def _auth_label(self, item):
        return "Disconnect" if JwtToken.exists() else "Connect"

    def build_menu(self):
        return pystray.Menu(
            pystray.MenuItem(self._auth_label, self.handle_connect_click),
            pystray.MenuItem("Quit", self.stop),
        )

    def handle_connect_click(self, icon, item):
        self.request_open("connecter_window")

    def request_open(self, window_name):
        self.window_to_open = window_name
        print(f"Request to open: {window_name}", flush=True)

    def stop(self, icon, item):
        if self.icon:
            self.icon.stop()
        sys.exit(0)

    def _update_loop(self):
        last_state = JwtToken.exists()
        while True:
            time.sleep(1)
            current_state = JwtToken.exists()
            if current_state != last_state:
                last_state = current_state
                if self.icon:
                    self.icon.update_menu()
                    print(f"Auth state changed: {current_state}", flush=True)

    def run(self):
        base_dir = Path(__file__).resolve().parent.parent
        icon_path = base_dir / "assets" / "icons" / "dove.ico"

        try:
            icon_image = Image.open(icon_path)
        except Exception:
            icon_image = Image.new("RGB", (64, 64), color=(73, 80, 87))

        self.icon = pystray.Icon(
            APP_PROG,
            icon_image,
            APP_DESCRIPTION,
            menu=self.build_menu(),
        )

        threading.Thread(target=self._update_loop, daemon=True).start()

        self.icon.run()