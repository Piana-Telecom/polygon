from __future__ import annotations
import math

def rotation_matrix(angle : float) -> tuple[Vec2d]:
    cos = round(math.cos(angle), 6)
    sin = round(math.sin(angle), 6)
    r_matrix = (Vec2d(cos, sin), Vec2d(-sin, cos))
    return r_matrix

class Vec2d:

    def __init__(self, x :  float, y : float) -> None:
        self.x = x
        self.y = y 

    @property
    def magnitude(self):
        return  abs(((self.x ** 2) + (self.y ** 2))**0.5)

    @property
    def angle(self):
        _angle = math.atan2(self.y,self.x)
        return _angle if _angle > 0 else _angle + math.pi *2   

    def __str__(self) -> str:
        return str(f'[{self.x}, {self.y}]')

    def __add__(self, other : Vec2d) -> Vec2d:
        assert type(other) == Vec2d
        return Vec2d(self.x + other.x, self.y + other.y)

    def __iadd__(self, other : Vec2d) -> Vec2d:
        assert type(other) == Vec2d
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other : Vec2d) -> Vec2d:
        assert type(other) == Vec2d
        return Vec2d(self.x - other.x, self.y - other.y)

    def __isub__(self, other: Vec2d) -> Vec2d:
        assert type(other) == Vec2d
        self.x -= other.x
        self.y -= other.y
        return self     

    def __mul__(self, other) -> Vec2d:

        if type(other) == Vec2d:
            return Vec2d(self.x * other.x, self.y * other.y)
        else:
            return Vec2d(self.x * other, self.y * other)

    def __imul__(self, other: Vec2d) -> Vec2d:
        if type(other) == Vec2d:
            self.x *= other.x
            self.y *= other.y
        else:
            self.x *= other
            self.y *= other           
        return self 

    def __matmul__(self, other) -> float:
        assert type(other) == Vec2d
        return ((self.x * other.x) + (self.y * other.y))

    def __truediv__(self, other) -> Vec2d:

        if type(other) == Vec2d:
            return Vec2d(self.x / other.x, self.y / other.y)
        else:
            return Vec2d(self.x / other, self.y / other)      

    def __idiv__(self, other: Vec2d) -> Vec2d:
        if type(other) == Vec2d:
            self.x /= other.x
            self.y /= other.y
        else:
            self.x /= other
            self.y /= other           
        return self

    def __eq__(self, other) -> Vec2d:
        assert type(other) == Vec2d
        return(self.x == other.x and self.y == other.y)

    def __ne__(self, other) -> Vec2d:
        assert type(other) == Vec2d
        return(self.x != other.x and self.y != other.y)

    def as_tuple(self):
        return (self.x, self.y)

    def distance_to(self, other : Vec2d) -> float:
        return (((self.x - other.x)**2) + ((self.y - other.y)**2))**0.5

    def angle_to(self, other : Vec2d) -> float:
        """
        Create new vector, which is the difference between other and self.
        returns the angle of the resulting vector
        """
        assert type(other) == Vec2d
        _v = Vec2d(*(other - self).as_tuple)
        return _v.angle 

    def normalize(self) -> Vec2d:
        _m = self.magnitude

        self.x /= _m
        self.y /= _m
        return self

    def rotate(self, angle, degrees = False) -> Vec2d:
        _a = angle
        if degrees:
            _a = math.radians(_a)
        rmx = rotation_matrix(_a)
        i_hat = rmx[0]
        j_hat = rmx[1]
        t_vec = (i_hat*self.x) + (j_hat*self.y)
        return self

    @staticmethod
    def centroid(vector_list : list[Vec2d]) -> Vec2d:
        _center_vector = Vec2d.zero()

        for vector in vector_list:

            _center_vector += vector

        _center_vector /= len(vector_list)

        return _center_vector

    @staticmethod
    def from_list(component_list : list):

        _c_list = component_list[:]

        if len(_c_list) < 2:
            raise Exception("-> not enought components to create a vector")
        else:
            return Vec2d(_c_list[0], _c_list[1])
        
    @staticmethod
    def from_polar(magnitude : float, angle : float):
        """
        Angle must be provided in radians
        """

        _x = magnitude * math.cos(angle)
        _y = magnitude * math.sin(angle)

        return Vec2d(_x, _y)

    @staticmethod
    def zero():
        return Vec2d(0,0)

    @staticmethod
    def angle_between(vector_a : Vec2d, vector_b : Vec2d, offset : Vec2d = None) -> float:
        if not offset:
            offset = Vec2d.zero()

        va = vector_a - offset
        vb = vector_b - offset

        _angle  = math.acos(va @ vb/ (va.magnitude*vb.magnitude))
        return _angle

    @staticmethod
    def rotated(vector : Vec2d, angle : float, degrees = False) -> Vec2d:
        _a = angle
        if degrees:
            _a = math.radians(_a)
        rmx = rotation_matrix(_a)
        i_hat = rmx[0]
        j_hat = rmx[1]
        t_vec = (i_hat*vector.x) + (j_hat*vector.y)
        return t_vec

if __name__ == "__main__":
    pass
