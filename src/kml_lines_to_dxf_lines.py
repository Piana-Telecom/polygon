import xml.dom.minidom as xml
import ezdxf as ez
from utils import batch_coords_trasform

file = 'F.D'
dom = xml.parse(f'{file}.kml')
exp_dxf = ez.new()
msp = exp_dxf.modelspace()
#____________________________________________________________________________
group = dom.documentElement
lines = group.getElementsByTagName('coordinates')
f_lines = []

for line in lines:
    coords = str(line.childNodes[0].nodeValue)
    coords = coords.replace('\n','').replace('\t','')
    coords = coords.split(' ')
    if len(coords) < 2:
        continue
    coords_as_floats = []
    for coord in coords:
        components = coord.split(',')
        if len(components) < 2:
            continue
        try:
            f_coord = (float(components[1]), float(components[0]))
        except:
            print(f'-> Could not parse components to float {components}')
            continue
        coords_as_floats.append(f_coord)
    f_lines.append(coords_as_floats)

amount = len(f_lines)
idx = 1
for line in f_lines:
    t_line = batch_coords_trasform(line, 'w', 'u23')
    msp.add_lwpolyline(t_line, dxfattribs={'layer' : 'FaixaDeDominio', 'color' : 5})
    print(f'{idx} out of {amount}', end='\r')
    idx += 1

exp_dxf.saveas('FaixaDeDominio.dxf')

