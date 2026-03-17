import requests
from src.app import DoveApp
from src.util.storable import Storable
from src.config_loader import API_ENDPOINT
from datetime import datetime, timedelta

class JwtToken(Storable):
    def __init__(self, access_token="", refresh_token="", expires_at=None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_at = expires_at

import requests
from datetime import datetime, timedelta

def request_jwt_token(user_id, password):
    payload = {
        "id": user_id,
        "password": password
    }

    try:
        response = requests.post(f"{API_ENDPOINT}/login", json=payload, timeout=5)

        if response.status_code == 200:
            data = response.json()
            access = data.get("access_token")
            refresh = data.get("refresh_token")
            expires_in = data.get("expires_in", 3600)
            
            expiry_date = datetime.now() + timedelta(seconds=expires_in)

            token_obj = JwtToken(
                access_token=access,
                refresh_token=refresh,
                expires_at=expiry_date
            )
            return token_obj, None
            
        elif response.status_code == 401:
            return None, "Invalid ID or password."
        else:
            return None, f"Server Error ({response.status_code})"
        
    except requests.exceptions.ConnectionError:
        return None, "Could not connect to the server."
    except requests.exceptions.Timeout:
        return None, "Connection timed out."
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"