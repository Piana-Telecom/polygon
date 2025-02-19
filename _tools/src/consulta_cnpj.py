import pandas as pd
import requests

# Carregar os CNPJs
df = pd.read_excel('Processed_Owner_List.xlsx')

# Função para consultar razão social
def consultar_razao_social(cnpj):
    url = f'https://receitaws.com.br/v1/cnpj/{cnpj}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('nome', 'Não encontrado')
    else:
        return 'Erro na consulta'

# Aplicar a função e salvar os dados
df['Razao_Social'] = df['owner_list'].apply(consultar_razao_social)
df.to_excel('Processed_Owner_List_Com_Razao_Social.xlsx', index=False)
