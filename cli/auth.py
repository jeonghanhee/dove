import requests
import getpass
from ..app.jwt import JwtToken
from ..app.config_loader import API_URL

def login() -> bool:
    username = input("* Username: ").strip()
    password = getpass.getpass("* Password: ")

    try:
        response = requests.post(
            f"{API_URL}/auth/login",
            json={"username": username, "password": password},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        jwt = JwtToken(
            access_token=data["access_token"],
            refresh_token=data.get("refresh_token", ""),
            expires_in=data.get("expires_in", 3600),
        )
        jwt.save()

        print("Login successful.\n")
        return True

    except requests.HTTPError as e:
        if e.response.status_code == 401:
            print("Invalid username or password.\n")
        else:
            print(f"Login failed: {e}\n")
    except requests.RequestException as e:
        print(f"Network error: {e}\n")

    return False

def logout() -> None:
    JwtToken.delete()
    print("Logged out.")