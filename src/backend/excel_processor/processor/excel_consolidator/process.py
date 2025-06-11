from ..utils.util import get_project_path, medir_tempo_execucao
import pandas as pd

class excel_consolidator:
    def __init__(self, output_file, data_base_file):
        self.output_file = output_file
        self.data_base_file = data_base_file

    def consolidar(self):
        """
        Consolidates multiple dataframes into a single output file.
        Reads data from various sources and saves the consolidated data.
        """
        input_bolsa = get_project_path("output", "Bolsa_Data_base.xlsx")
        input_novo_bolsa = get_project_path("output", "Novo_Bolsa_Data_base.xlsx")
        input_parcela = get_project_path("output", "Parcela_Data_base.xlsx")
        input_dih_play = get_project_path("output", "Dih_Pay_Data_base.xlsx")

        bolsa_df = pd.read_excel(input_bolsa, sheet_name="Bolsa")
        novo_bolsa_df = pd.read_excel(input_novo_bolsa, sheet_name="Novo Bolsa")
        paracela_df = pd.read_excel(input_parcela, sheet_name="Parcela")
        dih_play_df = pd.read_excel(input_dih_play, sheet_name="DIH Pay")
        # Save the consolidated dataframe to an Excel file
        with pd.ExcelWriter(self.output_file, engine='openpyxl') as writer:
            bolsa_df.to_excel(writer, sheet_name="Bolsa", index=False)
            novo_bolsa_df.to_excel(writer, sheet_name="Novo Bolsa", index=False)
            paracela_df.to_excel(writer, sheet_name="Parcela", index=False)
            dih_play_df.to_excel(writer, sheet_name="DIH Pay", index=False)

        print(f"\nArquivo '{self.output_file}' criado com sucesso!")

    def organizar_colunas(self):
        input_file = self.output_file

        bolsa_df = pd.read_excel(input_file, sheet_name="Bolsa")
        novo_bolsa_df = pd.read_excel(input_file, sheet_name="Novo Bolsa")
        parcela_df = pd.read_excel(input_file, sheet_name="Parcela")
        dih_play_df = pd.read_excel(input_file, sheet_name="DIH Pay")

        colunas_bolsa = [
            "AD_loja", "AD_dt_adesÃo", "Capana", "Adesão", "AE_loja", "AE_data", "AE_qtd", "Seguros",
            "BASS_loja", "BASS_data", "BASS_qtd", "BASS_seguros"
        ]
        colunas_novo_bolsa = [
            "AD_loja", "AD_dt_adesÃo", "AD_Capana", "seguro_adesao", "AE_loja", "AE_data", "AE_qtd", "AE_seguro_express"
        ]
        colunas_parcela = [
            "PP_loja", "PP_data", "PDV", "adesões_PDV_parcela_premiada", "PE_loja", "PE_data", "PE_venda", "PE_seguro"
        ]
        colunas_dih_play = ["PP_loja", "PP_data", "PP_qtd", "Seguros"]

        bolsa_df = bolsa_df[colunas_bolsa]
        novo_bolsa_df = novo_bolsa_df[colunas_novo_bolsa]
        parcela_df = parcela_df[colunas_parcela]
        dih_play_df = dih_play_df[colunas_dih_play]

        with pd.ExcelWriter(self.data_base_file, engine="openpyxl") as writer:
            bolsa_df.to_excel(writer, sheet_name="Bolsa", index=False)
            novo_bolsa_df.to_excel(writer, sheet_name="Novo Bolsa", index=False)
            parcela_df.to_excel(writer, sheet_name="Parcela", index=False)
            dih_play_df.to_excel(writer, sheet_name="DIH Pay", index=False)

        print(f"\nArquivo '{self.data_base_file.stem()}' criado com sucesso!")

@medir_tempo_execucao
def gerar_data_base():
       
    output_file = get_project_path("output", "Consolidado_data_base_C&A_completo.xlsx")
    data_base_file = get_project_path("output", "Consolidado_data_base_C&A.xlsx")
    
    process_cea = excel_consolidator(str(output_file), str(data_base_file))
    process_cea.consolidar()
    process_cea.organizar_colunas()
