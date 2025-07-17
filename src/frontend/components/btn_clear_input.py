from pathlib import Path
import os
from PySide6.QtWidgets import QPushButton, QMessageBox
from src.backend.utils.util import get_project_path

INPUT_DIR = get_project_path() / "input"

class BtnClearInput(QPushButton):
    def __init__(self, label_arquivo, parent=None):
        super().__init__("Limpar arquivos de input", parent)
        self.label_arquivo = label_arquivo
        self.clicked.connect(self.limpar_arquivos_input)

    def limpar_arquivos_input(self):
        reply = QMessageBox.question(
            self,
            "Confirmação",
            "Tem certeza que deseja apagar TODOS os arquivos Excel da pasta de input?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            arquivos = list(INPUT_DIR.glob("*.xlsx")) + list(INPUT_DIR.glob("*.xls"))
            if not arquivos:
                QMessageBox.information(self, "Limpar arquivos", "Nenhum arquivo Excel encontrado na pasta de input.")
                return
            for arquivo in arquivos:
                try:
                    os.remove(arquivo)
                except Exception as e:
                    QMessageBox.critical(self, "Erro ao apagar", f"Erro ao apagar {arquivo.name}: {e}")
                    return
            self.label_arquivo.setText("Nenhum arquivo selecionado")
            QMessageBox.information(self, "Limpar arquivos", "Todos os arquivos Excel foram apagados da pasta de input.")