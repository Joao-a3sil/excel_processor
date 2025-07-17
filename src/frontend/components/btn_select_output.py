from PySide6.QtWidgets import QPushButton, QFileDialog
from PySide6.QtGui import QIcon

class BtnSelectOutput(QPushButton):
    def __init__(self, parent=None, callback=None):
        super().__init__("Selecionar Pasta de Saída", parent)
        self.setStyleSheet("background-color: #2196F3; color: white;")
        self.setIcon(QIcon.fromTheme("folder"))
        self.clicked.connect(self.select_output_dir)
        self._callback = callback

    def select_output_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Selecione a pasta de saída")
        if dir_path and self._callback:
            self._callback(dir_path)