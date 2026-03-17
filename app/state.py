from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .folder import DoveFolder
    from .jwt import JwtToken
    from .ws import WsClient
    
class State:
    _instance = None
    folder: "DoveFolder | None"
    jwt: "JwtToken | None"
    ws: "WsClient | None"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.folder = None
            cls._instance.jwt = None
        return cls._instance

state = State()