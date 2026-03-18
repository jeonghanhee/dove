import os
from .config_loader import FOLDER_NAME, APP_ID

class DoveApp:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DoveApp, cls).__new__(cls)
            cls._instance.folder = None
            cls._instance.token = None
            cls._instance.ws = None
            cls._instance._initialized = False
            cls._instance._engine_started = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._initialized = True

    def load_token(self):
        from .network.auth import JwtToken
        self.token = JwtToken.load()

    def create_folder(self) -> bool:
        from .filesystem.folder import DoveFolder
        try:
            self.folder = DoveFolder.load()
            if not self.folder or not os.path.isdir(self.folder.path):
                self.folder = DoveFolder(FOLDER_NAME)
                self.folder.create_directory()

            if not self.folder.exists():
                print("Folder validation failed.")
                return False

            self.folder.start_watch()
            return True
        except Exception as err:
            print(f"Failed to start folder: {err}")
            return False

    def start_ws(self) -> bool:
        from .network.ws import WsClient
        try:
            self.ws = WsClient()
            self.ws.on_message(lambda msg: print("[ws]", msg))
            self.ws.start()
            return True
        except Exception as err:
            print(f"Failed to start WebSocket: {err}")
            return False

    def stop(self):
        if self.ws:
            self.ws.stop()
        if self.folder:
            self.folder.stop_watch()
        self.token = None
        print("Application services stopped.")

    def run(self):
        print(f"Launching {APP_ID} program...")

        self.load_token()

        if not self.create_folder():
            return 

        if not self.start_ws():
            return

        print(f"{APP_ID} engine services are now active.")