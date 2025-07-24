from ..utils.util import get_input_file, get_project_path, medir_tempo_execucao, criar_codigo_identificacao, concat_dataframes
import pandas as pd
import os

class DihPayProcessor:
    def __init__(self, input_file: str, output_file: str):
        self.input_file = input_file
        self.output_file = output_file

    def process(self):
        # Load spreadsheets from the original file
        protecao_premiada_df = pd.read_excel(self.input_file, sheet_name="Proteção Premiada")
        base_protecao_df = pd.read_excel(self.input_file, sheet_name="BaseProtecao_Premiada")

        # Create identification codes
        protecao_premiada_df.insert(0, "cod_protecao_premiada", criar_codigo_identificacao(protecao_premiada_df, "loja", "data"))
        base_protecao_df.insert(0, "cod_base_protecao_premiada", criar_codigo_identificacao(base_protecao_df, "origem comercial", "data de cadastro"))

        # Filter eligible data
        protecao_premiada_df = protecao_premiada_df[protecao_premiada_df["elegível"] == "S"].reset_index(drop=True)

        # Calculate sums to map values
        sum_seguros = base_protecao_df.groupby("cod_base_protecao_premiada")["Total"].sum()

        # Add calculated column
        protecao_premiada_df["Seguros"] = protecao_premiada_df["cod_protecao_premiada"].map(sum_seguros).fillna(0)

        # Rename columns to avoid conflicts
        self._rename_columns(protecao_premiada_df, base_protecao_df)

        # Create a base dataframe with the maximum number of rows
        max_rows = max(len(base_protecao_df), len(protecao_premiada_df))
        result_df = pd.DataFrame(index=range(max_rows))

        # Concatenate renamed dataframes
        result_df = concat_dataframes([protecao_premiada_df, base_protecao_df], max_rows)

        # Remove duplicate columns if any
        result_df = result_df.loc[:, ~result_df.columns.duplicated()]

        # Save the result to a new Excel file
        self._save_to_excel(result_df)

    def _rename_columns(self, protecao_df: pd.DataFrame, base_df: pd.DataFrame):
        prefixos = {
            'protecao_premiada': 'PP_',
            'base_protecao': 'BP_'
        }

        # Rename columns for protecao_df
        for col in protecao_df.columns:
            if col not in ['cod_protecao_premiada', 'Seguros']:
                protecao_df.rename(columns={col: f"{prefixos['protecao_premiada']}{col}"}, inplace=True)

        # Rename columns for base_df
        for col in base_df.columns:
            if col != 'cod_base_protecao_premiada':
                base_df.rename(columns={col: f"{prefixos['base_protecao']}{col}"}, inplace=True)

    def _save_to_excel(self, df: pd.DataFrame):
        with pd.ExcelWriter(self.output_file) as writer:
            df.to_excel(writer, sheet_name="DIH Pay", index=False)

@medir_tempo_execucao
def process_dih_pay():    
    input_file = get_input_file()
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "Dih_Pay_Data_base.xlsx")
    processor = DihPayProcessor(str(input_file), str(output_file))
    processor.process()
    print(f"\nArquivo '{os.path.basename(output_file)}' criado com sucesso!")