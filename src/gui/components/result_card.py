from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt

class Card(QWidget):
    def __init__(self, title_text="Card Title"):
        super().__init__()

        # Force size to make sure style applies
        self.setMinimumSize(200, 120)
        self.setSizePolicy(QWidget.sizePolicy(self))

        # Wrapper frame inside the card
        wrapper = QFrame()
        wrapper.setStyleSheet("""
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 6px;
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(wrapper)

        inner_layout = QVBoxLayout(wrapper)
        inner_layout.setContentsMargins(10, 10, 10, 10)

        # Header
        title_bar = QHBoxLayout()
        title = QLabel(title_text)

        title_bar.addWidget(title)
        title_bar.addStretch()

        inner_layout.addLayout(title_bar)

        # Subtitle
        subtitle = QLabel("")
        inner_layout.addWidget(subtitle)
        inner_layout.addStretch()

        # Footer
        footer = QHBoxLayout()
        for _ in range(3):
            icon = QLabel("a")
            footer.addWidget(icon)
        inner_layout.addLayout(footer)
