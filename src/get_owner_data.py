import pandas as pd
import requests as r
import json
import time

class Error():
    def __init__(self, description : str):
        self.description = description

def validate_cnpj_input(cnpj : str) -> bool:
    assert type(cnpj) == str
    char_list = list(cnpj)
    if len(char_list) != 14:
        return False
    while len(char_list) > 0:
        current_char = char_list[0]
        if not current_char.isnumeric():
            return False
        char_list.pop(0)
    return True

def validate_json(json : dict) -> dict | Error:
    MUSTA_HAVE = ['nome','fantasia','porte','municipio','email','telefone','qsa']
    missing_fields = []
    for field in MUSTA_HAVE:
        if field not in json:
            missing_fields.append(field)
    if len(missing_fields) == 0:
        return json 
    else:
        return Error(description = f"missing fields {missing_fields}")

def owner_data_from_cnpj(cnpj : str) -> str | Error:
    if not validate_cnpj_input(cnpj):
        return Error(description='invalid cnpj')
    response = r.get(f"https://receitaws.com.br/v1/cnpj/{cnpj}", timeout=10)
    return response.text

if __name__ == "__main__":
    dtypes = {'owner' : str, 'frquency' : int}
    df = pd.read_csv('data\\ownership_frequency_all.csv', dtype=dtypes)
    out_df = pd.DataFrame(columns=[
        'cnpj',
        'frequency',
        'nome',
        'nomef',
        'porte',
        'municipio',
        'email',
        'telefone',
        'qsa'
    ])

    amount = len(df)
    for idx, row in df.iterrows():
        try:
            st = time.time()
            print(f"{idx} out of {amount}", end="\r")
            cnpj = row['owner']
            raw_content = owner_data_from_cnpj(cnpj)
            if type(raw_content) == Error:
                print(f'{raw_content.description} at {idx}')
                continue
            try:
                content = validate_json(json.loads(raw_content))
            except:
                print('could not load json')
                continue

            if type(content) == Error:
                print(f"{content.description} at {idx}")
                continue
            out_df.loc[len(out_df)] = [
                cnpj,
                row['frquency'], 
                content['nome'],
                content['fantasia'],
                content['porte'],
                content['municipio'],
                content['email'],
                content['telefone'],
                str(content['qsa']),
            ]
            sleep_time = 21 - ((time.time() - st))
            time.sleep(sleep_time)
        except:
            continue

    out_df.to_excel("owner_data.xlsx")