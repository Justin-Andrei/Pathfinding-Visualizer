import pygame

from game_types import CellState, Cell, Setup, Result


class Constants:
    SCREEN_WIDTH = 1600
    SCREEN_HEIGHT = 900
    FPS = 60

    CELL_SIZE = 50

    FONT_SIZE = 20
    FONT_COLOR = "black"

    CELL_BORDER_COLOR = ""
    UNVISITED_COLOR = "white"
    VISITED_COLOR = "gray"
    START_COLOR = "green"
    DESTINATION_COLOR = "red"
    PATH_COLOR = "yellow"
    CURRENT_CELL_COLOR = "blue"
    WALL_COLOR = "black"
    

class ViewCell:
    def __init__(self, cell: Cell):
        self.cell = cell
        self.row = cell.row
        self.col = cell.col

        self._rect_x = self.col * Constants.CELL_SIZE
        self._rect_y = self.row * Constants.CELL_SIZE
        self._rect = pygame.Rect(self._rect_x, self._rect_y, Constants.CELL_SIZE, Constants.CELL_SIZE)

    def _get_color(self, state: CellState) -> str:
        color = {
            CellState.Unvisited: Constants.UNVISITED_COLOR,
            CellState.Visited: Constants.VISITED_COLOR,
            CellState.Start: Constants.START_COLOR,
            CellState.Destination: Constants.DESTINATION_COLOR,
            CellState.Path: Constants.PATH_COLOR,
            CellState.Wall: Constants.WALL_COLOR,
            CellState.currLocation: Constants.CURRENT_CELL_COLOR
        }
        return color[state]

    def draw(self, surface: pygame.Surface):
        color = self._get_color(self.cell.state)
        color_rect = pygame.Rect(self._rect_x, self._rect_y, Constants.CELL_SIZE - 1, Constants.CELL_SIZE - 1)
        pygame.draw.rect(surface, 'black', self._rect)
        pygame.draw.rect(surface, color, color_rect)
        # self._rect.x = self._rect.x + surface.get_rect().x
        # self._rect.y = self._rect.y + surface.get_rect().y
        

class Board:
    def __init__(self, row: int, col: int):
        self._row = row
        self._col = col
        self._board: list[list[ViewCell]] = self._create_blank_board()
        self._board_surface = self._create_board_surface()

    def _create_board_surface(self) -> pygame.Surface:
        surface_width = Constants.CELL_SIZE * self._col
        surface_height = Constants.CELL_SIZE * self._row
        return pygame.Surface((surface_width, surface_height))

    def _create_blank_board(self):
        board: list[list[ViewCell]] = []
        for i in range(self._row):
            row: list[ViewCell] = []
            for j in range(self._col):
                row.append(ViewCell(Cell(i,j)))
            board.append(row)
        return board
    
    def draw(self, surface: pygame.Surface):
        board_surface_rect = self._board_surface.get_rect()
        board_surface_rect.center = surface.get_rect().center

        for row in self._board:
            for view_cell in row:
                view_cell.draw(self._board_surface)
        
        surface.blit(self._board_surface, board_surface_rect)


class View:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
        self.board = Board(row, col)
        self._has_start = False
        self._has_dest = False
        self._solved = False

        self._screen = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
        self._clock = pygame.time.Clock()
        pygame.display.set_caption("Pathfinding Visualizer")


    def draw(self):
        # draw board
        self.board.draw(self._screen)

        # draw enter button

        # draw options button

        # draw instruction?

        # draw reset button

    def run(self):
        ...

