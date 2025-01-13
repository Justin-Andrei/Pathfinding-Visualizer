from __future__ import annotations
from typing import Protocol
from math import inf, sqrt
from dataclasses import dataclass

from game_types import Cell, Board, Result, CellState

class PathFinder(Protocol):
    def find_path(self, board: Board) -> Result:
        ...

def reset_board_color(board: list[list[Cell]], start: Cell):
    for row in board:
        for cell in row:
            if cell.state == CellState.Visited:
                if cell == start:
                    cell.change_state(CellState.Start)
                else:
                    cell.change_state(CellState.Unvisited)

class Model:
    def solve_board(self, board: Board, algorithm: str) -> Result:
        pathFinder: PathFinder | None = None
        match algorithm:
            case "DFS":
                pathFinder = DFS()
            case "BFS":
                pathFinder = BFS()
            case "Dijkstra":
                pathFinder = Dijkstra()
            case "A-Star":
                pathFinder = Astar()
            case _:
                ...
        if pathFinder == None:
            raise ValueError(f"{algorithm} is not found")
        return pathFinder.find_path(board)


class DFS:
    def find_path(self, board: Board) -> Result:
        start: Cell | None = None
        for row in board:
            for cell in row:
                if cell.state == CellState.Start:
                    start = cell
        if start == None:
            raise ValueError("No starting cell")
        
        visited: list[Cell] = [] 
        path: list[Cell] = []

        is_solved = self._dfs(board, start, visited, path)

        reset_board_color(board, start)

        path.reverse()
        path.pop()

        return Result(visited, path, is_solved)

    # update to store parent node rather than prev node as path
    def _dfs(self, board: Board, curr: Cell, visited: list[Cell], path: list[Cell]):
        if curr.state == CellState.Destination:
            return True
        if curr.state == CellState.Visited:
            return False
        if curr.state == CellState.Unvisited:
            curr.change_state(CellState.Visited)
            visited.append(curr)
        neighbors = curr.get_neighbors()
        for neighbor in neighbors:
            found = self._dfs(board, neighbor, visited, path)
            if found:
                path.append(neighbor)
                return True
        return False

class BFS:
    def find_path(self, board: Board) -> Result:
        start: Cell | None = None
        for row in board:
            for cell in row:
                if cell.state == CellState.Start:
                    start = cell
        if start == None:
            raise ValueError("No starting cell")

        visited: list[Cell] = [] 
        path: list[Cell] = []

        cells_to_visit: list[Cell] = []
        cells_to_visit += start.get_neighbors()
        parent_node: dict[Cell, Cell] = {}
        for cell in start.get_neighbors():
            parent_node[cell] = start
        prev_cell: Cell = start
        # is_solved = False
        while len(cells_to_visit) != 0:
            curr_cell = cells_to_visit.pop(0)
            # print(curr_cell)
            if curr_cell.state == CellState.Destination:
                # is_solved = True
                prev_cell = curr_cell
                break
            if curr_cell.state == CellState.Visited:
                continue
            if curr_cell.state == CellState.Unvisited:
                curr_cell.change_state(CellState.Visited)
                visited.append(curr_cell)
                prev_cell = curr_cell
            cells_to_visit += curr_cell.get_neighbors()
            for cell in curr_cell.get_neighbors():
                if cell.state not in [CellState.Visited, CellState.Start]:
                    parent_node[cell] = curr_cell
        # if is_solved:
        curr_cell = prev_cell
        while curr_cell != start:
            path.append(curr_cell)
            curr_cell = parent_node[curr_cell]

        path.reverse()
        path.pop()

        reset_board_color(board, start)

        return Result(visited, path, True)
        # else:
        #     # no solution
        #     ...
            
            
@dataclass
class DijkstraCell:
    cell: Cell
    distance: float
    parent_node: DijkstraCell | None

class Dijkstra:
    # start cell
    # update distance of neighbors
    # select cell w/ shortest path
        # visit cell
        # update distance of neighbors
    # if destination is visited end
    def find_path(self, board: Board) -> Result:
        d_dict: dict[Cell, DijkstraCell] = {}
        d_board: list[list[DijkstraCell]] = []
        to_visit: list[DijkstraCell] = []

        start: DijkstraCell | None = None
        for row in board:
            d_row: list[DijkstraCell] = []
            for cell in row:
                if cell.state == CellState.Start:
                    d_cell = DijkstraCell(cell, 0, None)
                    start = d_cell
                else:
                    d_cell = DijkstraCell(cell, inf, None)
                    to_visit.append(d_cell)
                d_dict[cell] = d_cell
                d_row.append(d_cell)
            d_board.append(d_row)

        if start == None:
            raise ValueError("No starting cell")

        visited: list[Cell] = [] 
        path: list[Cell] = []

        path_start: DijkstraCell | None = None

        solved = False
        curr_cell = start
        for cell in curr_cell.cell.get_neighbors():
            d_cell = d_dict[cell]
            if d_cell.distance > curr_cell.distance + 1:
                d_cell.parent_node = curr_cell
                d_cell.distance = curr_cell.distance + 1
        while len(to_visit) != 0:
            curr_cell = self._get_shortest_distance_cell(to_visit)
            if curr_cell.cell.state == CellState.Destination:
                path_start = curr_cell
                solved = True
                break
            if curr_cell.cell.state == CellState.Unvisited:
                curr_cell.cell.change_state(CellState.Visited)
                visited.append(curr_cell.cell)
                for cell in curr_cell.cell.get_neighbors():
                    d_cell = d_dict[cell]
                    if d_cell.distance > curr_cell.distance + 1:
                        d_cell.parent_node = curr_cell
                        d_cell.distance = curr_cell.distance + 1
        
        if not solved:
            raise ValueError("MALI ")

        while path_start != start:
            if path_start != None:
                path_start = path_start.parent_node
                if path_start != None:
                    path.append(path_start.cell)

        path.pop()
        path.reverse()
        reset_board_color(board, start.cell)
        return Result(visited, path, solved)

    def _get_shortest_distance_cell(self, cell_list: list[DijkstraCell]) -> DijkstraCell:
        cell_list.sort(key=lambda cell: cell.distance)
        return cell_list.pop(0)


