from excel_processor.processor.utils.util import get_input_file, get_project_path, medir_tempo_execucao, criar_codigo_identificacao, concat_dataframes

import pandas as pd


class NovoBolsaProcessor:
    def __init__(self, input_file: str, output_file: str):
        self.input_file = input_file
        self.output_file = output_file

    def process(self):
        adesao_df = pd.read_excel(self.input_file, sheet_name="Adesão")
        adesao_express_df = pd.read_excel(self.input_file, sheet_name="Adesão_Express")
        bolsa_novo_df = pd.read_excel(self.input_file, sheet_name="Bolsa_Novo")
        bolsa_novo_pdv_df = pd.read_excel(self.input_file, sheet_name="Bolsa_Novo_PDV")

        self._create_identification_codes(
            adesao_df, adesao_express_df, bolsa_novo_df, bolsa_novo_pdv_df
        )
        self._filter_data(adesao_df, adesao_express_df)
        result_df = self._concatenate_dataframes(
            adesao_df, adesao_express_df, bolsa_novo_df, bolsa_novo_pdv_df
        )
        result_df = result_df.loc[:, ~result_df.columns.duplicated()]
        self._save_to_excel(result_df)

    def _create_identification_codes(
        self, adesao_df, adesao_express_df, bolsa_novo_df, bolsa_novo_pdv_df
    ):
        adesao_df.insert(
            0, "cod_adesao", criar_codigo_identificacao(adesao_df, "loja", "dt_adesÃo")
        )
        adesao_express_df.insert(
            0,
            "cod_adesao_express",
            criar_codigo_identificacao(adesao_express_df, "loja", "data"),
        )
        bolsa_novo_df.insert(
            0,
            "cod_bolsa_novo",
            criar_codigo_identificacao(
                bolsa_novo_df, "origem comercial", "data de cadastro"
            ),
        )
        bolsa_novo_pdv_df.insert(
            0,
            "cod_bolsa_nova_pdv",
            criar_codigo_identificacao(
                bolsa_novo_pdv_df, "origem comercial", "data de cadastro"
            ),
        )

    def _filter_data(self, adesao_df, adesao_express_df):
        adesao_df.drop(
            adesao_df[adesao_df["HABIL_NOVO_BOLSA"] != "SIM"].index, inplace=True
        )
        adesao_df.reset_index(drop=True, inplace=True)  #

        adesao_express_df.drop(
            adesao_express_df[adesao_express_df["HABIL_NOVO_BOLSA"] != "SIM"].index,
            inplace=True,
        )
        adesao_express_df.reset_index(drop=True, inplace=True)

    def _concatenate_dataframes(
        self, adesao_df, adesao_express_df, bolsa_novo_df, bolsa_novo_pdv_df
    ):
        sum_adesao = bolsa_novo_df.groupby("cod_bolsa_novo")["Total"].sum()
        sum_adesao_express = bolsa_novo_pdv_df.groupby("cod_bolsa_nova_pdv")[
            "Total"
        ].sum()
        sum_express = adesao_express_df.groupby("cod_adesao_express")["qtd"].sum()

        adesao_df["express"] = adesao_df["cod_adesao"].map(sum_express).fillna(0)
        adesao_df["Capana"] = adesao_df["qtd_adesÕes"] - adesao_df["express"]
        adesao_df["seguro_adesao"] = adesao_df["cod_adesao"].map(sum_adesao).fillna(0)
        adesao_express_df["seguro_express"] = (
            adesao_express_df["cod_adesao_express"].map(sum_adesao_express).fillna(0)
        )

        prefixos = {
            "adesao": "AD_",
            "adesao_express": "AE_",
            "bolsa_novo": "BN_",
            "bolsa_novo_pdv": "BP_",
        }

        adesao_df_renamed = self._rename_columns(
            adesao_df,
            prefixos["adesao"],
            ["cod_adesao", "seguro_adesao", "seguro_express", "cod_adesao_express"],
        )
        adesao_express_df_renamed = self._rename_columns(
            adesao_express_df, prefixos["adesao_express"], ["cod_adesao_express"]
        )
        bolsa_novo_df_renamed = self._rename_columns(
            bolsa_novo_df, prefixos["bolsa_novo"], ["cod_bolsa_novo"]
        )
        bolsa_novo_pdv_df_renamed = self._rename_columns(
            bolsa_novo_pdv_df, prefixos["bolsa_novo_pdv"], ["cod_bolsa_nova_pdv"]
        )

        max_rows = max(
            len(adesao_df_renamed),
            len(adesao_express_df_renamed),
            len(bolsa_novo_df_renamed),
            len(bolsa_novo_pdv_df_renamed),
        )
        return concat_dataframes(
            [
                adesao_df_renamed,
                bolsa_novo_df_renamed,
                adesao_express_df_renamed,
                bolsa_novo_pdv_df_renamed,
            ],
            max_rows,
        )

    def _rename_columns(self, df, prefix, preserve_columns):
        df_renamed = df.copy()
        for col in df_renamed.columns:
            if col not in preserve_columns:
                df_renamed.rename(columns={col: f"{prefix}{col}"}, inplace=True)
        return df_renamed

    def _save_to_excel(self, result_df):
        with pd.ExcelWriter(self.output_file, engine="openpyxl") as writer:
            result_df.to_excel(writer, sheet_name="Novo Bolsa", index=False)
            worksheet = writer.sheets["Novo Bolsa"]
            for idx, col in enumerate(result_df.columns):
                max_len = (
                    max(result_df[col].astype(str).map(len).max(), len(str(col))) + 2
                )
                worksheet.column_dimensions[
                    worksheet.cell(row=1, column=idx + 1).column_letter
                ].width = max_len


@medir_tempo_execucao
def process_novo_bolsa():
    input_file = get_input_file()
    output_file = get_project_path("output", "Novo_Bolsa_Data_base.xlsx")
    
    processor = NovoBolsaProcessor(str(input_file), str(output_file))
    processor.process()
    print(f"\nArquivo '{output_file.stem}' criado com sucesso!")
