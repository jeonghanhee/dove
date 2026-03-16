import os
import time
import threading
from watchdog.events import FileSystemEventHandler
from .notifier import send_notification
from .config_loader import get_message

class FileRenameHandler(FileSystemEventHandler):
    def __init__(self, folder):
        self.folder = folder

    def on_moved(self, event):
        src = os.path.abspath(event.src_path)
        current_folder_path = os.path.abspath(self.folder.path)

        if src == current_folder_path:
            old_path = self.folder.path
            self.folder.path = os.path.abspath(event.dest_path)
            self.folder.name = os.path.basename(event.dest_path)
            self.folder.is_born = True
            self.folder.old_path = old_path
            
            title, message = get_message("born", name=self.folder.name)
            send_notification(title, message)

            t = threading.Thread(target=self._delayed_set_icon, daemon=True)
            t.start()

    def _delayed_set_icon(self):
        time.sleep(1) 
        self.folder.set_icon()