import platform
import subprocess
from src.storage.loader import APP_ID

system = platform.system()

def send_notification(title: str, message: str):
    if system == "Windows":
        from winotify import Notification
        toast = Notification(app_id=APP_ID, title=title, msg=message)
        toast.show()

    elif system == "Darwin":
        subprocess.run([
            "terminal-notifier",
            "-title", title,
            "-message", message,
            #"-sender", APP_ID
        ])