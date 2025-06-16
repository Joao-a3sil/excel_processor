from backend.excel_processor.processor.utils.util import get_input_file, medir_tempo_execucao_total
from backend.excel_processor.processor.bolsa.process import process_bolsa
from backend.excel_processor.processor.novo_bolsa.process import process_novo_bolsa
from backend.excel_processor.processor.parcela.process import process_parcela
from backend.excel_processor.processor.dih_pay.process import process_dih_pay
from backend.excel_processor.processor.excel_consolidator.process import gerar_data_base
import time

@medir_tempo_execucao_total
def main():    
    arquivo_processado = get_input_file()
    # print(f"Processando arquivo: {arquivo_processado.stem}")
    print(f"ARQUIVO_PROCESSADO: {arquivo_processado.name}")

    etapas = [
        ("DIH Pay", process_dih_pay),
        ("Bolsa", process_bolsa),
        # ("Novo Bolsa", process_novo_bolsa),
        # ("Parcela", process_parcela),
        # ("Consolidação", gerar_data_base)
    ]

    for nome, func in etapas:
        print(f"ETAPA_STATUS: {nome}")
        start = time.time()
        func()
        elapsed = time.time() - start
        minutos, segundos = divmod(int(elapsed), 60)
        print(f"Etapa {nome} concluída em {minutos}m {segundos}s.")
        print(f"ETAPA_CONCLUIDA: {nome}")

if __name__ == "__main__":
    main()