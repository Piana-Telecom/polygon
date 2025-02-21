import simplekml as skml
import pandas as pd
import datetime as dt
import time
import glob
import os

# Criar pasta de saída se não existir
OUTPUT_FOLDER = "KML_output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def get_xlsx():
    all_files = glob.glob("planilha_filtrada*.xlsx")  
    if not all_files:
        print("Nenhum arquivo .xlsx com prefixo 'planilha_filtrada' encontrado.")
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


def main():
    # Escolher o arquivo .xlsx
    arquivo = get_xlsx()

    if arquivo:
        df = pd.read_excel(arquivo)
        print(df)

        kml = skml.Kml()

        for _, feature in df.iterrows():
            new_point = kml.newpoint()
            new_point.name = feature["n_ps"]
            new_point.coords = [(feature["wgs_lon"], feature["wgs_lat"])]

        
        output_path = os.path.join(OUTPUT_FOLDER, f"ces_query_{arquivo}.kml")

        kml.save(output_path)

        print(f"Arquivo KML gerado com sucesso: {output_path}")
        print(f"ExecTime: {(time.time() - st) / 60:.2f} min")
    else:
        print("Erro ao carregar o arquivo.")


# Início do programa
if __name__ == "__main__":
    st = time.time()  # Marcar tempo de execução
    main()
