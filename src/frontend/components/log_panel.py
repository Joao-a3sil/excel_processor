from dearpygui.dearpygui import add_child_window, window, add_text, add_button
from frontend.utils.log import LOG_WIDGET

def show_main_window():
    with window(label="Consolidador de Excel", width=600, height=400):
        add_text("Bem-vindo ao consolidador de Excel!")
        add_button(label="Gerar Data Base", callback=on_generate_database)
        add_button(label="Sair", callback=lambda: stop_dearpygui())
        create_log_panel()

def create_log_panel():
    add_child_window(tag=LOG_WIDGET, height=100)
