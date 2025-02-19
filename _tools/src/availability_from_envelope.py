import pandas as pd
import datetime as dt
from envelope import Envelope
from vector2d import Vec2d
from gridmap import Gridmap, Gridcell
from utils import batch_coords_trasform
from ces_requests import query_ces_dados

def envelope_from_input(p1 : str, p2 : str) -> Envelope:
    
    p1_xy = p1.split(',')
    p2_xy = p2.split(',')

    if len(p1_xy) != 2 or len(p2_xy) != 2 :
        raise Exception('-> Input splits into the wrong amount of elements')

    try:
        p1_tuple = tuple([float(element) for element in p1_xy])
        p2_tuple = tuple([float(element) for element in p2_xy])

    except:
        Exception("-> One or more element within input could not be parsed into a float")

    sirgas_coords = batch_coords_trasform([p1_tuple,p2_tuple], 'w', 's')

    return Envelope.from_points(Vec2d.from_list(sirgas_coords[0]), Vec2d.from_list(sirgas_coords[1]))

if __name__ == "__main__":

    input_p1 = "-25.082572,-52.891859"
    input_p2 = "-25.122107,-52.843830"

    envelope  = envelope_from_input(input_p1, input_p2)
    gridmap = Gridmap.from_envelope(envelope)
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
    for idx, gridcell in enumerate(gridmap.cells):
        response = query_ces_dados(gridcell)
        features = None
        if 'features' in response:
            features = response['features']
        if features != None:
            amount = len(features)
            if amount < 1000 :
                print(f"-> {amount} features found [sector {idx+1} from {gricells_amount}]")
            else:
                print(f'1000 or more features found, possible data loss [sector {idx+1} from {gricells_amount}]')
            for feature in features:
                attribs = feature['attributes']
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
    coord_list = [(row['sad_x'],row['sad_y']) for _, row in df.iterrows()]
    wgs_coords = batch_coords_trasform(coord_list, 's', 'w')
    lat = [wgs_coord[0] for wgs_coord in wgs_coords]
    lon = [wgs_coord[1] for wgs_coord in wgs_coords]
    df.insert(10, "wgs_lat", lat, True)
    df.insert(11, "wgs_lon", lon, True)
    now = str(dt.datetime.now())
    now = now.replace(':','_')
    now = now.replace('.','_')
    now = now.replace(' ','_')
    now = now.replace('-','_')
    df.to_excel(f'CES_availability_{now}.xlsx')

