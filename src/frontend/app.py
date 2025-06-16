import sys
import threading
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import QMetaObject, Qt, Q_ARG
from frontend.components.log_panel import LogPanel
from frontend.components.btn_search import BtnSearch
from frontend.utils.log import QtLogRedirector, log_info
from backend.main import main as backend_main


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excel Processor - Frontend")
        self.resize(600, 400)

        self.log_panel = LogPanel(self.on_generate_database)
        self.log_widget = self.log_panel.get_log_widget()
        self.btn_search = BtnSearch(self.log_widget)

        layout = QVBoxLayout()
        layout.addWidget(self.log_panel)
        layout.addWidget(self.btn_search)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Redireciona prints para o painel de log
        sys.stdout = QtLogRedirector(self.log_widget)

    def write(self, message):
        if message.strip():
            QMetaObject.invokeMethod(
                self.log_widget, "append", Qt.QueuedConnection, Q_ARG(str, message)
            )

    def flush(self):
        pass

    def on_generate_database(self):
        def run_backend():
            log_info(self.log_widget, "Função de geração de data base chamada!")
            backend_main()
            log_info(self.log_widget, "Processamento concluído.")

        # Executa o backend em uma thread separada
        threading.Thread(target=run_backend, daemon=True).start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
