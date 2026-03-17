import pystray
from PIL import Image
from pathlib import Path
from gui.window_launcher import open_gui
from .network.jwt import JwtToken
from .storage.loader import APP_PROG, APP_DESCRIPTION 

class DoveTray:
    def __init__(self):
        self.icon = None

    def build_menu(self):
        if JwtToken.exists():
            return pystray.Menu(
                pystray.MenuItem("Logout", self.logout),
                pystray.MenuItem("Quit", self.stop)
            )
        else:
            return pystray.Menu(
                pystray.MenuItem("Login", lambda: open_gui("login_window")),
                pystray.MenuItem("Quit", self.stop)
            )

    def logout(self, icon, item):
        JwtToken.delete()
        self.icon.menu = self.build_menu()
        print("[*] Logged out and menu updated.")

    def stop(self, icon, item):
        self.icon.stop()

    def run(self):
        base_dir = Path(__file__).resolve().parent.parent
        icon_path = base_dir / "assets" / "icons" / "dove.ico"

        try:
            icon_image = Image.open(icon_path)
        except Exception:
            icon_image = Image.new('RGB', (64, 64), color=(73, 80, 87))

        self.icon = pystray.Icon(APP_PROG, icon_image, APP_DESCRIPTION)
        self.icon.menu = self.build_menu()
        
        print(f"[*] {APP_PROG} Tray icon is running...")
        self.icon.run()