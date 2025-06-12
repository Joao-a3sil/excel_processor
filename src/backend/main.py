from backend.excel_processor.processor.utils.util import get_input_file, medir_tempo_execucao_total
from backend.excel_processor.processor.bolsa.process import process_bolsa
from backend.excel_processor.processor.novo_bolsa.process import process_novo_bolsa
from backend.excel_processor.processor.parcela.process import process_parcela
from backend.excel_processor.processor.dih_pay.process import process_dih_pay
from backend.excel_processor.processor.excel_consolidator.process import gerar_data_base

@medir_tempo_execucao_total
def main():    
    arquivo_processado = get_input_file()
    print(f"Processando arquivo: {arquivo_processado.stem}")
    process_dih_pay()
    # process_bolsa()
    # process_novo_bolsa()
    # process_parcela()
    # gerar_data_base()    

if __name__ == "__main__":
    main()