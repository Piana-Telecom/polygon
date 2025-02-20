import pandas as pd

def qsa_to_list(qsa : str):
    _qsa_list = eval(qsa)
    if len(_qsa_list) <= 0:
        return False
    return _qsa_list

source_df = pd.read_excel("owner_data.xlsx")
out_df = pd.DataFrame(columns=[
    'cnpj',
    'name',
    'prop_name',
    'email',
    'tel'
])

for idx, row in source_df.iterrows():
    prop_list = qsa_to_list(row['qsa'])
    if prop_list:
        for prop in prop_list:
            if 'nome' in prop:
                out_df.loc[len(out_df)] = [
                    row['cnpj'],
                    row['nome'],
                    prop['nome'],
                    row['email'],
                    row['telefone']
                ]
                print(prop['nome'])

out_df.to_excel('prop_table.xlsx')
