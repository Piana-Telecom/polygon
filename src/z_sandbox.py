import pandas as pd

df = pd.read_excel("total_cascavel.xlsx")
for idx, row in df.iterrows():
    owners = str(row['owner_list']).split(',')
    unique = {}
    for owner in owners:
        if owner in unique:
            print(row['nps'])
        else:
            unique[owner] = 0
