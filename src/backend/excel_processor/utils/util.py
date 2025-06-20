import datetime
import sys
import threading
import time
import pandas as pd
from pathlib import Path
from glob import glob


def medir_tempo_execucao_total(funcao):
    """
    Decorador para medir o tempo de execução de uma função.
    """
    def wrapper(*args, **kwargs):
        tempo_inicial = time.time()
        resultado = funcao(*args, **kwargs)        
        tempo_total = time.time() - tempo_inicial        
        minutos, segundos = divmod(tempo_total, 60)                
        print(f"Tempo total de processamento em {int(minutos)} minutos e {int(segundos)} segundos. ")
        return resultado
    return wrapper

def criar_codigo_identificacao(df, coluna_loja_origem, coluna_data_origem):
    """
    Cria um código de identifstdicação a partir das 3 primeiras letras da loja/origem + data formatada.
    A data é convertida para o formato serializado do Excel.
    """
    if coluna_loja_origem not in df.columns or coluna_data_origem not in df.columns:
        return pd.Series([None] * len(df))
    
    prefixo = df[coluna_loja_origem].astype(str).str[:3]

    def converter_data(date):
        """Tenta converter a data para formato serial do Excel ou outro formato válido."""
        try:
            excel_start_date = datetime.datetime(1899, 12, 30)
            return str((pd.to_datetime(date) - excel_start_date).days)
        except:
            try:
                return pd.to_datetime(date, format='%d/%m/%Y').strftime('%Y%m%d')
            except:
                return str(date)
    
    data = df[coluna_data_origem].apply(converter_data)
    
    return prefixo + data

def concat_dataframes(dataframes, max_rows):
    """
    Concatena múltiplos dataframes horizontalmente com colunas separadoras entre eles.
    
    Args:
        dataframes (list): Lista de dataframes para concatenar
        max_rows (int): Número máximo de linhas para cada dataframe
        
    Returns:
        DataFrame: Dataframe concatenado com separadores
    """
    result_df = pd.DataFrame(index=range(max_rows))
    
    for i, df in enumerate(dataframes):
        # Garantir que o dataframe tenha o mesmo número de linhas
        temp_df = df.reindex(range(max_rows))
        
        # Concatenar ao resultado
        result_df = pd.concat([result_df, temp_df], axis=1)
        
        # Adicionar coluna separadora vazia após cada dataframe (exceto o último)
        # if i < len(dataframes) - 1:
        #     separator_name = " "* (i + 1)
        #     result_df[separator_name] = ""
    
    return result_df

def medir_tempo_execucao(funcao):
    """
    Decorador que mostra tempo decorrido durante a execução da função.
    (Sem spinner para evitar problemas com threads em GUI)
    """
    def wrapper(*args, **kwargs):
        tempo_inicial = time.time()
        resultado = funcao(*args, **kwargs)
        tempo_total = time.time() - tempo_inicial
        minutos, segundos = divmod(tempo_total, 60)
        print(f"{funcao.__name__} finalizado em {int(minutos)}:{int(segundos)}.")
        return resultado
    return wrapper

def get_project_path(*subpaths):
    """
    Retorna o caminho absoluto a partir da raiz do projeto, juntando subdiretórios/arquivos.
    Exemplo: get_project_path("input", "Quadro Seguros Diário.xlsx")
    """
    base_dir = Path(__file__).parent.parent
    return base_dir.joinpath(*subpaths)

def get_input_file(pattern="Quadro Seguros Diário*"):
    input_dir = get_project_path("input")   
    if not input_dir.exists():
        raise FileNotFoundError(f"A pasta de entrada '{input_dir}' não existe.") 
    
    arquivos = list(Path(input_dir).glob(f"{pattern}.xlsx"))        
    if not arquivos:
        raise FileNotFoundError(f"Nenhum arquivo encontrado que comece com '{pattern}' na pasta input.")
    return arquivos[0]

@medir_tempo_execucao
def filtro():
    input_file = r"output\Consolidado_data_base_C&A.xlsx"
    output_file = r"output\Consolidado_data_base_C&A_filtrado.xlsx"

    bolsa_df = pd.read_excel(input_file, sheet_name="Bolsa")
    novo_bolsa_df = pd.read_excel(input_file, sheet_name="Novo Bolsa")
    parcela_df = pd.read_excel(input_file, sheet_name="Parcela")
    dih_play_df = pd.read_excel(input_file, sheet_name="DIH Pay")

    colunas_bolsa = [
        "AD_loja",
        "AD_dt_adesÃo",
        "Capana",
        "Adesão",
        "AE_loja",
        "AE_data",
        "AE_qtd",
        "Seguros",
        "BASS_loja",
        "BASS_data",
        "BASS_qtd",
        "BASS_seguros",
    ]
    colunas_novo_bolsa = [
        "AD_loja",
        "AD_dt_adesÃo",
        "AD_Capana",
        "seguro_adesao",
        "AE_loja",
        "AE_data",
        "AE_qtd",
        "AE_seguro_express",
    ]
    colunas_parcela = [
        "PP_loja",
        "PP_data",
        "PDV",
        "adesões_PDV_parcela_premiada",
        "PE_loja",
        "PE_data",
        "PE_venda",
        "PE_seguro",
    ]
    colunas_dih_play = ["PP_loja", "PP_data", "PP_qtd", "Seguros"]

    bolsa_df = bolsa_df[colunas_bolsa]
    novo_bolsa_df = novo_bolsa_df[colunas_novo_bolsa]
    parcela_df = parcela_df[colunas_parcela]
    dih_play_df = dih_play_df[colunas_dih_play]

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        bolsa_df.to_excel(writer, sheet_name="Bolsa", index=False)
        novo_bolsa_df.to_excel(writer, sheet_name="Novo Bolsa", index=False)
        parcela_df.to_excel(writer, sheet_name="Parcela", index=False)
        dih_play_df.to_excel(writer, sheet_name="DIH Pay", index=False)

    print(f"Arquivo '{output_file}' criado com sucesso!")