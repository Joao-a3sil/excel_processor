from pathlib import Path
import shutil
from PySide6.QtWidgets import QFileDialog, QPushButton

from frontend.utils.log import log_info

INPUT_DIR = Path(__file__).resolve().parent.parent / "backend" / "excel_processor" / "input"

class BtnSearch(QPushButton):
    def __init__(self, log_widget, parent=None):
        super().__init__("Adicionar arquivo", parent)
        self.log_widget = log_widget
        self.clicked.connect(self.show_file_dialog)

    def show_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecionar arquivo", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            dest = INPUT_DIR / Path(file_path).name
            shutil.copy(file_path, dest)
            log_info(self.log_widget, f"Arquivo '{Path(file_path).name}' copiado para a pasta input.")