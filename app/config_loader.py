import os
import configparser

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config.ini")

config = configparser.ConfigParser()
config.read(CONFIG_PATH, encoding="utf-8")

# app
APP_NAME = config.get("App", "app_name")
APP_TITLE = config.get("App", "app_title")

# file
FOLDER_NAME = config.get("Folder", "folder_name")
ASSETS_FOLDER_PATH = os.path.join(os.path.dirname(__file__), "..", config.get("Folder", "assets_folder_path"))
ASSETS_ICONS_FOLDER = os.path.join(os.path.dirname(__file__), "..", config.get("Folder", "assets_icons_folder_path"))

# file
FILE_EXTENSION = config.get("File", "file_extension")

# messages
def get_message(section: str, name: str) -> tuple[str, str]:
    title = config.get("Messages", f"{section}_title").format(name=name)
    message = config.get("Messages", f"{section}_message")
    return title, message