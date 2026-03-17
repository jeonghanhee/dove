from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt

class Button(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background-color: #4A90E2;
                color: white;
                font-weight: bold;
                padding: 13px;
                border-radius: 6px;
                margin-top: 5px;
            }
            QPushButton:hover {
                background-color: #357ABD;
            }
            QPushButton:pressed {
                background-color: #2A5A8E;
            }
        """)