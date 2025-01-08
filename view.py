import pygame

from game_types import CellState, Cell, Setup, Result


class Constants:
    SCREEN_WIDTH = 1600
    SCREEN_HEIGHT = 900
    FPS = 60

    CELL_SIZE = 50

    FONT_SIZE = 20
    FONT_COLOR = "black"
    FONT = "Arial"


    BACKGROUND_COLOR = "gray"

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

        self._rect_x = self.col * Constants.CELL_SIZE + 1
        self._rect_y = self.row * Constants.CELL_SIZE + 1
        self.rect = pygame.Rect(self._rect_x, self._rect_y, Constants.CELL_SIZE, Constants.CELL_SIZE)

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
        self.rect.x = self._rect_x
        self.rect.y = self._rect_y
        color = self._get_color(self.cell.state)
        color_rect = pygame.Rect(self._rect_x, self._rect_y, Constants.CELL_SIZE - 1, Constants.CELL_SIZE - 1)
        pygame.draw.rect(surface, 'black', self.rect)
        pygame.draw.rect(surface, color, color_rect)

        
class Board:
    def __init__(self, row: int, col: int):
        self._row = row
        self._col = col
        self.board: list[list[ViewCell]] = self._create_blank_board()
        self._board_surface = self._create_board_surface()

    def _create_board_surface(self) -> pygame.Surface:
        surface_width = Constants.CELL_SIZE * self._col + 1
        surface_height = Constants.CELL_SIZE * self._row + 1
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

        for row in self.board:
            for view_cell in row:
                view_cell.draw(self._board_surface)
                view_cell.rect.x = view_cell.rect.x + board_surface_rect.x
                view_cell.rect.y = view_cell.rect.y + board_surface_rect.y
                pygame.draw.rect(surface, 'red', (view_cell.rect.x, view_cell.rect.y, 10, 10))
        
        surface.blit(self._board_surface, board_surface_rect)


class View:
    def __init__(self, row: int, col: int):
        pygame.init()

        self.row = row
        self.col = col
        self.board = Board(row, col)
        self._has_start = False
        self._has_dest = False
        self._solved = False

        self._font = pygame.font.SysFont(Constants.FONT, Constants.FONT_SIZE)
        self._button = self._create_button()

        self._screen = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
        self._clock = pygame.time.Clock()
        pygame.display.set_caption("Pathfinding Visualizer")

    def _create_button(self) -> tuple[pygame.Surface, pygame.Rect]:
        button_surface = pygame.Surface((100, 50))
        button_surface.fill('white')
        text = self._font.render("VISUALIZE", True, Constants.FONT_COLOR)
        text_rect = text.get_rect()
        text_rect.center = button_surface.get_rect().center
        button_surface.blit(text, text_rect)
        return (button_surface, button_surface.get_rect())

    def draw(self):
        self._screen.fill(Constants.BACKGROUND_COLOR)

        # draw board
        self.board.draw(self._screen)

        # draw enter button
        self._button[1].center = self._screen.get_rect().center
        self._button[1].y = 70
        self._screen.blit(self._button[0], self._button[1])


        # draw options button

        # draw instruction?

        # draw reset button
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    for i, row in enumerate(self.board.board):
                        for j, cell in enumerate(row):
                            if cell.rect.collidepoint(mouse_pos):
                                print(f"{i}:{j}")
                                # add a start cell
                                if not self._has_start and cell.cell.state != CellState.Destination:
                                    cell.cell.change_state(CellState.Start)
                                    self._has_start = True
                                # remove add start cell
                                elif self._has_start and cell.cell.state == CellState.Start:
                                    cell.cell.change_state(CellState.Unvisited)
                                    self._has_start = False
                                # add a destination
                                elif self._has_start and not self._has_dest and cell.cell.state != CellState.Start:
                                    cell.cell.change_state(CellState.Destination)
                                    self._has_dest = True
                                # remove destination
                                elif self._has_dest and cell.cell.state == CellState.Destination:
                                    cell.cell.change_state(CellState.Unvisited)
                                    self._has_dest = False

                    if self._button[1].collidepoint(mouse_pos):
                        print("VISUALIZE")
                        
            self.draw()
            self._clock.tick(Constants.FPS)



test = View(10, 10)
test.run()

