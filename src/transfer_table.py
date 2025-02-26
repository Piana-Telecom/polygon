import pandas as pd
import glob
import re  
import os 

OUTPUT_FOLDER = "FILTRADA_output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def get_xlsx():
    all_files = glob.glob(os.path.join("OWNERSHIP_output", "CES_ownership*.xlsx"))
    if not all_files:
        print("Nenhum arquivo .xlsx com o prefixo 'CES_ownership' encontrado na pasta OWNERSHIP_output.")
        return None

    print("Escolha o arquivo .xlsx desejado:")
    for i, file in enumerate(all_files, start=1):
        print(f"{i}. {os.path.basename(file)}")

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

    cnpj_formatado = format_cnpj(cnpj)

    source_df = pd.read_excel(file)

    df_filtrado = source_df[
        source_df["owner_list"].apply(lambda x: cnpj_formatado in str(x).split(","))
    ]

    df_resultado = df_filtrado[["n_ps", "wgs_lat", "wgs_lon"]]

    df_resultado["n_ps"] = pd.to_numeric(df_resultado["n_ps"], errors="coerce").fillna(0).astype(int)

    return df_resultado


def main():
    arquivo = get_xlsx()
    if arquivo is None:
        return

    cnpj_filtro = input("Digite o CNPJ para filtrar: ")

    df_filtrado = format_xlsx(arquivo, cnpj_filtro)

    if df_filtrado is not None and not df_filtrado.empty:
        nome_saida = f"filtrada_{os.path.basename(arquivo)}"
        output_file = os.path.join(OUTPUT_FOLDER, nome_saida)
        df_filtrado.to_excel(output_file, index=False)
        print(f"Planilha filtrada salva com sucesso em {output_file}!")
    else:
        print("Nenhum dado encontrado para o CNPJ especificado.")


if __name__ == "__main__":
    main()
