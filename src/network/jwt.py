from src.storage.storable import Storable

class JwtToken(Storable):
    def __init__(self, access_token="", refresh_token="", expires_at=None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_at = expires_at