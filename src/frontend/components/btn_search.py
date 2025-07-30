from pathlib import Path
import shutil
from PySide6.QtWidgets import QFileDialog, QPushButton, QMessageBox
from src.backend.utils.util import get_project_path

INPUT_DIR = get_project_path() / "input"

def get_project_root():
    return Path(__file__).resolve().parents[3]  # Ajuste o número conforme necessário

# INPUT_DIR = get_project_root() / "input"

print(f"INPUT_DIR: {INPUT_DIR}")
# /home/jp/Documents/excel_processor/src/backend/excel_processor/input/

class BtnSearch(QPushButton):
    def __init__(self, label_arquivo, parent=None):
        super().__init__("Adicionar arquivo", parent)
        self.label_arquivo = label_arquivo
        self.clicked.connect(self.show_file_dialog)

    def show_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar arquivo",
            "",
            "Excel Files (*.xlsx *.xls)"
        )
        print(f"Arquivo selecionado: {file_path}")
        if file_path:
            dest = INPUT_DIR / Path(file_path).name
            try:
                if Path(file_path).resolve() == dest.resolve():
                    self.label_arquivo.setText(f"Arquivo: {Path(file_path).name}")
                    QMessageBox.information(self, "Arquivo já está na pasta", f"O arquivo '{Path(file_path).name}' já está na pasta de input.")
                    return
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(file_path, dest)
                self.label_arquivo.setText(f"Arquivo: {Path(file_path).name}")
                QMessageBox.information(self, "Arquivo adicionado", f"Arquivo '{Path(file_path).name}' copiado para a pasta input.")
            except Exception as e:
                QMessageBox.critical(self, "Erro ao copiar", str(e))