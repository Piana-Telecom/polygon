from __future__ import annotations
from vector2d import Vec2d
from shapely import Polygon

class Envelope:

    def __init__(self, top:int, bottom:int, right:int, left:int ) -> None:
        
        self.top = top
        self.bottom = bottom
        self.right = right
        self.left = left

        self.height = abs(top-bottom)
        self.width = abs(right-left)

    def __str__(self) -> str:
        return f"{self.top}, {self.bottom}, {self.right}, {self.left}"

    def as_polygon(self) -> Polygon:
        points = [
            (self.right, self.top),
            (self.left, self.top),
            (self.left, self.bottom),
            (self.right, self.bottom)
        ]
        bbox = Polygon(points)
        return bbox

    @staticmethod
    def from_points(point_a : Vec2d, point_b : Vec2d) -> Envelope:
        
        assert point_a.x != point_b.x
        assert point_a.y != point_b.y

        if point_a.x > point_b.x:
            _r = point_a.x
            _l = point_b.x
        else:
            _r = point_b.x
            _l = point_a.x

        if point_a.y > point_b.y:
            _t = point_a.y
            _b = point_b.y
        else:
            _t = point_b.y
            _b = point_a.y

        return Envelope(_t,_b,_r,_l)
