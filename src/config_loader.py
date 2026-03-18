import os
import configparser

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config.ini")

config = configparser.ConfigParser()
config.read(CONFIG_PATH, encoding="utf-8")

# app
APP_ID = config.get("App", "app_id")
APP_PROG = config.get("App", "app_prog")
APP_DESCRIPTION = config.get("App", "app_description")
APP_VERSION = config.get("App", "app_version")

# notification
NOTIFICATION_NAME = config.get("Notification", "notification_name")
NOTIFICATION_TITLE = config.get("Notification", "notification_title")

# file
FOLDER_NAME = config.get("Folder", "folder_name")
ASSETS_FOLDER_PATH = os.path.join(os.path.dirname(__file__), "..", config.get("Folder", "assets_folder_path"))
ASSETS_ICONS_FOLDER = os.path.join(os.path.dirname(__file__), "..", config.get("Folder", "assets_icons_folder_path"))

# file
FILE_EXTENSION = config.get("File", "file_extension")

# server
API_ENDPOINT = config.get("Endpoints", "api_endpoint")
WS_URL = config.get("Endpoints", "ws_url")

# messages
def get_message(section: str, name: str = "") -> tuple[str, str]:
    title = config.get("Messages", f"{section}_title").format(name=name)
    message = config.get("Messages", f"{section}_message")
    return title, message