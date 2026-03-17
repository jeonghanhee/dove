import sys
from .storage.loader import FOLDER_NAME
from .storage.state import state
from .filesystem.folder import DoveFolder
from .network.ws import WsClient
from .tray import DoveTray

class DoveApp:
    def __init__(self):
        self.tray = DoveTray()

    def create_folder(self) -> bool:
        try:
            state.folder = DoveFolder.load()
            if not state.folder:
                state.folder = DoveFolder(FOLDER_NAME)
                state.folder.create_directory()

            if not state.folder.exists():
                print("Folder validation failed: folder does not exist.")
                return False

            state.folder.start_watch()
            print("Folder started successfully.")
            return True
        except Exception as err:
            print(f"Failed to start folder: {err}")
            return False

    def start_ws(self) -> bool:
        try:
            state.ws = WsClient()
            state.ws.on_message(lambda msg: print("[ws]", msg))
            state.ws.start()

            # if not state.ws.is_connected():
            #     print("WebSocket validation failed: not connected.")
            #     return False

            print("WebSocket started successfully.")
            return True
        except Exception as err:
            print(f"Failed to start WebSocket: {err}")
            return False

    def stop(self):
        if state.ws:
            state.ws.stop()
        if state.folder:
            state.folder.stop_watch()
        print("Application services stopped.")

    def run(self):
        print("Preparing to launch engine...")

        if not self.create_folder():
            print("Cannot create folder.")
            sys.exit(1)

        if not self.start_ws():
            print("Cannot start WebSocket.")
            sys.exit(1)

        print("Application engine started successfully.")

        try:
            self.tray.run()
        finally:
            self.stop()
            
    @property
    def folder(self):
        return state.folder

    @property
    def jwt(self):
        return state.jwt

    @property
    def ws(self):
        return state.ws

if __name__ == "__main__":
    app = DoveApp()
    app.run()