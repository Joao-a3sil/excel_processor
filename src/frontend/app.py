from dearpygui.dearpygui import *
import sys
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parent.parent))

from backend.main import main as backend_main
from frontend.components.log_panel import create_log_panel
from frontend.utils.log import log_info, DpgLogRedirector
from frontend.components.btn_search import on_file_selected, show_file_dialog


def on_generate_database(sender, app_data, user_data):
    sys.stdout = DpgLogRedirector()  # Redireciona prints para o painel de log
    log_info("Função de geração de data base chamada!")
    backend_main()
    sys.stdout = sys.__stdout__  # (Opcional) Restaura o stdout padrão após execução


def main():
    create_context()
    create_viewport(title="Excel Processor - Frontend", width=600, height=400)
    add_file_dialog(
    tag="file_dialog_id",
    callback=on_file_selected,
    show=False,
    width=500,
    height=400
)
    with window(label="Consolidador de Excel", width=600, height=400):
        add_text("Bem-vindo ao consolidador de Excel!")
        add_button(label="Adicionar arquivo", callback=show_file_dialog)
        add_button(label="Gerar Data Base", callback=on_generate_database)
        add_button(label="Sair", callback=lambda: stop_dearpygui())
        create_log_panel()

    setup_dearpygui()
    show_viewport()
    start_dearpygui()
    destroy_context()


if __name__ == "__main__":
    main()