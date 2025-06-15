# detail_page.py
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit,
    QGroupBox, QPushButton, QScrollArea
)
from PyQt5.QtCore import Qt
from src.utils.normalize_pdf import PDFTextConverter
from src.algorithms.Regex import Regex

from src.controller.Controller import Controller
from src.database.db_config import *
from src.database.db_search import *

class DetailPage(QWidget):

    def __init__(self, page_change, path=None):
        super().__init__()

        self.path = path
        if self.path is not None:
            print("extracting")
            self.data = self.extract_data(self.path)
            print(self.data)

        main_layout = QVBoxLayout(self)

        # Header
        header_widget = QWidget()
        header_widget.setMaximumHeight(80)
        header_widget.setStyleSheet("background-color: #FFFACD; border-radius: 10px;")
        header = QHBoxLayout(header_widget)
        header.setContentsMargins(10, 10, 10, 10)

        back_button = QPushButton("Back")
        back_button.setMaximumWidth(100)
        back_button.clicked.connect(lambda: page_change(1))
        back_button.setStyleSheet("padding: 10px; font-size: 14px; border-radius: 15px; background-color: #FFD700;")
        header.addWidget(back_button)

        title = QLabel("View Summary")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: 600; border-radius: 15px; color: black;")
        header.addWidget(title)

        main_layout.addWidget(header_widget)

        # Content Layout
        content_layout = QHBoxLayout()

        # Left Column (Biodata)
        self.biodata_layout = QVBoxLayout()
        
        self.name_label = QLabel("Nama: -")
        self.name_label.setStyleSheet("font-size: 14px;")
        self.birthdate_label = QLabel("Birthdate: -")
        self.birthdate_label.setStyleSheet("font-size: 14px;")
        self.address_label = QLabel("Address: -")
        self.address_label.setStyleSheet("font-size: 14px;")
        self.phone_label = QLabel("Phone: -")
        self.phone_label.setStyleSheet("font-size: 14px;")

        self.biodata_layout.addWidget(self.name_label)
        self.biodata_layout.addWidget(self.birthdate_label)
        self.biodata_layout.addWidget(self.address_label)
        self.biodata_layout.addWidget(self.phone_label)

        self.biodata_box = QGroupBox("Biodata Diri")
        self.biodata_box.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                background-color: #FFF8DC;
                padding: 10px;
                border-radius: 15px;
            }
        """)
        self.biodata_box.setLayout(self.biodata_layout)
        self.biodata_box.setFixedWidth(300)
        content_layout.addWidget(self.biodata_box)

        # Right Column inside Scroll Area
        right_widget = QWidget()
        self.right_column = QVBoxLayout(right_widget)

        # ------------ SKILL ------------
        self.skill_box = QGroupBox("Skill")
        self.skill_box.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                background-color: #FFF8DC;
                padding: 10px;
                border-radius: 15px;
            }
        """)
        self.skill_layout = QVBoxLayout()
        self.skill_box.setLayout(self.skill_layout)
        self.right_column.addWidget(self.skill_box)

        # ------------ EXPERIENCES ------------
        self.job_box = QGroupBox("Job History")
        self.job_box.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                background-color: #FFF8DC;
                padding: 10px;
                border-radius: 15px;
            }
        """)
        self.job_layout = QVBoxLayout()
        self.job_box.setLayout(self.job_layout)
        self.right_column.addWidget(self.job_box)

        # ------------ EDUCATION ------------
        self.education_box = QGroupBox("Education")
        self.education_box.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                background-color: #FFF8DC;
                padding: 10px;
                border-radius: 15px;
            }
        """)
        self.education_layout = QVBoxLayout()
        self.education_box.setLayout(self.education_layout)
        self.right_column.addWidget(self.education_box)

        # Scroll Area for Right Column
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none; background-color: transparent;")
        scroll_area.setWidget(right_widget)

        content_layout.addWidget(scroll_area)
        content_layout.setStretch(1, 1)

        main_layout.addLayout(content_layout)

    def create_section_box(self, title, content_text=""):
        box = QGroupBox(title)
        box.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                background-color: #FFF8DC;
                padding: 10px;
                border-radius: 15px;
            }
        """)
        layout = QVBoxLayout()
        content = QLabel(content_text)
        content.setStyleSheet("background-color: white; font-size: 14px; padding: 6px;")
        layout.addWidget(content)
        box.setLayout(layout)
        return box

    def populate_section(self, layout, items, fields=None):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if all(isinstance(i, str) for i in items): 
            for skill in items:
                label = QLabel(f"• {skill}")
                label.setStyleSheet("background-color: white; font-size: 14px; padding: 4px; color: black; border-radius: 5px;")
                layout.addWidget(label)
            return

        for item in items:
            entry_widget = QWidget()
            entry_layout = QVBoxLayout(entry_widget)
            entry_layout.setContentsMargins(5, 5, 5, 5)

            for field in fields:
                value = item.get(field, "-")
                if isinstance(value, list):
                    title = QLabel(f"{field.capitalize()}:")
                    title.setStyleSheet("font-weight: bold; font-size: 14px; color: black;")
                    entry_layout.addWidget(title)

                    for desc in value:
                        desc_label = QLabel(f"• {desc}")
                        desc_label.setStyleSheet("color: black; font-size: 14px; padding-left: 10px;")
                        entry_layout.addWidget(desc_label)
                else:
                    label = QLabel(f"{field.capitalize()}: {value}")
                    label.setStyleSheet("background-color: white; font-size: 14px; padding: 4px; border-radius: 6px; color: black;")
                    entry_layout.addWidget(label)

            layout.addWidget(entry_widget)

    def update_data(self):
        experience, education, skill = self.data
        if experience is not None:
            self.populate_section(self.job_layout, experience, ["position", "company", "location", "description"])
        if education is not None:
            self.populate_section(self.education_layout, education, ["degree", "field", "institution", "year", "location"])
        if skill is not None:
            self.populate_section(self.skill_layout, skill)
        if self.id is not None:
            data_detail = Controller.getDataByIndex(self.id)
            self.name_label.setText(f"Nama: {data_detail['first_name'] + data_detail['last_name']}")
            self.birthdate_label.setText(f"Birthdate: {data_detail['date_of_birth']}")
            self.address_label.setText(f"Address: {data_detail['address']}")
            self.phone_label.setText(f"Phone: {data_detail['phone_number']}")
            self.biodata_box.setStyleSheet("""
                QGroupBox {
                    font-weight: bold;
                    font-size: 16px;
                    background-color: #FFF8DC;
                    padding: 10px;
                    border-radius: 15px;
                }
                QLabel {
                    color: black;
                    font-size: 14px;
                }
            """)
        return

    def extract_data(self, path):
        (experience, education, skill) = Controller.get_data(path)
        self.data = (experience, education, skill)

    def load_path(self, path, index):
        self.path = path
        self.id = index
        self.extract_data(path)
        self.update_data()
        return
