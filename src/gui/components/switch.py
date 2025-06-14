from PyQt5.QtWidgets import QWidget, QCheckBox, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal


class ToggleSwitch(QWidget):
    toggled = pyqtSignal(bool) 

    def __init__(self, label_text="", parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.checkbox = QCheckBox()
        self.checkbox.setTristate(False)
        self.checkbox.setChecked(False)

        self.checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 40px;
                height: 20px;
            }
            QCheckBox::indicator:unchecked {
                background-color: #ccc;
                border-radius: 10px;
            }
            QCheckBox::indicator:checked {
                background-color: #4CAF50;
                border-radius: 10px;
            }
        """)

        layout.addWidget(self.checkbox, alignment=Qt.AlignLeft)

        self.checkbox.stateChanged.connect(self.emit_toggle)

    def emit_toggle(self, state):
        self.toggled.emit(state == Qt.Checked)

    def isChecked(self):
        return self.checkbox.isChecked()

    def setChecked(self, value: bool):
        self.checkbox.setChecked(value)
