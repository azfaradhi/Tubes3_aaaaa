from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
)

class AboutPage(QWidget):

    def __init__(self, page_change):
        super().__init__()
        layout = QVBoxLayout(self)

        # self.radhi = 