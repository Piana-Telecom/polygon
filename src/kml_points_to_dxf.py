import xml.dom.minidom as xml
import ezdxf as ez
from utils import batch_coords_trasform
import traceback

try:
    file = input('Nome do arquivo (sem extensão):')
    dom = xml.parse(f'{file}.kml')
    exp_dxf = ez.new()
    msp = exp_dxf.modelspace()
    #____________________________________________________________________________
    group = dom.documentElement
    points = group.getElementsByTagName('coordinates')
    f_points = []

    for point in points:
        coords = str(point.childNodes[0].nodeValue)
        coords = coords.replace('\n','').replace('\t','')
        coords = coords.split(' ')
        coords_as_floats = []
        for coord in coords:
            components = coord.split(',')
            try:
                f_coord = (float(components[1]), float(components[0]))
            except:
                print(f'-> Could not parse components to float {components}')
                continue
            coords_as_floats.append(f_coord)
        f_points.append(coords_as_floats)

    amount = len(f_points)
    idx = 1
    for point in f_points:
        t_point = batch_coords_trasform(point, 'w', 's')
        msp.add_circle(t_point[0],4, dxfattribs={'layer' : 'PontosEarth', 'color' : 2})
        print(f'{idx} out of {amount}', end='\r')
        idx += 1

    exp_dxf.saveas('PontosEarth.dxf')
    input("-> Seu DXF esta pronto [aperte ENTER para sair]")

except:
    print(traceback.format_exc())
    input("-> Algo de errado aconteceu. entre em contato com o suporte [aperte ENTER para sair]")
