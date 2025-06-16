from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from frontend.utils.log import LogWidget

class LogPanel(QWidget):
    def __init__(self, on_generate_database, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        self.label = QLabel("Bem-vindo ao consolidador de Excel!")
        self.layout.addWidget(self.label)

        self.btn_generate = QPushButton("Gerar Data Base")
        self.btn_generate.clicked.connect(on_generate_database)
        self.layout.addWidget(self.btn_generate)

        self.btn_exit = QPushButton("Sair")
        self.layout.addWidget(self.btn_exit)

        self.log_widget = LogWidget()
        self.layout.addWidget(self.log_widget)

    def get_log_widget(self):
        return self.log_widget