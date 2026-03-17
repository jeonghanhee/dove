from PyQt6.QtWidgets import QLineEdit

class InputField(QLineEdit):
    def __init__(self, placeholder="", is_password=False, parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        if is_password:
            self.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.setStyleSheet("""
            QLineEdit {
                background-color: #3D3D3D;
                color: white;
                border: 1px solid #555555;
                padding: 12px;
                border-radius: 6px;
            }
            QLineEdit:focus {
                border: 1px solid #4A90E2;
            }
        """)