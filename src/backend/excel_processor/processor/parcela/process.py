from backend.excel_processor.processor.utils.util import (
    get_input_file,
    get_project_path,
    medir_tempo_execucao,
    criar_codigo_identificacao,
    concat_dataframes,
)
import pandas as pd

class ProcessParcela:
    def __init__(self, input_file: str, output_file: str):
        self.input_file = input_file
        self.output_file = output_file

    def process(self):
        parcela_premiada_df = pd.read_excel(
            self.input_file, sheet_name="Parcela Premiada"
        )
        seguro_parcela_df = pd.read_excel(self.input_file, sheet_name="Seguro_Parcela")
        parcela_express_df = pd.read_excel(
            self.input_file, sheet_name="Parcela-Express"
        )

        self._create_identification_codes(
            parcela_premiada_df, seguro_parcela_df, parcela_express_df
        )
        parcela_df = self._filter_eligible_records(parcela_premiada_df)

        self._add_calculated_columns(parcela_df, parcela_express_df)
        result_df = self._rename_columns(
            parcela_df, seguro_parcela_df, parcela_express_df
        )

        self._save_to_excel(result_df)

    def _create_identification_codes(
        self, parcela_premiada_df, seguro_parcela_df, parcela_express_df
    ):
        parcela_premiada_df.insert(
            0,
            "cod_parcela_premiada",
            criar_codigo_identificacao(parcela_premiada_df, "loja", "data"),
        )
        seguro_parcela_df.insert(
            0,
            "cod_seguro_parcela",
            criar_codigo_identificacao(seguro_parcela_df, "loja", "data"),
        )
        parcela_express_df.insert(
            0,
            "cod_parcela_express",
            criar_codigo_identificacao(parcela_express_df, "loja", "data"),
        )

    def _filter_eligible_records(self, parcela_premiada_df):
        return (
            parcela_premiada_df[parcela_premiada_df["elegível"] == "S"]
            .copy()
            .reset_index(drop=True)
        )

    def _add_calculated_columns(self, parcela_df, parcela_express_df):
        express_sum = parcela_express_df.groupby("cod_parcela_express")["venda"].sum()
        parcela_df["express_parcela_premiada"] = (
            parcela_df["cod_parcela_premiada"].map(express_sum).fillna(0)
        )
        parcela_df["PDV"] = parcela_df["qtd"] - parcela_df["express_parcela_premiada"]
        parcela_df["adesões_PDV_parcela_premiada"] = 0

    def _rename_columns(self, parcela_df, seguro_parcela_df, parcela_express_df):
        prefixos = {
            "parcela_premiada": "PP_",
            "seguro_parcela": "SP_",
            "parcela_express": "PE_",
        }

        parcela_df_renamed = self._rename_dataframe_columns(
            parcela_df,
            prefixos["parcela_premiada"],
            [
                "cod_parcela_premiada",
                "express_parcela_premiada",
                "PDV",
                "adesões_PDV_parcela_premiada",
            ],
        )
        seguro_parcela_df_renamed = self._rename_dataframe_columns(
            seguro_parcela_df, prefixos["seguro_parcela"], ["cod_seguro_parcela"]
        )
        parcela_express_df_renamed = self._rename_dataframe_columns(
            parcela_express_df, prefixos["parcela_express"], ["cod_parcela_express"]
        )

        max_rows = max(
            len(parcela_df_renamed),
            len(seguro_parcela_df_renamed),
            len(parcela_express_df_renamed),
        )
        # result_df = pd.DataFrame(index=range(max_rows))
        result_df = concat_dataframes(
            [parcela_df_renamed, seguro_parcela_df_renamed, parcela_express_df_renamed],
            max_rows,
        )
        result_df = self._post_concatenation_calculations(result_df, parcela_express_df, prefixos) 

        return result_df

    def _post_concatenation_calculations(self, result_df, parcela_express_df, prefixos):
    # Calcular os mapeamentos e valores após a concatenação
    # Mapear os valores de express_sum para colunas específicas com segurança
        if (
            "cod_seguro_parcela" in result_df.columns
            and "cod_parcela_express" in result_df.columns
        ):
            express_sum_seguro = parcela_express_df.groupby("cod_parcela_express")[
                "seguro"
            ].sum()
            result_df.insert(
                12,
                "express_seguro_parcela",
                result_df["cod_seguro_parcela"].map(express_sum_seguro).fillna(0),
            )

            if f"{prefixos['seguro_parcela']}Total" in result_df.columns:
                result_df.insert(
                    13,
                    "adesões_PDV_seguro_parcela",
                    result_df[f"{prefixos['seguro_parcela']}Total"]
                    - result_df["express_seguro_parcela"],
                )

                # Calcular somas de adesões PDV
                if "cod_parcela_premiada" in result_df.columns:
                    # Criar um dataframe temporário para o agrupamento
                    temp_df = result_df[
                        ["cod_seguro_parcela", "adesões_PDV_seguro_parcela"]
                    ].dropna()
                    adesoes_pdv_sum = temp_df.groupby("cod_seguro_parcela")[
                        "adesões_PDV_seguro_parcela"
                    ].sum()
                    result_df["adesões_PDV_parcela_premiada"] = (
                        result_df["cod_parcela_premiada"].map(adesoes_pdv_sum).fillna(0)
                )
        return result_df

    def _rename_dataframe_columns(self, df, prefix, columns_to_preserve):
        df_renamed = df.copy()
        for col in df_renamed.columns:
            if col not in columns_to_preserve:
                df_renamed = df_renamed.rename(columns={col: f"{prefix}{col}"})
        return df_renamed

    def _save_to_excel(self, result_df):
        with pd.ExcelWriter(self.output_file, engine="openpyxl") as writer:
            result_df.to_excel(writer, sheet_name="Parcela", index=False)
            self._adjust_column_widths(writer, result_df)

    def _adjust_column_widths(self, writer, result_df):
        worksheet = writer.sheets["Parcela"]
        for idx, col in enumerate(result_df.columns):
            max_len = max(result_df[col].astype(str).map(len).max(), len(str(col))) + 2
            worksheet.column_dimensions[
                worksheet.cell(row=1, column=idx + 1).column_letter
            ].width = max_len


@medir_tempo_execucao
def process_parcela():
    input_file = get_input_file()
    output_file = get_project_path("output", "Parcela_Data_base.xlsx")
    processor = ProcessParcela(str(input_file), str(output_file))
    processor.process()
    print(f"\nArquivo '{output_file.stem}' criado com sucesso!")


