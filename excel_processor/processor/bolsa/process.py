from ..utils.util import (
    get_input_file,
    medir_tempo_execucao,
    criar_codigo_identificacao,
    concat_dataframes,
    get_project_path,
)
import pandas as pd


class BolsaProcessor:
    def __init__(self, input_file: str, output_file: str):
        self.input_file = input_file
        self.output_file = output_file

    def process(self):
        # Load spreadsheets from the original file
        adesao_df = pd.read_excel(self.input_file, sheet_name="Adesão")
        adesao_express_df = pd.read_excel(self.input_file, sheet_name="Adesão_Express")
        seguro_adesao_df = pd.read_excel(self.input_file, sheet_name="Seguro_Adesao")
        seguro_express_df = pd.read_excel(self.input_file, sheet_name="Seguro_Express")
        b_ades_seg_self_df = pd.read_excel(
            self.input_file, sheet_name="B_ADES_SEG_SELF"
        )

        # Create identification codes
        self._create_identification_codes(
            adesao_df,
            adesao_express_df,
            seguro_adesao_df,
            seguro_express_df,
            b_ades_seg_self_df,
        )
        # Filter eligible data
        adesao_df = self._filter_data(adesao_df)
        adesao_express_df = self._filter_data(adesao_express_df)

        self._calculate_sums(
            adesao_df,
            adesao_express_df,
            seguro_adesao_df,
            seguro_express_df,
            b_ades_seg_self_df,
        )

        result_df = self._prepare_final_dataframe(
            adesao_df,
            adesao_express_df,
            seguro_adesao_df,
            seguro_express_df,
            b_ades_seg_self_df,
        )

        self._save_to_excel(result_df)

    def _create_identification_codes(
        self,
        adesao_df,
        adesao_express_df,
        seguro_adesao_df,
        seguro_express_df,
        b_ades_seg_self_df,
    ):
        adesao_df.insert(
            0, "cod_adesao", criar_codigo_identificacao(adesao_df, "loja", "dt_adesÃo")
        )
        adesao_express_df.insert(
            0,
            "cod_adesao_express",
            criar_codigo_identificacao(adesao_express_df, "loja", "data"),
        )
        seguro_adesao_df.insert(
            0,
            "cod_seguro_adesao",
            criar_codigo_identificacao(
                seguro_adesao_df, "origem comercial", "data de cadastro"
            ),
        )
        seguro_express_df.insert(
            0,
            "cod_seguro_express",
            criar_codigo_identificacao(
                seguro_express_df, "origem comercial", "data de cadastro"
            ),
        )
        b_ades_seg_self_df.insert(
            0,
            "cod_b_ades_seg_self",
            criar_codigo_identificacao(b_ades_seg_self_df, "loja", "data"),
        )

    def _filter_data(self, df):
        return df[df["HABIL_NOVO_BOLSA"] == "NÃO"].reset_index(drop=True)

    def _calculate_sums(
        self,
        adesao_df,
        adesao_express_df,
        seguro_adesao_df,
        seguro_express_df,
        b_ades_seg_self_df,
    ):
        sum_express = adesao_express_df.groupby("cod_adesao_express")["qtd"].sum()
        sum_self = b_ades_seg_self_df.groupby("cod_b_ades_seg_self")["qtd"].sum()
        sum_seguro_adesao = seguro_adesao_df.groupby("cod_seguro_adesao")["Total"].sum()
        sum_seguro_express = seguro_express_df.groupby("cod_seguro_express")[
            "Total"
        ].sum()

        adesao_df["express"] = adesao_df["cod_adesao"].map(sum_express).fillna(0)
        adesao_df["SELF"] = adesao_df["cod_adesao"].map(sum_self).fillna(0)
        adesao_express_df["Seguros"] = (
            adesao_express_df["cod_adesao_express"].map(sum_seguro_express).fillna(0)
        )
        adesao_df["Capana"] = (
            adesao_df["qtd_adesÕes"] - adesao_df["express"] - adesao_df["SELF"]
        )
        adesao_df["Adesão"] = adesao_df["cod_adesao"].map(sum_seguro_adesao).fillna(0)

    def _prepare_final_dataframe(
        self,
        adesao_df,
        adesao_express_df,
        seguro_adesao_df,
        seguro_express_df,
        b_ades_seg_self_df,
    ):
        prefixos = {
            "adesao": "AD_",
            "adesao_express": "AE_",
            "seguro_adesao": "SA_",
            "seguro_express": "SE_",
            "b_ades_seg_self": "BASS_",
        }

        adesao_df_renamed = self._rename_columns(
            adesao_df,
            prefixos["adesao"],
            ["cod_adesao", "express", "SELF", "Capana", "Adesão"],
        )
        adesao_express_df_renamed = self._rename_columns(
            adesao_express_df,
            prefixos["adesao_express"],
            ["cod_adesao_express", "Seguros"],
        )
        seguro_adesao_df_renamed = self._rename_columns(
            seguro_adesao_df, prefixos["seguro_adesao"], ["cod_seguro_adesao"]
        )
        seguro_express_df_renamed = self._rename_columns(
            seguro_express_df, prefixos["seguro_express"], ["cod_seguro_express"]
        )
        b_ades_seg_self_df_renamed = self._rename_columns(
            b_ades_seg_self_df, prefixos["b_ades_seg_self"], ["cod_b_ades_seg_self"]
        )

        max_rows = max(
            len(adesao_df_renamed),
            len(adesao_express_df_renamed),
            len(seguro_adesao_df_renamed),
            len(seguro_express_df_renamed),
            len(b_ades_seg_self_df_renamed),
        )

        result_df = pd.DataFrame(index=range(max_rows))

        dfs_to_concat = [
            adesao_df_renamed,
            seguro_adesao_df_renamed,
            adesao_express_df_renamed,
            seguro_express_df_renamed,
            b_ades_seg_self_df_renamed,
        ]

        result_df = concat_dataframes(dfs_to_concat, max_rows)
        result_df = result_df.loc[:, ~result_df.columns.duplicated()]

        return result_df

    def _rename_columns(self, df, prefix, preserve_columns):
        df_renamed = df.copy()
        for col in df_renamed.columns:
            if col not in preserve_columns:
                df_renamed = df_renamed.rename(columns={col: f"{prefix}{col}"})
        return df_renamed

    def _save_to_excel(self, result_df):
        with pd.ExcelWriter(self.output_file, engine="openpyxl") as writer:
            result_df.to_excel(writer, sheet_name="Bolsa", index=False)
            self._adjust_column_width(writer, result_df)

    def _adjust_column_width(self, writer, df):
        worksheet = writer.sheets["Bolsa"]
        for idx, col in enumerate(df.columns):
            max_len = max(df[col].astype(str).map(len).max(), len(str(col))) + 2
            worksheet.column_dimensions[
                worksheet.cell(row=1, column=idx + 1).column_letter
            ].width = max_len


@medir_tempo_execucao
def process_bolsa():
    input_file = get_input_file()
    output_file = get_project_path("output", "Bolsa_Data_base.xlsx")

    bolsa_processor = BolsaProcessor(str(input_file), str(output_file))
    bolsa_processor.process()
    print(f"\nArquivo '{output_file.stem}' criado com sucesso!")
