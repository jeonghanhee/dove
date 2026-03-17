import os
import time
import threading
from watchdog.events import FileSystemEventHandler
from src.network.notifier import send_notification
from src.storage.loader import get_message

class FileRenameHandler(FileSystemEventHandler):
    def __init__(self, folder_obj):
        self.folder_obj = folder_obj

    def on_moved(self, event):
        src = os.path.abspath(event.src_path)
        current_folder_obj_path = os.path.abspath(self.folder_obj.path)

        if src == current_folder_obj_path:
            old_path = self.folder_obj.path
            self.folder_obj.path = os.path.abspath(event.dest_path)
            self.folder_obj.name = os.path.basename(event.dest_path)
            self.folder_obj.is_born = True
            self.folder_obj.old_path = old_path
            
            title, message = get_message("born", name=self.folder_obj.name)
            send_notification(title, message)

            t = threading.Thread(target=self._delayed_set_icon, daemon=True)
            t.start()

    def _delayed_set_icon(self):
        time.sleep(1) 
        self.folder_obj.set_icon()
        self.folder_obj.save()