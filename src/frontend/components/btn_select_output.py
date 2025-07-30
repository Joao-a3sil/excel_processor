from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon
import os
import subprocess
import sys
from pathlib import Path

class BtnSelectOutput(QPushButton):
    def __init__(self, parent=None, output_dir=None):
        super().__init__("Abrir Pasta de Saída", parent)
        self.setStyleSheet("background-color: #2196F3; color: white;")
        self.setIcon(QIcon.fromTheme("folder"))
        # Calcula o caminho absoluto da pasta output a partir deste arquivo
        if output_dir is None:
            # Sobe 3 níveis: components -> frontend -> src -> excel_processor
            self.output_dir = str(Path(__file__).resolve().parents[3] / "output")
        else:
            self.output_dir = output_dir
        self.clicked.connect(self.open_output_dir)

    def open_output_dir(self):
        path = os.path.abspath(self.output_dir)
        if not os.path.exists(path):
            os.makedirs(path)
        if sys.platform.startswith("linux"):
            subprocess.Popen(["xdg-open", path])
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        elif sys.platform == "win32":
            os.startfile(path)