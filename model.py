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

        if not is_solved:
            raise ValueError("No valid path to destination or no destination")

        return Result(visited, path)

    def _dfs(self, board: Board, curr: Cell, visited: list[Cell], path: list[Cell]):
        visited.append(curr)
        print(f"I am {curr.row}: {curr.col}")
        print(f"neighbors: {curr.get_neighbors()}")
        print()
        if curr.state == CellState.Destination:
            print(f"Destination at {curr}")
            return True
        if curr.state == CellState.Visited:
            return False
        curr.change_state(CellState.Visited)
        neighbors = curr.get_neighbors()
        for neighbor in neighbors:
            found = self._dfs(board, neighbor, visited, path)
            if found:
                path.append(neighbor)
                return True
        return False



class BFS:
    def find_path(self, board: Board) -> Result:
        ...

class Dijkstra:
    def find_path(self, board: Board) -> Result:
        ...

class Astar:
    def find_path(self, board: Board) -> Result:
        ...

def setup_neighbors(board: Board):
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


boardTest = [[Cell(i, j) for j in range(10)] for i in range(10)]
setup_neighbors(boardTest)
boardTest[0][0].change_state(CellState.Start)
boardTest[9][9].change_state(CellState.Destination)

finder = DFS()
r = finder.find_path(boardTest)

print(r.search)
print()
for l in reversed(r.path):
    print(l)
# print(r.path)