from dearpygui.dearpygui import *

def on_generate_database(sender, app_data, user_data):
    log_info("Função de geração de data base chamada!")

def main():
    create_context()
    create_viewport(title="Excel Processor - Frontend", width=600, height=400)

    with window(label="Consolidador de Excel", width=600, height=400):
        add_text("Bem-vindo ao consolidador de Excel!")
        add_button(label="Gerar Data Base", callback=on_generate_database)
        add_button(label="Sair", callback=lambda: stop_dearpygui())

    setup_dearpygui()
    show_viewport()
    start_dearpygui()
    destroy_context()

if __name__ == "__main__":
    main()