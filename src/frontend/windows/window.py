# filepath: src/frontend/windows/main_window.py
import sys
import time
import threading
import io
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QProgressBar, QMessageBox, QLabel
from PySide6.QtCore import QMetaObject, Qt, Q_ARG, Slot, Signal
from src.backend.main import main as backend_main
from src.frontend.components.btn_search import BtnSearch

class StatusBarRedirector:
    def __init__(self, window):
        self.window = window

    def write(self, message):
        if message.strip():
            QMetaObject.invokeMethod(
                self.window,
                "process_backend_message",
                Qt.QueuedConnection,
                Q_ARG(str, message)
            )

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
        self.btn_teste = QPushButton("Teste")
        self.btn_teste.clicked.connect(lambda: print("Teste clicado!"))

        layout = QVBoxLayout()
        layout.addWidget(self.label_arquivo)
        layout.addWidget(self.btn_search)
        layout.addWidget(self.btn_generate)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.btn_teste)

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
            start_time = time.time()
            buffer = io.StringIO()
            try:
                # Redireciona prints do backend para buffer
                sys_stdout_original = sys.stdout
                sys.stdout = buffer
                backend_main()
            except Exception as e:
                self.backend_message.emit(f"Erro: {e}")
            finally:
                sys.stdout = sys_stdout_original
                # Envia cada linha do buffer para o slot
                buffer.seek(0)
                for line in buffer:
                    self.backend_message.emit(line.strip())
                self.progress_bar.hide()
                self.btn_generate.setEnabled(True)

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
        elif message.startswith("ARQUIVO_PROCESSADO:"):
            arquivo = message.split(":", 1)[1].strip()
            self.label_arquivo.setText(f"Arquivo: {arquivo}")
        elif message.startswith("ETAPA_CONCLUIDA:"):
            etapa = message.split(":", 1)[1].strip()
            # Atualize seu label de etapas concluídas aqui
        self.btn_search.show_file_dialog()