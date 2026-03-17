from .config_loader import FOLDER_NAME
from .state import state

class DoveApp:
    def start_folder(self):
        from .folder import DoveFolder
        state.folder = DoveFolder.load()
        if not state.folder:
            state.folder = DoveFolder(FOLDER_NAME)
            state.folder.create_directory()
        state.folder.start_watch()

    def start_ws(self):
        from .ws import WsClient
        state.ws = WsClient()
        state.ws.on_message(lambda msg: print("[ws]", msg))
        state.ws.start()

    def stop(self):
        if state.ws:
            state.ws.stop()
        if state.folder:
            state.folder.stop_watch()

    def run(self):
        print("Preparing to launch...")
        self.start_folder()
        self.start_ws()
        print("Application started successfully.")

    @property
    def folder(self):
        return state.folder

    @property
    def jwt(self):
        return state.jwt

    @property
    def ws(self):
        return state.ws