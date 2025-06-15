from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy

class LandingPage(QWidget):

    def __init__(self, page_change):
        super().__init__()
        layout = QVBoxLayout(self)
        self.setStyleSheet("background-color: #FFFACD;")  

        button_row = QHBoxLayout()
        button_row.setSpacing(20) 
        button_row.addStretch()

        # CV Analyzer button
        self.analyze_button = QPushButton("CV Analyzer")
        self.analyze_button.setMinimumWidth(180)
        self.analyze_button.setStyleSheet("""
            padding: 12px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 15px;
            background-color: #FFD700;
            color: black;
        """)
        self.analyze_button.clicked.connect(lambda: page_change(1))
        button_row.addWidget(self.analyze_button)

        # About button
        self.about_button = QPushButton("About")
        self.about_button.setMinimumWidth(180)
        self.about_button.setStyleSheet("""
            padding: 12px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 15px;
            background-color: #FFD700;
            color: black;
        """)
        self.about_button.clicked.connect(lambda: page_change(3))
        button_row.addWidget(self.about_button)

        button_row.addStretch()
        layout.addStretch()
        layout.addLayout(button_row)
        layout.addStretch()
