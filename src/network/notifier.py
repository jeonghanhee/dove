import platform
import subprocess
from src.config_loader import APP_ID

system = platform.system()

def notify(title: str, message: str):
    if system == "Windows":
        try:
            from winotify import Notification
            toast = Notification(app_id=APP_ID, title=title, msg=message)
            toast.show()
        except ImportError:
            print(f"[{title}] {message}")
    elif system == "Darwin":
        try:
            subprocess.run([
                "terminal-notifier",
                "-title", title,
                "-message", message
            ], check=True)
        except FileNotFoundError:
            print(f"[{title}] {message}")
    else:
        print(f"[{title}] {message}")