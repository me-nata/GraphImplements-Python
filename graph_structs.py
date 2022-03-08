from typing import NamedTuple


class Vertice:
    def __init__(self, label:str="No label", data=None, degree:int=0) -> None:
        self.label  = label
        self.data   = data
        self.degree = degree
        self._painted = 0

    def __str__(self) -> str:
        return f"('{self.label}', {self.data})"

    def altern_paint(self):
        self._painted = 1-self._painted

    def painted(self):
        return self._painted

class Edge:
    def __init__(self, label:str="No label", weight:float=1.0):
        self.label = label
        self.weight = weight

    def __str__(self):
        return f'(\'{self.label}\', w:{self.weight})'


class EdgeEntry(NamedTuple):
    i: int
    j: int
    e: Edge
