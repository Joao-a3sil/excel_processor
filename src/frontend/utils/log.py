from dearpygui.dearpygui import add_text, set_y_scroll, get_y_scroll_max

LOG_WIDGET = "log_panel"

def add_log_text(message, parent=LOG_WIDGET):
    add_text(message, parent=parent)
    set_y_scroll(parent, get_y_scroll_max(parent))
    

def log_info(message):
    add_log_text(message)

class DpgLogRedirector:
    def write(self, message):
        if message.strip():
            log_info(message)
    def flush(self):
        pass

