from __future__ import annotations
import pandas as pd
import ezdxf as ez
from ezdxf.layouts.layout import Modelspace
import math

def get_color(situacao : str) -> int:

    match situacao:
        case 'Disponível' :
            return 3
        
        case 'Indisponível' :
            return 1
        
        case 'Possível disponibilidade' :
            return 2
        
        case _:
            return None

class Point:

    def __init__(self, x : int | float, y : int | float, data : dict = {}, is_availeble = False) -> None:

        self.x = x
        self.y = y
        self.data = data
        self.is_availeble = is_availeble

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def magnitude(self) -> float:
        return ((self.x ** 2) + (self.y ** 2))**0.5

    def distance_to(self, other : Point) -> float:

        return  ( (self.x - other.x)**2 + (self.y - other.y)**2 ) ** 0.5

    def as_tuple(self) -> tuple:
        return (self.x, self.y)

    def make_absolute(self) -> None:

        self.x = abs(self.x)
        self.y = abs(self.y)

    @staticmethod
    def from_string(string : str) -> Point:
        
        formated_string = string.replace('(','').replace(')','')
        formated_string = string.split(',')

        new_point = Point(*formated_string)
        return new_point

    @staticmethod
    def dot(p1 : Point, p2 : Point) -> Point:
        return ((p1.x * p2.x) + (p1.y * p2.y))

    @staticmethod
    def three_point_angle(common : Point, p1 : Point, p2 : Point):
        p1_from_origin = Point(p1.x-common.x, p1.y-common.y)
        p2_from_origin = Point(p2.x-common.x, p2.y-common.y)

        dot_product = Point.dot(p1_from_origin, p2_from_origin)

        magA = p1_from_origin.magnitude()
        magB = p2_from_origin.magnitude()

        if magA == 0 or magB == 0:
            return 0

        angle = math.acos(dot_product/(magA*magB))

        return angle
   
    @staticmethod
    def add(p1 : Point, p2 : Point):
        return Point(p1.x + p2.x, p1.y + p2.y)

class Line:

    def __init__(self, points : list[Point] = [], query_radius : int = 50) -> None:
        
        self.points = points
        self.query = QueryRadius(Point(0,0), query_radius)

    def __repr__(self) -> str:
        return f"line of lenght {len(self.points)}"

    def walk(self, point : Point, qtree : QTree, seen : list[Point] | None = None):

        if len(self.points) <= 0:
            self.points.append(point)

        self.query.update(point)
        self.query.find(qtree)

        if self.query.points:

            new_point = self.find_next_point(point, self.query.points, seen)

            if new_point:
                self.points.append(new_point)
                self.walk(new_point, qtree, seen)

    def draw_dxf(self, msp : Modelspace):

        msp.add_lwpolyline(
            [point.as_tuple() for point in self.points]
        )

    def find_next_point(self, ref_point : Point, candidates : list[Point], seen : list[Point]):

        to_sort = []

        for candidate in candidates:

            if candidate in self.points:
                continue

            if candidate == ref_point:
                continue

            if not candidate.is_availeble:
                continue
            
            if seen:
                if candidate in seen:
                    continue

            if len(self.points) < 2:

                weight = ref_point.distance_to(candidate)

                if 18 >= weight:
                    continue

                to_sort.append((weight, candidate))
            
            else:
                try:
                    angle = Point.three_point_angle(ref_point, self.points[-2], candidate)
                except:
                    angle = 0

                if angle < 2.79253:
                    continue

                weight = angle*-1

                to_sort.append((weight, candidate))

        to_sort.sort(key =lambda tup : tup[0])

        if to_sort:
            return to_sort[0][-1]

