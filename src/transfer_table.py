import pandas as pd
import glob
import re  

def get_xlsx():
    all_files = glob.glob("CES_ownership*.xlsx")  
    if not all_files:
        print("Nenhum arquivo .xlsx com o prefixo 'CES_ownership' encontrado.")
        return None

    print("Escolha o arquivo .xlsx desejado:")
    for i, file in enumerate(all_files, start=1):
        print(f"{i}. {file}")

    while True:
        try:
            escolha = int(input("Digite o número do arquivo: "))
            if 1 <= escolha <= len(all_files):
                return all_files[escolha - 1]
            else:
                print("Número inválido! Tente novamente.")
        except ValueError:
            print("Entrada inválida! Digite um número válido.")


def format_cnpj(cnpj):
    
    return re.sub(r'\D', '', cnpj)

def format_xlsx(file, cnpj):
    if file is None:
        return None

    # Formatar o CNPJ informado pelo usuário
    cnpj_formatado = format_cnpj(cnpj)

    source_df = pd.read_excel(file)

    df_filtrado = source_df[
        source_df["owner_list"].apply(lambda x: cnpj_formatado in str(x).split(","))
    ]

    df_resultado = df_filtrado[["n_ps", "wgs_lat", "wgs_lon"]]
    
    df_resultado["n_ps"] = pd.to_numeric(df_resultado["n_ps"], errors="coerce").fillna(0).astype(int)

    return df_resultado


# Função principal
def main():
    arquivo = get_xlsx()
    if arquivo is None:
        return

    cnpj_filtro = input("Digite o CNPJ para filtrar: ")

    df_filtrado = format_xlsx(arquivo, cnpj_filtro)

    if df_filtrado is not None and not df_filtrado.empty:
        nome_saida = f"planilha_filtrada_{arquivo}"
        df_filtrado.to_excel(nome_saida, index=False)
        print(f"Planilha filtrada salva com sucesso em {nome_saida}!")
    else:
        print("Nenhum dado encontrado para o CNPJ especificado.")


# Início do programa
if __name__ == "__main__":
    main()
