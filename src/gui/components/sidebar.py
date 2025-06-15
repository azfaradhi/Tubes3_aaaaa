from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QSizePolicy,
    QLineEdit
)
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt, QPropertyAnimation
from src.gui.components.radio import RadioAlgorithm

from PyQt5.QtCore import pyqtSignal

class Sidebar(QWidget):
    submit_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.expanded_width = 250
        self.collapsed_width = 30
        self.is_expanded = True

        self.setFixedWidth(self.expanded_width + 20)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        # Layout
        self.wrapper = QFrame(self)
        self.wrapper.setStyleSheet("background-color: #FFFACD;")
        self.wrapper.setGeometry(0, 0, self.expanded_width, self.height())

        self.sidebar_layout = QVBoxLayout()
        self.sidebar_layout.setAlignment(Qt.AlignTop)
        self.wrapper.setLayout(self.sidebar_layout)

        # ------------- Title -------------
        self.title = QLabel("CV Analyzer App")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("""
            font-size: 20pt;
            font-weight: bold;
            color: #2c3e50;
        """)
        self.sidebar_layout.addWidget(self.title)

        # ------------- Input Fields -------------
        self.label = QLabel("Keywords:")
        self.label.setStyleSheet("color: black; font-size: 14px;")
        self.keyword_input = QLineEdit()
        self.keyword_input.setFixedHeight(30)
        self.keyword_input.setStyleSheet("background-color: white; border-radius: 5px; font-size: 14px; color: black;")
        self.sidebar_layout.addWidget(self.label)
        self.sidebar_layout.addWidget(self.keyword_input)

        self.label = QLabel("Pilih Algoritma:")
        self.label.setStyleSheet("color: black; font-size: 14px;")
        self.toggle = RadioAlgorithm()
        self.sidebar_layout.addWidget(self.label)
        self.sidebar_layout.addWidget(self.toggle)

        self.label = QLabel("Top Matches:")
        self.label.setStyleSheet("color: black; font-size: 14px;")
        self.text_input = QLineEdit()
        self.text_input.setFixedHeight(30)
        self.text_input.setStyleSheet("background-color: white; border-radius: 5px; font-size: 14px; color: black;")
        self.sidebar_layout.addWidget(self.label)
        self.sidebar_layout.addWidget(self.text_input)

        # ------------- Analyze button -------------
        self.upload_button = QPushButton("Analyze")
        self.upload_button.setStyleSheet("""
            padding: 10px;
            border-radius: 15px;
            background-color: #FFD700;
            font-size: 14px;
            font-weight: bold;
        """)
        self.upload_button.clicked.connect(self.validate_and_submit)
        self.sidebar_layout.addStretch()
        self.sidebar_layout.addWidget(self.upload_button)

        # ------------- Toggle Button -------------
        self.toggle_button = QPushButton(">", self)
        self.toggle_button.setFixedSize(50, 80)
        self.toggle_button.clicked.connect(self.toggle_sidebar)
        self.toggle_button.raise_()
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #FFFACD;
                border: none;
                font-size: 16px;
            }
            QPushButton:pressed {
                background-color: #FFEFD5;
            }
            QPushButton:focus {
                outline: none;
            }
        """)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.wrapper.setGeometry(0, 0, self.width() - 20, self.height())
        y = self.height() // 2 - self.toggle_button.height() // 2
        x = self.width() - (self.toggle_button.width() // 2)
        self.toggle_button.move(x, y)

    def toggle_sidebar(self):
        animation = QPropertyAnimation(self, b"minimumWidth")
        animation.setDuration(300)

        if self.is_expanded:
            animation.setStartValue(self.expanded_width)
            animation.setEndValue(self.collapsed_width)
            self.title.setText("")
            self.upload_button.setText("")
        else:
            animation.setStartValue(self.collapsed_width)
            animation.setEndValue(self.expanded_width)
            self.title.setText("CV Analyzer App")
            self.upload_button.setText("Analyze")

        self.is_expanded = not self.is_expanded
        animation.start()
        self.animation = animation

    def get_parameter(self):
        return (
            self.keyword_input.text(),
            self.toggle.get_selected_option(),
            int(self.text_input.text())
        )
    
    def validate_and_submit(self):
        keyword = self.keyword_input.text().strip()
        algorithm = self.toggle.get_selected_option()
        top_matches = self.text_input.text().strip()

        if not keyword or not algorithm or not top_matches:
            QMessageBox.warning(self, "Incomplete Input", "Please fill in all fields and select an algorithm.")
            return

        if not top_matches.isdigit() or int(top_matches) <= 0:
            QMessageBox.warning(self, "Invalid Input", "Top Matches must be a positive number.")
            return

        # If all valid, emit the submit signal
        self.submit_clicked.emit()