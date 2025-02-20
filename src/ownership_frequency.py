import pandas as pd
import datetime as dt

source_file = "conjunto_andira"
source_df = pd.read_excel(f"{source_file}.xlsx")
out_df = pd.DataFrame(columns=['owner', 'n_ps'])

amount = len(source_df)
for idx, row in source_df.iterrows():
    print(f"{idx} of {amount}", end='\r')
    owner_list = str(row['owner_list']).split(',')
    for owner in owner_list:
        out_df.loc[len(out_df)] = [
            owner,
            row["n_ps"]
        ]

now = str(dt.datetime.now())
now = now.replace(':','_')
now = now.replace('.','_')
now = now.replace(' ','_')
now = now.replace('-','_')
out_df.to_excel(f'CES_ownership_frequency_{now}.xlsx')
