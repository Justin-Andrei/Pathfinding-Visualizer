from __future__ import annotations
from dataclasses import dataclass
from enum import StrEnum


class CellState(StrEnum):
    Unvisited = "Unvisited"
    Visited = "Visited"
    Start = "Start"
    Destination = "Destination"
    Wall = "Wall"
    currLocation = "CurrentLocation"
    Path = "Path"

class Cell:
    def __init__(self, row: int, col: int):
        self._row = row
        self._col = col
        self._state = CellState.Unvisited
        self._neighbors: list[Cell] = []

    def __repr__(self) -> str:
        return f"{self.row}:{self.col}"

    @property
    def row(self) -> int:
        return self._row

    @property
    def col(self) -> int:
        return self._col
    
    @property
    def state(self) -> CellState:
        return self._state
    
    def get_neighbors(self) -> list[Cell]:
        def check_valid(x: Cell) -> bool:
            if x.state == CellState.Wall:
                return False
            return True
        
        return list(filter(check_valid, self._neighbors))


    def add_neighbor(self, neighbor: Cell):
        self._neighbors.append(neighbor)

    def change_state(self, new_state: CellState):
        self._state = new_state


type Board = list[list[Cell]]

@dataclass(frozen=True)
class Result:
    search: list[Cell]
    path: list[Cell]
    is_solved: bool