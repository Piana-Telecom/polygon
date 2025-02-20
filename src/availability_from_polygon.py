import pandas as pd
from shapely import Point
import datetime as dt
from vector2d import Vec2d
from gridmap import Gridmap
from utils import batch_coords_trasform, polygon_from_kml
from ces_requests import query_ces_dados
import time

if __name__ == "__main__":

    filter = False
    cnpj = '05236051000130'
    file = 'input'
    poly = polygon_from_kml(file)
    gridmap = Gridmap.from_polygon(poly)
    df = pd.DataFrame(columns=[
        'n_ps',
        'cod_ps',
        'ocupantes',
        'max_ocupantes',
        'situação',
        'equipamento',
        'particular',
        'sector',
        'sad_x',
        'sad_y',
    ])
    gricells_amount = len(gridmap.cells)
    st_query_time = time.time()
    for idx, gridcell in enumerate(gridmap.cells):
        while True:
            response = query_ces_dados(gridcell)
            if not 'error' in response:
                break
            else:
                print(response)
        features = None
        if 'features' in response:
            features = response['features']
        else:
            print(response)
        if features != None:
            amount = len(features)
            if amount < 1000 :
                print(f"-> {amount} features found [sector {idx+1} from {gricells_amount}] - dt = {time.time() - st_query_time}")
            else:
                print(f'1000 or more features found, possible data loss [sector {idx+1} from {gricells_amount}]')
            for feature in features:
                attribs = feature['attributes']
                p = Point(attribs["COORD_X"],attribs["COORD_Y"])
                if poly.contains(p):
                    df.loc[len(df)] = [
                        attribs["NUM_SEQ_GEO"], #'n_ps'
                        attribs["COD_POSTE_PS"], #'cod_ps'
                        attribs["PONTOSFIXACAOSEMCOPEL"], #'ocupantes'
                        attribs["LIMITEPONTOSFIX"], #'max_ocupantes'
                        attribs["SITUACAO"], #'situação'
                        attribs["POSSUI_EQUIP"], #'equipamento'
                        attribs["INDIC_PS_PARTICULAR"], #'particular'
                        gridcell.sector, #setor
                        attribs["COORD_X"], #sad x
                        attribs["COORD_Y"]  #sad y      
                    ]
        st_query_time = time.time()
    coord_list = [(row['sad_x'],row['sad_y']) for _, row in df.iterrows()]
    wgs_coords = batch_coords_trasform(coord_list, 's', 'w')
    lat = [wgs_coord[0] for wgs_coord in wgs_coords]
    lon = [wgs_coord[1] for wgs_coord in wgs_coords]
    df.insert(len(df.columns), "wgs_lat", lat, True)
    df.insert(len(df.columns), "wgs_lon", lon, True)
    now = str(dt.datetime.now())
    now = now.replace(':','_')
    now = now.replace('.','_')
    now = now.replace(' ','_')
    now = now.replace('-','_')
    df.to_excel(f'CES_availability_{now}.xlsx')
