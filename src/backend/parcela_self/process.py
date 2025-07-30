from ..utils.util import (
    get_input_file,
    get_project_path,
    medir_tempo_execucao,
)
import pandas as pd
import os


class ParcelaSelfProcessor:
    def __init__(self, input_file: str, output_file: str):
        self.input_file = input_file
        self.output_file = output_file

    def process(self):
        # Load spreadsheets from the original file
        parcela_self_df = pd.read_excel(self.input_file, sheet_name="parcela_self")
        
        parcela_self_df = parcela_self_df[["loja", "data", "venda", "seguro", "habil"]]

        # Save the result to a new Excel file
        self._save_to_excel(parcela_self_df)

    def _save_to_excel(self, df):
        with pd.ExcelWriter(self.output_file) as writer:
            df.to_excel(writer, sheet_name="Parcela Self", index=False)


@medir_tempo_execucao
def process_parcela_self():
    input_file = get_input_file()

    output_file = get_project_path("output", "Parcela_Self_Data_base.xlsx")
    processor = ParcelaSelfProcessor(str(input_file), str(output_file))
    processor.process()
    print(f"\nArquivo '{os.path.basename(output_file)}' criado com sucesso!")
