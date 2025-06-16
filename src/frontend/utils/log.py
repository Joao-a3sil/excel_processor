from PySide6.QtWidgets import QTextEdit

class LogWidget(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)

    def add_log_text(self, message):
        self.append(message)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

def log_info(log_widget, message):
    log_widget.add_log_text(message)

class QtLogRedirector:
    def __init__(self, log_widget):
        self.log_widget = log_widget

    def write(self, message):
        if message.strip():
            self.log_widget.add_log_text(message)

    def flush(self):
        pass