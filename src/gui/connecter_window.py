import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QLabel
from PyQt6.QtCore import Qt

root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

from src.gui.base_window import BaseWindow
from src.gui.components.input_field import InputField
from src.gui.components.button import Button
from src.config_loader import APP_ID, get_message
from src.network.auth import request_jwt_token, JwtToken
from src.network.notifier import send_notification
from src.app import DoveApp

class ConnecterWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self.app = DoveApp()
        self.setWindowTitle(f"{APP_ID} Connecter")
        self.setMinimumWidth(350)
        self.setup()

    def setup(self):
        is_connected = self.app.token is not None

        if is_connected:
            self.setup_disconnect_ui()
        else:
            self.setup_connect_ui()

    def setup_connect_ui(self):
        self.id_input = InputField(placeholder="Please enter your ID.")
        self.pw_input = InputField(placeholder="Please enter your Password.", is_password=True)
        self.pw_input.returnPressed.connect(self.handle_connect)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #FF6B6B; font-size: 12px; font-weight: bold; margin: 2px 5px;")
        self.error_label.hide()

        self.connect_button = Button("Connect")
        self.connect_button.clicked.connect(self.handle_connect)

        self.layout.addWidget(self.id_input)
        self.layout.addWidget(self.pw_input)
        self.layout.addWidget(self.error_label)
        self.layout.addWidget(self.connect_button)

    def setup_disconnect_ui(self):
        self.status_label = QLabel("You are currently connected to the server.")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #AAAAAA; margin-bottom: 10px;")
        
        self.disconnect_button = Button("Disconnect")
        self.disconnect_button.clicked.connect(self.handle_disconnect)
        
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.disconnect_button)

    def handle_connect(self):
        user_id = self.id_input.text().strip()
        user_pw = self.pw_input.text().strip()

        if not user_id or not user_pw:
            self.show_error("Please enter your ID and password.")
            return
        
        self.connect_button.setEnabled(False)
        self.connect_button.setText("Connecting...")
        
        new_token, error_msg = request_jwt_token(user_id, user_pw)
        if new_token:
            print("Connection Success")
            new_token.save()
            title, message = get_message("success_connect_server")
            send_notification(title, message)
            self.app.token = new_token
            self.close()
        else:
            self.show_error(error_msg)
            self.connect_button.setEnabled(True)
            self.connect_button.setText("Connect")

    def handle_disconnect(self):
        print("Disconnected.")
        JwtToken.delete()
        title, message = get_message("success_disconnect_server")
        send_notification(title, message)
        self.app.token = None
        self.close()

    def show_error(self, message):
        if hasattr(self, 'error_label'):
            self.error_label.setText(message)
            self.error_label.show()
            self.adjustSize()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConnecterWindow()  
    window.show()
    sys.exit(app.exec())