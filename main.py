import os
import threading
from PIL import Image
import pystray
from app.app import DoveApp
from app.config_loader import APP_PROG, APP_DESCRIPTION

def setup_tray():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    icon_image = Image.open(os.path.join(base_dir, "assets", "icons", "dove.ico"))
    menu = pystray.Menu(pystray.MenuItem("Quit", lambda icon, _: icon.stop()))
    icon = pystray.Icon(APP_PROG, icon_image, APP_DESCRIPTION, menu)
    icon.run()

def main():
    threading.Thread(target=lambda: DoveApp().run(), daemon=True).start()
    setup_tray()

if __name__ == "__main__":
    main()