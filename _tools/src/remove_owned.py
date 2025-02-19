import pandas as pd
import datetime as dt

availability_data = 'CES_availability_2024_10_25_10_53_15_335609'
ownership_data = 'total_campomourão'

aval_df = pd.read_excel(f"{availability_data}.xlsx")
ownership_data = pd.read_excel(f'{ownership_data}.xlsx')
owned_ps_list = ownership_data['n_ps'].tolist()
found_idx_list = []
for idx, row in aval_df.iterrows():
    if row['n_ps'] in owned_ps_list:
        found_idx_list.append(idx)

aval_not_owned = aval_df.drop(found_idx_list)

now = str(dt.datetime.now())
now = now.replace(':','_')
now = now.replace('.','_')
now = now.replace(' ','_')
now = now.replace('-','_')
aval_not_owned.to_excel(f'not_owned_{now}.xlsx')
