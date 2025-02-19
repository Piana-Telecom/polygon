from pyproj import CRS, Transformer
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from shapely import Polygon

REF = "{http://www.opengis.net/kml/2.2}"

def get_crs_from_input(crs_input) -> CRS:

    crs_type = type(crs_input)

    if crs_type == str:

        _crs : str = crs_input.strip().lower()

        if _crs.startswith('s'):
            
            #sirgas from gpt
            #"+proj=tmerc +lat_0=0 +lon_0=-51 +k=0.9996 +x_0=500000 +y_0=10000000 +ellps=GRS80 +units=m +no_defs"

            #sad69(96) z22
            #"+proj=utm +zone=22 +south +ellps=aust_SA +towgs84=-67.35,3.88,-38.22,0,0,0,0 +units=m +no_defs +type=crs"

            #sirgar 2000 z22
            #"+proj=utm +zone=22 +south +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs +type=crs"

            return CRS("+proj=utm +zone=22 +south +ellps=aust_SA +towgs84=-67.35,3.88,-38.22,0,0,0,0 +units=m +no_defs +type=crs")

        elif _crs.startswith('u'):
            
            try:
                utmcode = int(f'327{_crs[-2:]}')
            except:

                raise Exception(f"-> utm zone couldn't be parsed {_crs[-2:]}")

            return CRS(utmcode)

        elif _crs.startswith('w'):
            
            return CRS(4326)
        
    if crs_type == int:
        
        return CRS(crs_input)

    else:
        raise Exception('-> CRS input is not of a valid type ')

def batch_coords_trasform(vec_list : list[tuple], from_crs, to_crs) -> list[tuple]:

    _from_crs = get_crs_from_input(from_crs)
    _to_crs = get_crs_from_input(to_crs)
    _transf = Transformer.from_crs(_from_crs, _to_crs)

    trans_vec_list = []

    for vec in _transf.itransform(vec_list):

        trans_vec_list.append(vec)

    return trans_vec_list

def get_coords(_elem : Element):
    f_coords = []
    coords = _elem.findall(".//"+REF+'coordinates')[0].text.replace('\n','').replace('\t','').split(' ')
    try:
        coords.remove('')
    except:
        pass
    for coord in coords:
        splited_coord = coord.split(',')
        f_coords.append((float(splited_coord[1]), float(splited_coord[0])))
    return f_coords

def polygon_from_kml(file : str):
    file_name = file
    with open(file_name + ".kml", 'r', encoding="utf-8") as file:
        kml_as_str = file.read()
        root = ET.fromstring(kml_as_str)
        placemarks = root.findall(".//"+REF+'Placemark')
        for placemark in placemarks:
            polygons = placemark.findall(".//"+REF+"LineRing") + placemark.findall(".//"+REF+"LinearRing")
            if len(polygons) < 1:
                continue 
            for poly in polygons:
                points = get_coords(poly)
                proj_points = batch_coords_trasform(points, 'w', 's')
                s_poly = Polygon(proj_points)
                return s_poly    


if __name__ == "__main__":
    poly = polygon_from_kml('input')
    print(poly.bounds)