@dataclass
class AstarCell:
    cell: Cell
    distance: float
    heuristic: float
    parent_node: AstarCell | None


class Astar:
    def find_path(self, board: Board) -> Result:
        a_dict: dict[Cell, AstarCell] = {}
        a_board: list[list[AstarCell]] = []
        to_visit: list[AstarCell] = []

        start: AstarCell | None = None

        dest_location: tuple[int, int] | None = None

        found = False
        for row in board:
            for cell in row:
                if cell.state == CellState.Destination:
                    dest_location = (cell.row, cell.col)
                    found = True
                    break
            if found:
                break

        if dest_location == None:
            raise ValueError("No dest")

        for row in board:
            a_row: list[AstarCell] = []
            for cell in row:
                if cell.state == CellState.Start:
                    a_cell = AstarCell(cell, 0, self._get_heuristic((cell.row, cell.col), dest_location), None)
                    start = a_cell
                elif cell.state == CellState.Destination:
                    a_cell = AstarCell(cell, inf, 0, None)
                    to_visit.append(a_cell)
                else:
                    a_cell = AstarCell(cell, inf, self._get_heuristic((cell.row, cell.col), dest_location), None)
                    to_visit.append(a_cell)
                a_dict[cell] = a_cell
                a_row.append(a_cell)
            a_board.append(a_row)

        if start == None:
            raise ValueError("No starting cell")

        visited: list[Cell] = []
        path: list[Cell] = []

        path_start: AstarCell | None = None

        solved = False
        curr_cell = start
        for cell in curr_cell.cell.get_neighbors():
            a_cell = a_dict[cell]
            if a_cell.distance > curr_cell.distance + 1:
                a_cell.parent_node = curr_cell
                a_cell.distance = curr_cell.distance + 1
        while len(to_visit) != 0:
            curr_cell = self._get_shortest_distance_cell(to_visit)
            if curr_cell.cell.state == CellState.Destination:
                path_start = curr_cell
                solved = True
                break
            if curr_cell.cell.state == CellState.Unvisited:
                curr_cell.cell.change_state(CellState.Visited) 
                visited.append(curr_cell.cell)
                for cell in curr_cell.cell.get_neighbors():
                    a_cell = a_dict[cell]
                    if a_cell.distance > curr_cell.distance + 1:
                        a_cell.parent_node = curr_cell
                        a_cell.distance = curr_cell.distance + 1
        
        if not solved:
            raise ValueError("MALI")

        while path_start != start:
            if path_start != None:
                path_start = path_start.parent_node
                if path_start != None:
                    path.append(path_start.cell)

        path.pop()
        path.reverse()
        reset_board_color(board, start.cell)
        return Result(visited, path, solved)



    def _get_shortest_distance_cell(self, cell_list: list[AstarCell]) -> AstarCell:
        cell_list.sort(key=lambda cell: cell.distance + cell.heuristic)
        return cell_list.pop(0)

    def _get_heuristic(self, location: tuple[int, int], destination: tuple[int, int]) -> float:
        return sqrt((destination[0] - location[0])**2 + (destination[1] - location[1])**2)



def setup_neighbors(board: list[list[Cell]]):
    for i in range(len(board)):
        for j in range(len(board[0])):
            cell = board[i][j]
            if j < len(board[0]) - 1: # right
                cell.add_neighbor(board[i][j+1])
            if i > 0: # up
                cell.add_neighbor(board[i-1][j])
            if j > 0: # left
                cell.add_neighbor(board[i][j-1])
            if i < len(board) - 1: # down
                cell.add_neighbor(board[i+1][j])


# test = BFS()

# board = [[Cell(i, j) for j in range(5)] for i in range(5)]
# board[0][0].change_state(CellState.Start)
# board[4][4].change_state(CellState.Destination)
# setup_neighbors(board)

# print(test.find_path(board))