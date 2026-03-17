import os
import platform
import subprocess
import ctypes
import threading
from watchdog.observers import Observer
from .handlers import FileRenameHandler
from src.storage.storable import Storable
from src.storage.loader import FOLDER_NAME, ASSETS_ICONS_FOLDER

ATTR_READONLY = 0x01
ATTR_HIDDEN = 0x02
ATTR_SYSTEM = 0x04
ATTR_NORMAL = 0x80

class DoveFolder(Storable):
    def __init__(self, name=FOLDER_NAME):
        self.name = name
        self.is_born = False
        self.system = platform.system()
        self.desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        self.icon_file = None
        self.icon_path = None
        self.path = os.path.join(self.desktop, self.name)
        self._observer = None

    def update_path(self, new_name):
        self.name = new_name
        self.path = os.path.join(self.desktop, self.name)

    def create_directory(self):
        os.makedirs(self.path, exist_ok=True)
        self.set_icon()
        self.save()

    def set_icon(self):
        if not self.is_born:
            self.icon_file = "egg.ico" if self.system == "Windows" else "egg.icns"
        else:
            self.icon_file = "dove.ico" if self.system == "Windows" else "dove.icns"

        self.icon_path = os.path.abspath(os.path.join(ASSETS_ICONS_FOLDER, self.icon_file))

        if self.system == "Windows":
            self._set_windows_icon()
        elif self.system == "Darwin":
            self._set_macos_icon()
            
    def start_watch(self):
        if self.system not in ["Windows", "Darwin"]:
            return
        if not self.is_born:    
            parent_dir = os.path.dirname(self.path)
            self._observer = Observer()
            self._observer.schedule(FileRenameHandler(self), path=parent_dir, recursive=False)
            threading.Thread(target=self._observer.start, daemon=True).start()
        threading.Thread(target=self._watch_deleted, daemon=True).start()

    def _set_windows_icon(self):
        desktop_ini = os.path.join(self.path, "desktop.ini")

        if os.path.exists(desktop_ini):
            ctypes.windll.kernel32.SetFileAttributesW(desktop_ini, ATTR_NORMAL)
            os.remove(desktop_ini)

        content = (
            "[.ShellClassInfo]\r\n"
            f"IconResource={self.icon_path},0\r\n"
            "[ViewState]\r\n"
            "Mode=\r\n"
            "Vid=\r\n"
            "FolderType=Generic\r\n"
        )

        with open(desktop_ini, "w", encoding="utf-16") as f:
            f.write(content)

        ctypes.windll.kernel32.SetFileAttributesW(desktop_ini, ATTR_HIDDEN | ATTR_SYSTEM)
        ctypes.windll.kernel32.SetFileAttributesW(self.path, ATTR_READONLY)

        shell32 = ctypes.windll.shell32
        parent_path = os.path.dirname(self.path)
        old_path = getattr(self, 'old_path', self.path)

        shell32.SHChangeNotify(
            0x00020000, # SHCNE_RENAMEFOLDER
            0x0005, # SHCNF_PATHW
            ctypes.c_wchar_p(old_path),
            ctypes.c_wchar_p(self.path)
        )
        shell32.SHChangeNotify(0x00001000, 0x0005, ctypes.c_wchar_p(parent_path), None)

    def _set_macos_icon(self):
        try:
            subprocess.run(["fileicon", "set", self.path, self.icon_path], check=True)
            subprocess.run(["killall", "Finder"])
        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            print(f"fileicon failed: {e}")
        
    def _watch_deleted(self):
        while True:
            if not os.path.exists(self.path):
                if DoveFolder.exists():
                    DoveFolder.delete() 
                break
            threading.Event().wait(2)

    def _to_dict(self) -> dict:
        return {
            "name": self.name,
            "is_born": self.is_born,
            "icon_file": self.icon_file,
            "icon_path": self.icon_path,
        }

    def _from_dict(self, data: dict) -> None:
        self.name = data["name"]
        self.is_born = data["is_born"]
        self.icon_file = data.get("icon_file")
        self.icon_path = data.get("icon_path")
        self.system = platform.system()
        self.desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        self.path = os.path.join(self.desktop, self.name)
        self._observer = None