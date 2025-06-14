from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QRadioButton, QButtonGroup, QLabel
)
from PyQt5.QtCore import Qt

class RadioAlgorithm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("")
        self.resize(300, 150)

        layout = QVBoxLayout()

        # Radio buttons
        self.radio1 = QRadioButton("KMP")
        self.radio1.setStyleSheet("""
            QRadioButton {
                spacing: 8px;
                font-size: 12px;
                font-weight: 500;
                color: #333;
            }

            QRadioButton::indicator {
                width: 12px;
                height: 12px;
                border-radius: 9px;
                border: 1px solid #999;
                background-color: #fff;
            }

            QRadioButton::indicator:checked {
                background-color: #0078d4;
                border: 1px solid #0078d4;
            }

            QRadioButton::hover {
                color: #000;
            }
        """)
        
        self.radio2 = QRadioButton("BM")
        self.radio2.setStyleSheet("""
            QRadioButton {
                spacing: 8px;
                font-size: 12px;
                font-weight: 500;
                color: #333;
            }

            QRadioButton::indicator {
                width: 12px;
                height: 12px;
                border-radius: 9px;
                border: 1px solid #999;
                background-color: #fff;
            }

            QRadioButton::indicator:checked {
                background-color: #0078d4;
                border: 1px solid #0078d4;
            }

            QRadioButton::hover {
                color: #000;
            }
        """)

        self.radio3 = QRadioButton("Lavenstein")
        self.radio3.setStyleSheet("""
            QRadioButton {
                spacing: 8px;
                font-size: 12px;
                font-weight: 500;
                color: #333;
            }

            QRadioButton::indicator {
                width: 12px;
                height: 12px;
                border-radius: 9px;
                border: 1px solid #999;
                background-color: #fff;
            }

            QRadioButton::indicator:checked {
                background-color: #0078d4;
                border: 1px solid #0078d4;
            }

            QRadioButton::hover {
                color: #000;
            }
        """)

        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.radio1, 1)
        self.button_group.addButton(self.radio2, 2)
        self.button_group.addButton(self.radio3, 3)

        layout.addWidget(self.radio1)
        layout.addWidget(self.radio2)
        layout.addWidget(self.radio3)

        self.setLayout(layout)

    def get_selected_option(self):
        selected_button = self.button_group.checkedButton()
        return selected_button.text() if selected_button else None