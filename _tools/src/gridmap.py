from __future__ import annotations
from envelope import Envelope
from shapely import Polygon
from vector2d import Vec2d

class Gridcell(Envelope):
    def __init__(self, top: int, bottom: int, right: int, left: int, sector : str) -> None:
        super().__init__(top, bottom, right, left)
        self.sector = sector

    def __str__(self) -> str:
        return super().__str__()

class Gridmap:
    def __init__(self, cells : list[Gridcell]) -> None:
        self.cells : list[Gridcell] = cells

    @staticmethod
    def from_envelope(envelope : Envelope, cell_dim : int = 1000):

        xcells = int(envelope.width / cell_dim) + 1
        ycells = int(envelope.height / cell_dim) + 1
        xrem = envelope.width % cell_dim
        yrem = envelope.height % cell_dim

        _cells : list[Gridcell] = []

        for xcell in range(xcells):
            for ycell in range (ycells):
                grid_needle = Vec2d(envelope.left + (cell_dim*xcell), envelope.top - (cell_dim*ycell))
                sector = str(xcell) + str(ycell)

                if (xcell + 1) != xcells and (ycell+1) != ycells:
                    new_cell = Gridcell(
                        grid_needle.y,
                        grid_needle.y - cell_dim,
                        grid_needle.x + cell_dim,
                        grid_needle.x,
                        sector
                    )
                    _cells.append(new_cell)
                elif (xcell + 1) == xcells and (ycell+1) != ycells:
                    new_cell = Gridcell(
                        grid_needle.y,
                        grid_needle.y - cell_dim,
                        grid_needle.x + xrem,
                        grid_needle.x,
                        sector
                    )
                    _cells.append(new_cell)
                elif (xcell + 1) != xcells and (ycell+1) == ycells:
                    new_cell = Gridcell(
                        grid_needle.y,
                        grid_needle.y - yrem,
                        grid_needle.x + cell_dim,
                        grid_needle.x,
                        sector
                    )
                    _cells.append(new_cell)
                elif (xcell + 1) == xcells and (ycell+1) == ycells:
                    new_cell = Gridcell(
                        grid_needle.y,
                        grid_needle.y - yrem,
                        grid_needle.x + xrem,
                        grid_needle.x,
                        sector
                    )
                    _cells.append(new_cell)
        return Gridmap(_cells)  

    @staticmethod
    def from_polygon(poly : Polygon, cell_dim : int = 1000):
        b = poly.bounds
        envelope = Envelope(b[3],b[1],b[2],b[0])
        xcells = int(envelope.width / cell_dim) + 1
        ycells = int(envelope.height / cell_dim) + 1
        xrem = envelope.width % cell_dim
        yrem = envelope.height % cell_dim

        _cells : list[Gridcell] = []

        for xcell in range(xcells):
            for ycell in range (ycells):
                grid_needle = Vec2d(envelope.left + (cell_dim*xcell), envelope.top - (cell_dim*ycell))
                sector = str(xcell) + str(ycell)
                new_cell = None
                if (xcell + 1) != xcells and (ycell+1) != ycells:
                    new_cell = Gridcell(
                        grid_needle.y,
                        grid_needle.y - cell_dim,
                        grid_needle.x + cell_dim,
                        grid_needle.x,
                        sector
                    )
                elif (xcell + 1) == xcells and (ycell+1) != ycells:
                    new_cell = Gridcell(
                        grid_needle.y,
                        grid_needle.y - cell_dim,
                        grid_needle.x + xrem,
                        grid_needle.x,
                        sector
                    )
                elif (xcell + 1) != xcells and (ycell+1) == ycells:
                    new_cell = Gridcell(
                        grid_needle.y,
                        grid_needle.y - yrem,
                        grid_needle.x + cell_dim,
                        grid_needle.x,
                        sector
                    )
                elif (xcell + 1) == xcells and (ycell+1) == ycells:
                    new_cell = Gridcell(
                        grid_needle.y,
                        grid_needle.y - yrem,
                        grid_needle.x + xrem,
                        grid_needle.x,
                        sector
                    )
 
                if new_cell != None:
                    if poly.intersects(new_cell.as_polygon()):
                        _cells.append(new_cell)
        return Gridmap(_cells)  
