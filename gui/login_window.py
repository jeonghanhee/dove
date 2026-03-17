import sys

from PyQt6.QtWidgets import QApplication, QLabel
from PyQt6.QtCore import Qt

from base_window import BaseWindow
from components.input_field import InputField
from components.button import Button

from src.storage.loader import APP_ID

class LoginWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_ID} Login")
        self.setMinimumWidth(350)
        self.setWindowFlags(Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.WindowTitleHint)
        self.setup()

    def setup(self):
        self.id_input = InputField(placeholder="Enter ID")
        self.pw_input = InputField(placeholder="Enter Password", is_password=True)
        self.pw_input.returnPressed.connect(self.handle_login)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #FF6B6B; font-size: 12px; font-weight: bold; margin: 2px 5px;")
        self.error_label.hide()

        self.login_button = Button("Login")
        self.login_button.clicked.connect(self.handle_login)
        
        self.layout.addWidget(self.id_input)
        self.layout.addWidget(self.pw_input)
        self.layout.addWidget(self.error_label)
        self.layout.addWidget(self.login_button)

        self.adjustSize()

    def handle_login(self):
        user_id = self.id_input.text().strip()
        user_pw = self.pw_input.text().strip()

        if not user_id or not user_pw:
            self.show_error("Please check your ID or Password.")
            return
        
        # login logic

    def show_error(self, message):
        self.error_label.setText(message)
        self.error_label.show()
        self.adjustSize()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()  
    window.show()
    sys.exit(app.exec()) 