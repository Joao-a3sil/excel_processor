from pathlib import Path
import shutil
from dearpygui.dearpygui import add_file_dialog, show_item, hide_item

from frontend.utils.log import log_info

INPUT_DIR = str(Path(__file__).resolve().parent.parent / "backend" / "excel_processor" / "input")

def on_file_selected(sender, app_data):
    selected_file = app_data['file_path_name']
    if selected_file:
        dest = Path(INPUT_DIR) / Path(selected_file).name
        shutil.copy(selected_file, dest)
        log_info(f"Arquivo '{Path(selected_file).name}' copiado para a pasta input.")
    hide_item("file_dialog_id")

def show_file_dialog(sender=None, app_data=None, user_data=None):
    show_item("file_dialog_id")

