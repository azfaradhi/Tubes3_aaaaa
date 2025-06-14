from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout

class LandingPage(QWidget):

    def __init__(self, page_change):
        super().__init__()
        layout = QVBoxLayout(self)

        # --- CV Analyzer button centered ---
        analyze_row = QHBoxLayout()
        analyze_row.addStretch()
        self.analyze_button = QPushButton("CV Analyzer")
        self.analyze_button.setMinimumWidth(200)
        self.analyze_button.setStyleSheet("padding: 10px; border-radius: 15px; background-color: #ccc;")
        self.analyze_button.clicked.connect(lambda: page_change(1))
        analyze_row.addWidget(self.analyze_button)
        analyze_row.addStretch()
        layout.addLayout(analyze_row)

        # --- About button centered ---
        about_row = QHBoxLayout()
        about_row.addStretch()
        self.about_button = QPushButton("About")
        self.about_button.setMinimumWidth(200)
        self.about_button.setStyleSheet("padding: 10px; border-radius: 15px; background-color: #ccc;")
        self.about_button.clicked.connect(lambda: page_change(3))
        about_row.addWidget(self.about_button)
        about_row.addStretch()
        layout.addLayout(about_row)
