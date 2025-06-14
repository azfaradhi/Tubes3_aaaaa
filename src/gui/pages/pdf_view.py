from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import fitz 

class PDFPreview(QWidget):
    def __init__(self, pdf_path):
        super().__init__()
        self.setWindowTitle("PDF Preview")
        self.resize(800, 600)

        layout = QVBoxLayout(self)

        scroll_area = QScrollArea()
        self.pdf_label = QLabel()
        self.pdf_label.setAlignment(Qt.AlignCenter)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.pdf_label)

        layout.addWidget(scroll_area)
        self.setLayout(layout)

        self.load_pdf(pdf_path)

    def load_pdf(self, path):
        doc = fitz.open(path)
        print(path)
        page = doc.load_page(0)  
        pix = page.get_pixmap()  
        mode = QImage.Format_RGBA8888 if pix.alpha else QImage.Format_RGB888
        image = QImage(pix.samples, pix.width, pix.height, pix.stride, mode)
        self.pdf_label.setPixmap(QPixmap.fromImage(image))
