from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon
import os
import subprocess
import sys

class BtnSelectOutput(QPushButton):
    def __init__(self, parent=None, output_dir="output"):
        super().__init__("Abrir Pasta de Saída", parent)
        self.setStyleSheet("background-color: #2196F3; color: white;")
        self.setIcon(QIcon.fromTheme("folder"))
        self.output_dir = output_dir
        self.clicked.connect(self.open_output_dir)

    def open_output_dir(self):
        path = os.path.abspath(self.output_dir)
        if sys.platform.startswith("linux"):
            subprocess.Popen(["xdg-open", path])
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        elif sys.platform == "win32":
            os.startfile(path)