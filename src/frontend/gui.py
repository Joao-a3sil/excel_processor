from dearpygui.core import *
from dearpygui.simple import *

def setup_gui():
    with window("Main Window"):
        set_window_size("Main Window", 600, 400)
        add_text("Welcome to the Excel Processor!")
        add_button("Process Excel", callback=process_excel)
        add_button("Exit", callback=exit_program)

def process_excel():
    # Here you would call the backend processing functions
    print("Processing Excel file...")

def exit_program():
    stop_dearpygui()

if __name__ == "__main__":
    setup_gui()
    start_dearpygui()