class QTree:

    def __init__(self, capacity : int , top:int, bottom:int, right:int, left:int , ) -> None:

        self.capacity = capacity

        self.points : list[Point] = []

        self.top = top
        self.bottom = bottom
        self.right = right
        self.left = left

        self.height = abs(top-bottom)
        self.width = abs(right-left)

        self.is_divided = False

    def __len__(self):

        count = len(self.points)

        if self.is_divided:

            count += len(self.tr_quad)
            count += len(self.tl_quad)
            count += len(self.br_quad)
            count += len(self.bl_quad)
        
        return count

    def __iter__(self):

        for point in self.points[:]:
            yield point
        
        if self.is_divided:

            yield from self.tr_quad
            yield from self.tl_quad
            yield from self.br_quad
            yield from self.bl_quad

    def __str__(self):
        return f"t:{self.top}, b:{self.bottom}, r:{self.right}, l:{self.left}"

    def divide(self) -> None:

        _w = self.width
        _h = self.height

        _t = self.top
        _b = self.bottom
        _r = self.right
        _l = self.left

        self.tr_quad = QTree(
            self.capacity,
            _t, _t-_h/2, _r, _r-_w/2,
        )
        self.tl_quad = QTree(
            self.capacity,
            _t, _t-_h/2,_l+_w/2, _l,
        )
        self.br_quad = QTree(
            self.capacity,
            _b+_h/2, _b, _r, _r-_w/2,
        )
        self.bl_quad = QTree(
            self.capacity,
            _b+_h/2, _b, _l+_w/2, _l,
        )

        self.is_divided = True

    def insert(self, point : Point) -> bool:
        if not self.contains(point):
            return False
        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        if not self.is_divided:
            self.divide()

        return (
            self.tr_quad.insert(point) or
            self.tl_quad.insert(point) or
            self.br_quad.insert(point) or
            self.bl_quad.insert(point)
        )

    def intersects(self, top:int, bottom:int, right:int, left:int) -> bool:

        return(
            top >= self.bottom or
            bottom <= self.top or
            left >= self.right or
            right <= self.left
        )

    def contains(self, point : Point) -> bool:

        return (
            point.x > self.left and
            point.x <= self.right and
            point.y > self.bottom  and
            point.y <= self.top
        )

    def is_empty(self) -> bool:

        if len(self.points) <= 0:
            return True
        else:
            return False

    def draw(self, level = 0):

        tab = '\t' * level

        print(f'{tab}{self} - len: {len(self.points)}')

        if self.is_divided:

            self.tr_quad.draw(level+1)
            self.tl_quad.draw(level+1)
            self.br_quad.draw(level+1)
            self.bl_quad.draw(level+1)
        
    def draw_dxf(self, msp : Modelspace, draw_quads = False):

        if draw_quads:

            msp.add_lwpolyline(
                [
                    (self.left, self.top),
                    (self.right, self.top),
                    (self.right, self.bottom),
                    (self.left, self.bottom)
                ],
                close = True,
            )

        for point in self.points:

            color = 0

            if 'situacao' in point.data:

                color = get_color(point.data['situacao'])

            msp.add_circle(
                (point.x, point.y),
                3,
                dxfattribs= {'color' : color}
            )

        if self.is_divided:

            self.tr_quad.draw_dxf(msp, draw_quads)
            self.tl_quad.draw_dxf(msp, draw_quads)
            self.br_quad.draw_dxf(msp, draw_quads)
            self.bl_quad.draw_dxf(msp, draw_quads)

    @staticmethod
    def from_points(capacity : int, p1 : Point, p2 : Point) -> QTree:

        if p1[0] == p2[0]:

            raise Exception('-> Left and right are equal')

        elif p1[0] > p2[0]:

            right = p2[0]
            left = p1[0]

        else:

            right = p1[0]
            left = p2[0]

        if p1[1] == p2[1]:

            raise Exception('-> Top and Bottom are equal')

        elif p1[1] > p2[1]:

            top = p2[1]
            bottom = p1[1]

        else:

            top = p1[1]
            bottom = p2[1]        

        return QTree(capacity, top, bottom, right, left)

class QueryEnvelope:

    def __init__(self, top:int, bottom:int, right:int, left:int) -> None:

        self.points : list[Point] = []
        self.top = top 
        self.bottom = bottom
        self.right = right
        self.left = left  

    def contains(self, point : Point) -> bool:

        return (
            point.x > self.left and
            point.x <= self.right and
            point.y > self.bottom  and
            point.y <= self.top
        )

    def find(self, qtree : QTree) -> None:

        if not qtree.intersects(self.top,self.bottom,self.right,self.left):
            return False
        
        for point in qtree.points:
            if self.contains(point):
                self.points.append(point)
        
        if qtree.is_divided:
            self.find(qtree.tr_quad)
            self.find(qtree.tl_quad)
            self.find(qtree.br_quad)
            self.find(qtree.bl_quad)

    def draw_dxf(self,  msp : Modelspace) -> None:

        msp.add_lwpolyline(
            [
                (self.left, self.top),
                (self.right, self.top),
                (self.right, self.bottom),
                (self.left, self.bottom)
            ],
            close = True,
            dxfattribs={'color' : 3}
        )

        for point in self.points:

            msp.add_circle(
                (point.x, point.y),
                4,
                dxfattribs= {'color' : 3}
            )

class QueryRadius:

    def __init__(self, point : Point, radius : int | float) -> None:
        
        self.points : list[Point] = []

        self.center = point
        self.radius = radius

        self.top = self.center.y + self.radius
        self.bottom = self.center.y - self.radius
        self.right = self.center.x + self.radius 
        self.left = self.center.x - self.radius

    def contains(self, point : Point) -> bool:

        return (
            point.x > self.left and
            point.x <= self.right and
            point.y > self.bottom  and
            point.y <= self.top
        )    

    def find(self, qtree: QTree) -> None:

        if not qtree.intersects(self.top,self.bottom,self.right,self.left):
            return False

        for point in qtree.points:
            if (self.center.distance_to(point) <= self.radius):

                self.points.append(point)

        if qtree.is_divided:
            self.find(qtree.tr_quad)
            self.find(qtree.tl_quad)
            self.find(qtree.br_quad)
            self.find(qtree.bl_quad)        

    def draw_dxf(self,  msp : Modelspace) -> None:

        msp.add_circle(
            self.center.as_tuple(),
            self.radius,
            dxfattribs={"color" : 4}
        )

        for point in self.points:

            msp.add_circle(
                (point.x, point.y),
                4,
                dxfattribs= {'color' : 4}
            )

    def update(self, point : Point, radius : int | None = None ):

        if not radius:
            radius = self.radius
        else:
            self.radius = radius

        self.points : list[Point] = []

        self.center = point

        self.top = self.center.y + self.radius
        self.bottom = self.center.y - self.radius
        self.right = self.center.x + self.radius 
        self.left = self.center.x - self.radius        

if __name__ == "__main__":

    pass
