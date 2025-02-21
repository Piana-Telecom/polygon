import pandas as pd
import os
from shapely import Point
import datetime as dt
from vector2d import Vec2d
from gridmap import Gridmap
from utils import batch_coords_trasform, polygon_from_kml
from ces_requests import query_ces_postes_transf
import time

if __name__ == "__main__":
    kml_files = [f for f in os.listdir('.') if f.endswith('.kml')]
    
    if not kml_files:
        print("Nenhum arquivo .kml encontrado.")
        exit()
    
    # Mostrar opções para o usuário
    print("Escolha um arquivo .kml:")
    for idx, file in enumerate(kml_files, start=1):
        print(f"{idx}: {file}")
    
    # Obter a escolha do usuário
    while True:
        try:
            choice = int(input("Digite o número do arquivo desejado: "))
            if 1 <= choice <= len(kml_files):
                file = kml_files[choice - 1]
                break
            else:
                print("Número inválido, tente novamente.")
        except ValueError:
            print("Entrada inválida, digite um número válido.")
    
    file_name = os.path.basename(file).replace('.kml', '')  
    poly = polygon_from_kml(file_name)
    gridmap = Gridmap.from_polygon(poly)
    df = pd.DataFrame(columns=[
        'n_ps',
        'owner_list',
        'sector',
        'sad_x',
        'sad_y',
    ])
    gricells_amount = len(gridmap.cells)
    st_query_time = time.time()
    
    for idx, gridcell in enumerate(gridmap.cells):
        while True:
            response = query_ces_postes_transf(gridcell)
            if 'error' not in response:
                break
            else:
                print(response)
        
        features = response.get('features', None)
        if features is None:
            print(response)
        
        if features:
            amount = len(features)
            if amount < 1000:
                print(f"[+] {amount} features found [sector {idx+1} from {gricells_amount}] - dt = {time.time() - st_query_time}")
            else:
                print(f'1000 or more features found, possible data loss [sector {idx+1} from {gricells_amount}]')
            
            for feature in features:
                attribs = feature['attributes']
                p = Point(attribs["COORD_X"], attribs["COORD_Y"])
                if poly.contains(p):
                    df.loc[len(df)] = [
                        attribs["NUM_SEQ_GEO"],  # 'n_ps'
                        attribs["NUM_CNPJ_PREL"],  # owner_list
                        gridcell.sector,  # setor
                        attribs["COORD_X"],  # sad x
                        attribs["COORD_Y"]  # sad y
                    ]
        
        st_query_time = time.time()
    
    coord_list = [(row['sad_x'], row['sad_y']) for _, row in df.iterrows()]
    wgs_coords = batch_coords_trasform(coord_list, 's', 'w')
    lat = [wgs_coord[0] for wgs_coord in wgs_coords]
    lon = [wgs_coord[1] for wgs_coord in wgs_coords]
    df.insert(len(df.columns), "wgs_lat", lat, True)
    df.insert(len(df.columns), "wgs_lon", lon, True)
    
    now = dt.datetime.now().strftime('%d-%m-%Y-%H-%M')
    df.to_excel(f'CES_ownership_{file_name}_{now}.xlsx')
    print(f'Arquivo salvo como CES_ownership_{file_name}_{now}.xlsx')