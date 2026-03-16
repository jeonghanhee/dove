import platform

system = platform.system()

def send_notification(title: str, message: str):
    if system == "Windows":
        from winotify import Notification
        toast = Notification(app_id="dove", title=title, msg=message)
        toast.show()
    elif system == "Darwin":
        import subprocess
        script = f'display notification "{message}" with title "{title}"'
        subprocess.run(["osascript", "-e", script])