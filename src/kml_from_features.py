import simplekml as skml
import pandas as pd
import time
import glob
import os

# Criar pasta de saída se não existir
OUTPUT_FOLDER = "KML_output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def get_xlsx():
    all_files = glob.glob(os.path.join("FILTRADA_output", "filtrada*.xlsx"))  
    if not all_files:
        print("Nenhum arquivo .xlsx com prefixo 'filtrada' encontrado.")
        return None

    print("Escolha o arquivo .xlsx desejado:")
    for i, file in enumerate(all_files, start=1):
        # Mostrando apenas o nome do arquivo, sem o caminho
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


def main():
    # Escolher o arquivo .xlsx
    arquivo = get_xlsx()

    if arquivo:
        df = pd.read_excel(arquivo)
        print(df)

        kml = skml.Kml()

        for _, feature in df.iterrows():
            new_point = kml.newpoint()

            # Corrigir o nome para evitar valores float com .0
            name_value = feature["n_ps"]
            if isinstance(name_value, float) and name_value.is_integer():
                name_value = int(name_value)  # Converte float para inteiro se não houver fração

            new_point.name = str(name_value)  # Garante que seja string
            new_point.coords = [(feature["wgs_lon"], feature["wgs_lat"])]

        # Extrair apenas o nome base para gerar o arquivo KML corretamente
        nome_base = os.path.basename(arquivo)
        data_hora = nome_base.split("_")[-2:]  # Pega a data e hora no final
        nome_kml = f"ces_query_input_{'-'.join(data_hora).replace('.xlsx', '')}.kml"

        output_path = os.path.join(OUTPUT_FOLDER, nome_kml)

        kml.save(output_path)

        print(f"Arquivo KML gerado com sucesso: {output_path}")
        print(f"ExecTime: {(time.time() - st) / 60:.2f} min")
    else:
        print("Erro ao carregar o arquivo.")


# Início do programa
if __name__ == "__main__":
    st = time.time()  # Marcar tempo de execução
    main()
