from game_types import Cell, Board, Result, CellState
from typing import Protocol

class PathFinder(Protocol):
    def find_path(self, board: Board) -> Result:
        ...

class Model:
    def solve_board(self, board: Board, algorithm: str) -> Result:
        pathFinder: PathFinder | None = None
        match algorithm:
            case "DFS":
                pathFinder = DFS()
            case "BFS":
                pathFinder = BFS()
            case "BFS":
                pathFinder = Dijkstra()
            case "BFS":
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

        for row in board:
            for cell in row:
                if cell.state == CellState.Visited:
                    if cell == start:
                        cell.change_state(CellState.Start)
                    else:
                        cell.change_state(CellState.Unvisited)

        path.reverse()
        path.pop()

        return Result(visited, path, is_solved)

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
        print(cells_to_visit)
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

        for row in board:
            for cell in row:
                if cell.state == CellState.Visited:
                    if cell == start:
                        cell.change_state(CellState.Start)
                    else:
                        cell.change_state(CellState.Unvisited)

        return Result(visited, path, True)
        # else:
        #     # no solution
        #     ...
            
            
        

class Dijkstra:
    def find_path(self, board: Board) -> Result:
        ...

class Astar:
    def find_path(self, board: Board) -> Result:
        ...

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


test = BFS()

board = [[Cell(i, j) for j in range(5)] for i in range(5)]
board[0][0].change_state(CellState.Start)
board[4][4].change_state(CellState.Destination)
setup_neighbors(board)

print(test.find_path(board))