# filepath: src/frontend/windows/main_window.py
import sys
import threading
import os
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QProgressBar, QMessageBox, QLabel, QApplication, QGroupBox, QFileDialog
from PySide6.QtCore import QMetaObject, Qt, Q_ARG, Slot, Signal
from PySide6.QtGui import QIcon
from src.backend.main import main as backend_main
from src.frontend.components.btn_search import BtnSearch
from src.frontend.components.btn_clear_input import BtnClearInput
from src.frontend.components.btn_select_output import BtnSelectOutput
from src.frontend.utils.print_to_signal_stream import PrintToSignalStream

class MainWindow(QMainWindow):
    backend_message = Signal(str)

    def __init__(self):
        super().__init__()
        self.output_dir = None  # <-- novo atributo
        self.setWindowTitle("Excel Processor - Frontend")
        self.resize(600, 400)
        self.setStyleSheet("""
            QWidget { background-color: #232629; color: #f0f0f0; }
            QPushButton { background-color: #444; color: #fff; border-radius: 4px; padding: 6px 12px; }
            QPushButton:hover { background-color: #666; }
            QProgressBar { background: #333; color: #fff; border-radius: 4px; }
        """)
        self._setup_widgets()
        self._setup_layout()
        self._setup_signals()
        self.statusBar().showMessage("Pronto")

    def _setup_widgets(self):
        self.label_titulo = QLabel("Excel Processor")
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.label_titulo.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 16px;")
        self.label_arquivo = QLabel("Nenhum arquivo selecionado")
        self.label_arquivo.setStyleSheet("font-size: 14px; color: #333; padding: 6px;")
        self.btn_search = BtnSearch(self.label_arquivo)
        self.btn_generate = QPushButton("Gerar Data Base")
        self.btn_generate.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        self.btn_generate.setIcon(QIcon.fromTheme("document-save"))
        self.btn_generate.clicked.connect(self.on_generate_database)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setStyleSheet("QProgressBar {height: 18px;}")
        self.progress_bar.hide()
        self.btn_limpar = BtnClearInput(self.label_arquivo)
        self.btn_limpar.setStyleSheet("background-color: #f44336; color: white;")
        self.btn_limpar.setIcon(QIcon.fromTheme("edit-delete"))
        self.btn_sair = QPushButton("Sair")
        self.btn_sair.setStyleSheet("background-color: #555; color: white;")
        self.btn_sair.setIcon(QIcon.fromTheme("application-exit"))
        self.btn_sair.clicked.connect(self.on_btn_sair_clicked)
        self.btn_select_output = BtnSelectOutput(parent=self, callback=self.on_output_dir_selected)

    def _setup_layout(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        self.label_titulo = QLabel("Excel Processor")
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.label_titulo.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 16px;")
        layout.addWidget(self.label_titulo)

        layout.addWidget(self.label_arquivo)
        layout.addWidget(self.btn_search)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.btn_select_output)  # <-- adicione antes do grupo de ações

        group = QGroupBox("Ações")
        group_layout = QVBoxLayout()
        group_layout.addWidget(self.btn_generate)
        group_layout.addWidget(self.btn_limpar)
        group_layout.addWidget(self.btn_sair)
        group.setLayout(group_layout)
        layout.addWidget(group)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def _setup_signals(self):
        self.backend_message.connect(self.process_backend_message)

    def on_generate_database(self):
        """Inicia o processamento do backend em uma thread separada."""
        if not self.output_dir:
            self.show_error("Selecione a pasta de saída antes de gerar o Data Base.")
            return
        self.progress_bar.show()
        self.btn_generate.setEnabled(False)
        process_name = "Gerar Data Base"
        self.statusBar().showMessage(f"Iniciando: {process_name}")

        def run_backend():
            sys_stdout_original = sys.stdout
            try:
                sys.stdout = PrintToSignalStream(self.backend_message)
                os.environ["EXCEL_PROCESSOR_OUTPUT_DIR"] = self.output_dir  # <-- aqui
                backend_main()
            except Exception as e:
                self.backend_message.emit(f"Erro: {e}")
            finally:
                sys.stdout = sys_stdout_original
                self.backend_message.emit("PROCESSAMENTO_FINALIZADO")

        threading.Thread(target=run_backend, daemon=True).start()

    def show_info(self, message):
        QMessageBox.information(self, "Informação", message)

    def show_error(self, message):
        QMessageBox.critical(self, "Erro", message)

    @Slot(str)
    def process_backend_message(self, message):
        """Processa mensagens vindas do backend e atualiza a interface."""
        if message.startswith("ETAPA_STATUS:"):
            etapa = message.split(":", 1)[1].strip()
            self.statusBar().showMessage(f"Processando: {etapa}")
        elif message.startswith("Arquivo Processado:"):
            arquivo = message.split(":", 1)[1].strip()
            self.label_arquivo.setText(f"Arquivo: {arquivo}")
        elif message.startswith("ETAPA_CONCLUIDA:"):
            etapa = message.split(":", 1)[1].strip()
            self.statusBar().showMessage(f"Etapa concluída: {etapa}")
        elif message.startswith("Sucesso no processamento:"):
            tempo = message.split(":", 1)[1].strip()
            self.show_info(f"Processamento finalizado com sucesso!\nTempo total: {tempo}")
        elif message.startswith("Erro:"):
            self.show_error(message)
        elif message == "PROCESSAMENTO_FINALIZADO":
            self.progress_bar.hide()
            self.btn_generate.setEnabled(True)
            self.statusBar().showMessage("Pronto")

    def on_btn_sair_clicked(self):
        QApplication.quit()   

    def on_output_dir_selected(self, dir_path):
        self.output_dir = dir_path
        self.statusBar().showMessage(f"Pasta de saída: {dir_path}")