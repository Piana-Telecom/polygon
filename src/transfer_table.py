import pandas as pd
import glob


# Função para selecionar o arquivo .xlsx
def get_xlsx():
    all_files = glob.glob("*.xlsx")  # Busca todos os arquivos .xlsx no diretório
    if len(all_files) > 1:
        print("Mais de um arquivo encontrado")
        for i, file in enumerate(all_files, start=1):
            print(f"{i}. {file}")
        escolha = int(input("Escolha o número do arquivo: "))
        if 1 <= escolha <= len(all_files):
            return all_files[escolha - 1]
        else:
            print("Arquivo não encontrado!")
            return None
    elif len(all_files) == 1:
        return all_files[0]
    else:
        print("Nenhum arquivo .xlsx encontrado.")
        return None


def format_xlsx(file, cnpj):
    if file is None:
        return None

    source_df = pd.read_excel(file)

    df_filtrado = source_df[
        source_df["owner_list"].apply(lambda x: cnpj in str(x).split(","))
    ]

    df_resultado = df_filtrado[["n_ps", "wgs_lat", "wgs_lon"]]

    return df_resultado


def main():
    arquivo = get_xlsx()
    cnpj_filtro = input("Digite o CNPJ para filtrar: ")

    if arquivo:
        # Processar o arquivo selecionado
        df_filtrado = format_xlsx(arquivo, cnpj_filtro)

        if df_filtrado is not None and not df_filtrado.empty:
            # Salvar o resultado em uma nova planilha
            nome_saida = "planilha_filtrada_" + arquivo
            df_filtrado.to_excel(nome_saida, index=False)
            print(f"Planilha filtrada salva com sucesso em {nome_saida}!")
        else:
            print("Nenhum dado encontrado para o CNPJ especificado.")
    else:
        print("Erro ao carregar o arquivo.")


if __name__ == "__main__":
    main()
