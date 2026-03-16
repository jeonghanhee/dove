from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
from .folder import Folder
from .config_loader import FOLDER_NAME, APP_NAME, APP_TITLE
from . import state

def create_image():
    image = Image.new('RGB', (64, 64), color='white')
    draw = ImageDraw.Draw(image)
    draw.ellipse((8, 8, 56, 56), fill='gray')
    return image

def quit_action(icon):
    icon.stop()

def run():
    state.folder = Folder(FOLDER_NAME)
    state.folder.create()

    icon = Icon(APP_NAME, create_image(), APP_TITLE, menu=Menu(MenuItem("Quit", lambda icon, item: quit_action(icon))))
    icon.run()