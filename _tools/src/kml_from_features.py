import simplekml as skml
import pandas as pd
import datetime as dt
import time

# features = input("Nome do arquivo (sem exteção)")
st = time.time()
features = f"pontos CERTTO"

df = pd.read_excel(f"{features}.xlsx")
print(df)
kml = skml.Kml()

for idx, feature in df.iterrows():
    # if feature['owned'] == 'n':
    #     continue
    new_point = kml.newpoint()
    new_point.name = feature['n_ps']
    new_point.coords = [(feature['wgs_lon'],feature['wgs_lat'])]

now = str(dt.datetime.now())
now = now.replace(':','_')
now = now.replace('.','_')
now = now.replace(' ','_')
now = now.replace('-','_')

kml.save(f'ces_query_{now}.kml')
print(f"ExecTime : {(time.time() - st)/60} min")
