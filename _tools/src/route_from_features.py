import pandas as pd
from qtree import Point, QTree, QueryRadius, Line
import simplekml
import time
import traceback
import datetime as dt
import os
import ezdxf as ez

def line_from_point(point : Point, qtree : QTree, seen : list[Point], radius : int):

    _seen = []

    query = QueryRadius(point, query_radius)
    query.find(qtree)

    line_starters : list[Point] = []

    for result in query.points:

        if result == point:
            continue
        if result in seen or result in _seen:
            continue
        if not result.is_availeble:
            continue

        _seen.append(result)
        line_starters.append([point, result])

    possible_lines = []

    for starter in line_starters:

        query.update(starter[-1])
        query.find(qtree)

        for result in query.points:

            if result == point:
                continue
            if result in seen or result in _seen:
                continue
            if not result.is_availeble:
                continue    

            try:
                angle = Point.three_point_angle(starter[-1], point, result)
            except:
                angle = 0

            if angle < 2.79253:
                continue

            weight = angle                    

            possible_lines.append((weight, [point, starter[-1], result]))

    possible_lines.sort(key = lambda tup : tup[0], reverse=True)

    if len(possible_lines) > 0:
        return Line(possible_lines[0][1])

try :

    arquivo = None
    dxf_route = 'draw_points'
    if dxf_route and dxf_route != '' :
        dxf_file = ez.readfile(f'{dxf_route}.dxf')
        msp = dxf_file.modelspace()

    while not arquivo:
        input_file = "not_owned"
        if os.path.isfile(f'{os.getcwd()}\\{input_file}.xlsx'):
           arquivo = input_file
        else:
            print('-> Input file is not valid')

    query_radius = None

    while not query_radius:
        try:
            query_radius = int(input("Raio de pesquisa(em metros): "))
        except:
            print(f"-> Input coudn't be cast into an intger")

    st = time.time()

    df = pd.read_excel(f"{arquivo}.xlsx")
    kml = simplekml.Kml()

    qt_top = df['sad_y'].max() + 500
    qt_bottom = df['sad_y'].min() - 500
    qt_right = df['sad_x'].max() + 500
    qt_left = df['sad_x'].min() - 500

    qtree = QTree(2,qt_top,qt_bottom,qt_right,qt_left)
    point_list : list[Point] = []

    for ind, row in df.iterrows():

        availability = False

        match row['situação']:
            case 'Disponível':
                availability = True
            case 'Possível disponibilidade' :
                availability = True
            case 'Indisponível':
                availability = False
            case _:
                availability = False

        wgs_coord = (row['wgs_lon'], row['wgs_lat'])

        new_point = Point(
            row['sad_x'],
            row['sad_y'],
            data = {
                'situacao' : row['situação'],
                'wgs_coord' : wgs_coord
            },
            is_availeble = availability
            )

        qtree.insert(new_point)
        point_list.append(new_point)

    point_list.sort(key= lambda point : point.y - point.x, reverse = True)

    amount_of_points = len(point_list)
    seen = []

    for ind, point in enumerate(point_list):

        print(f"{ind} of {amount_of_points}", end='\r')

        if point in seen:
            continue

        
        if "situacao" in point.data:
            if point.data['situacao'] == "Indisponível":
                continue

        line = line_from_point(point, qtree, seen, query_radius)

        if line:

            line.walk(line.points[-1], qtree, seen)

            wgs_line = [pt.data['wgs_coord'] for pt in line.points]

            new_line = kml.newlinestring()
            new_line.coords = wgs_line
            line.draw_dxf(msp)

            for seen_point in line.points:
                seen.append(seen_point)

            seen.append(point)

    now = str(dt.datetime.now())
    now = now.replace(':','_')
    now = now.replace('.','_')
    now = now.replace(' ','_')
    now = now.replace('-','_')

    kml.save(f'route_{now}.kml')
    dxf_file.saveas('draw_route.dxf')

    print(f"ExecTime : {(time.time() - st)/60} min")

except:

    print(traceback.format_exc())
    input('algo deu errado. entre em contato com o suporte.')    
