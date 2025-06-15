from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath

class AboutUs(QWidget):
    def __init__(self, page_change):
        super().__init__()

        self.setStyleSheet("background-color: #FFFACD;")
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)

        top_row = QHBoxLayout()
        self.back_button = QPushButton("Back")
        self.back_button.setStyleSheet("""
            padding: 8px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 10px;
            background-color: #FFD700;
            color: white;
        """)
        self.back_button.clicked.connect(lambda: page_change(0))
        top_row.addWidget(self.back_button, alignment=Qt.AlignLeft)
        top_row.addStretch()
        main_layout.addLayout(top_row)

        main_layout.addStretch()

        three_section_row = QHBoxLayout()
        three_section_row.setSpacing(30)

        data = [
            ["src/gui/assets/foto-radhi.jpeg", "Azfa Radhiyya Hakim", "berdasanlah kau raja dunia"],
            ["src/gui/assets/foto-barru.png", "Barru Adi Utomo", "dsadsa"],
            ["src/gui/assets/foto-rafif.jpeg", "Rafif Farras", "apaya"]
        ]


        for i in range(3):
            three_section_row.addLayout(self.create_profile_section(data[i]))

        main_layout.addLayout(three_section_row)

        main_layout.addStretch()

    def create_profile_section(self, data):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        image_size = 160

        # Image placeholder
        image_label = QLabel()
        pixmap = QPixmap(data[0])  
        scaled_pixmap = pixmap.scaled(image_size, image_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

        # Create a circular mask
        rounded_pixmap = QPixmap(image_size, image_size)
        rounded_pixmap.fill(Qt.transparent)

        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addEllipse(0, 0, image_size, image_size)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, scaled_pixmap)
        painter.end()

        # Set into QLabel
        image_label = QLabel()
        image_label.setPixmap(rounded_pixmap)
        image_label.setFixedSize(image_size, image_size)
        image_label.setStyleSheet("background: transparent;")
        layout.addWidget(image_label, alignment=Qt.AlignCenter)

        # Name placeholder
        name_label = QLabel(data[1])
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px; color: black;")
        layout.addWidget(name_label)

        # Quote placeholder
        quote_label = QLabel(data[2])
        quote_label.setWordWrap(True)
        quote_label.setAlignment(Qt.AlignCenter)
        quote_label.setStyleSheet("font-style: italic; color: #555; padding: 5px;")
        layout.addWidget(quote_label)

        return layout
