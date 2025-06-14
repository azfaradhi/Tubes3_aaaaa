# detail_page.py
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit,
    QGroupBox, QPushButton
)
from PyQt5.QtCore import Qt
from utils.normalize_pdf import PDFTextConverter
from algorithms.Regex import Regex


class DetailPage(QWidget):
    def __init__(self, page_change):
        super().__init__()

        # ------------ extracting data ------------


        # -----------------------------------------


        main_layout = QVBoxLayout(self)

        header_widget = QWidget()
        header_widget.setMaximumHeight(80) 
        header_widget.setStyleSheet("background-color: #EFEFEF; border-radius: 10px;")

        header = QHBoxLayout(header_widget)
        header.setContentsMargins(10, 10, 10, 10)

        # Back button
        back_button = QPushButton("Back")
        back_button.setMaximumWidth(100)
        back_button.clicked.connect(lambda: page_change(1))
        back_button.setStyleSheet("padding: 10px; border-radius: 15px; background-color: #ccc;")
        header.addWidget(back_button)

        # Title
        title = QLabel("View Summary")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: 500; border-radius: 15px; color: black;")
        header.addWidget(title)

        main_layout.addWidget(header_widget)  # ✅ Add the header widget instead of layout

        # --- Content Layout ---
        content_layout = QHBoxLayout()

        # Left Column (Biodata)
        biodata_box = QGroupBox("Biodata Diri")
        biodata_box.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                background-color: #D3D3D3;
                padding: 10px;
                border-radius: 15px;
            }
        """)
        biodata_layout = QVBoxLayout()

        biodata_layout.addWidget(QLabel("Nama"))
        biodata_layout.addWidget(QLabel("Birthdate"))
        biodata_layout.addWidget(QLabel("Address"))
        biodata_layout.addWidget(QLabel("Phone"))

        biodata_box.setLayout(biodata_layout)
        biodata_box.setFixedWidth(300)

        content_layout.addWidget(biodata_box)

        # Right Column (Skill, Job History, Education)
        right_column = QVBoxLayout()

        skill_box = self.create_section_box("Skill", "item 01   item 02")
        right_column.addWidget(skill_box)

        job_box = self.create_section_box("Job History")
        right_column.addWidget(job_box)

        education_box = self.create_section_box("Education")
        right_column.addWidget(education_box)

        content_layout.addLayout(right_column)
        content_layout.setStretch(1, 1)

        main_layout.addLayout(content_layout)

    def create_section_box(self, title, content_text=""):
        box = QGroupBox(title)
        box.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                background-color: #D3D3D3;
                padding: 10px;
                border-radius: 15px;
            }
        """)
        layout = QVBoxLayout()
        content = QLabel(content_text)
        content.setStyleSheet("background-color: white; padding: 6px;")
        layout.addWidget(content)
        box.setLayout(layout)
        return box


    def extract_data(self):
        pdf_converter = PDFTextConverter(max_workers=8)
        pdf_converter.set_pdf_path("data/HR/11763983.pdf")
        text = pdf_converter.to_text_raw("data/HR/11763983.pdf")
        regex = Regex(text)
        print(regex.extract_experience())
        return