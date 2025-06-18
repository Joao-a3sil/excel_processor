# filepath: src/frontend/windows/main_window.py
import sys
import threading
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QProgressBar, QMessageBox, QLabel
from PySide6.QtCore import QMetaObject, Qt, Q_ARG, Slot, Signal
from src.backend.main import main as backend_main
from src.frontend.components.btn_search import BtnSearch

class QtStream:
    def __init__(self, signal):
        self.signal = signal

    def write(self, message):
        if message.strip():
            self.signal.emit(message.strip())

    def flush(self):
        pass

class MainWindow(QMainWindow):
    backend_message = Signal(str)  # Sinal customizado

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excel Processor - Frontend")
        self.resize(600, 400)

        self.btn_generate = QPushButton("Gerar Data Base")
        self.btn_generate.clicked.connect(self.on_generate_database)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0)
        self.progress_bar.hide()
        self.label_arquivo = QLabel("Nenhum arquivo selecionado")
        self.btn_search = BtnSearch(self.label_arquivo)                

        layout = QVBoxLayout()
        layout.addWidget(self.label_arquivo)
        layout.addWidget(self.btn_search)
        layout.addWidget(self.btn_generate)
        layout.addWidget(self.progress_bar)        

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.statusBar().showMessage("Pronto")
        self.backend_message.connect(self.process_backend_message)

    def on_generate_database(self):
        self.progress_bar.show()
        self.btn_generate.setEnabled(False)
        process_name = "Gerar Data Base"
        self.statusBar().showMessage(f"Iniciando: {process_name}")

        def run_backend():
            sys_stdout_original = sys.stdout
            try:
                sys.stdout = QtStream(self.backend_message)
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