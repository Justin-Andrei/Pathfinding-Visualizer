import pygame

from game_types import CellState, Cell, Result
from model import Model


class Constants:
    SCREEN_WIDTH = 1600
    SCREEN_HEIGHT = 900
    FPS = 60

    CELL_SIZE = 30

    FONT_SIZE = 20
    FONT_COLOR = "black"
    FONT = "Arial"

    ANIMATION_DELAY = 1

    BACKGROUND_COLOR = "gray"

    CELL_BORDER_COLOR = ""
    UNVISITED_COLOR = "white"
    VISITED_COLOR = "gray"
    START_COLOR = "green"
    DESTINATION_COLOR = "red"
    PATH_COLOR = "yellow"
    CURRENT_CELL_COLOR = "blue"
    WALL_COLOR = "darkgoldenrod"
    
class ViewCell:
    def __init__(self, cell: Cell):
        self.cell = cell
        self.row = cell.row
        self.col = cell.col

        self._rect_x = self.col * Constants.CELL_SIZE
        self._rect_y = self.row * Constants.CELL_SIZE

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

    def draw(self, surface: pygame.Surface, init_x: int, init_y: int):
        color = self._get_color(self.cell.state)
        self.rect = pygame.Rect(init_x + self._rect_x, init_y + self._rect_y, Constants.CELL_SIZE, Constants.CELL_SIZE)
        color_rect = pygame.Rect(init_x + self._rect_x + 1, init_y + self._rect_y + 1, Constants.CELL_SIZE - 2, Constants.CELL_SIZE - 2)
        pygame.draw.rect(surface, 'black', self.rect)
        pygame.draw.rect(surface, color, color_rect)

class Board:
    def __init__(self, row: int, col: int):
        self._row = row
        self._col = col
        self.board = self._create_blank_board()
        self.board_rect = self._get_board_dimensions()
        self._setup_neighbors()

    def _create_blank_board(self) -> list[list[ViewCell]]:
        board: list[list[ViewCell]] = []
        for i in range(self._row):
            row: list[ViewCell] = []
            for j in range(self._col):
                row.append(ViewCell(Cell(i,j)))
            board.append(row)
        return board

    def _get_board_dimensions(self) -> pygame.Rect:
        width = self._col * Constants.CELL_SIZE
        height = self._row * Constants.CELL_SIZE
        return pygame.Rect(0, 0, width, height)
    
    def _setup_neighbors(self):
        board = self.board
        for i in range(len(board)):
            for j in range(len(board[0])):
                cell = board[i][j]
                if j < len(board[0]) - 1: # right
                    cell.cell.add_neighbor(board[i][j+1].cell)
                if i > 0: # up
                    cell.cell.add_neighbor(board[i-1][j].cell)
                if j > 0: # left
                    cell.cell.add_neighbor(board[i][j-1].cell)
                if i < len(board) - 1: # down
                    cell.cell.add_neighbor(board[i+1][j].cell)
    
    def draw(self, surface: pygame.Surface):
        self.board_rect.center = surface.get_rect().center
        self.board_rect.y = surface.get_rect().height - 20 - self.board_rect.height
        init_x, init_y = self.board_rect.x, self.board_rect.y

        for row in self.board:
            for view_cell in row:
                view_cell.draw(surface, init_x, init_y)

class Button:
    def __init__(self, font: pygame.Font, text: str, x: int, y: int):
        self._text = font.render(text, True, Constants.FONT_COLOR)
        self.rect = pygame.Rect(x, y, 100, 50)

    def draw(self, surface: pygame.Surface):
        text_rect = self._text.get_rect()
        text_rect.center = self.rect.center
        pygame.draw.rect(surface, 'white', self.rect)
        surface.blit(self._text, text_rect)

class View:
    def __init__(self, row: int, col: int):
        pygame.init()
        self._screen = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
        self._clock = pygame.time.Clock()
        pygame.display.set_caption("Pathfinding Visualizer")
        self._font = pygame.font.SysFont(Constants.FONT, Constants.FONT_SIZE)

        self.row = row
        self.col = col
        self.board = Board(row, col)
        self._has_start = False
        self._has_dest = False
        self._solved = False
        self._visualizing = False
        self.result: Result | None = None
        self.solver = Model()
        self._delay_counter = 0
        self._prev_cell: Cell | None = None

        self._start = Button(self._font, "VISUALIZE", 1000, 30)
        self._reset = Button(self._font, "RESET", 1000, 100)


    def draw(self):
        self._screen.fill(Constants.BACKGROUND_COLOR)

        # draw board
        self.board.draw(self._screen)

        # draw enter button
        self._start.draw(self._screen)

        # draw reset button
        self._reset.draw(self._screen)

        # draw options button

        # draw instruction?

        pygame.display.flip()

    def _next_animation(self):
        if self.result == None:
            return True
        if len(self.result.search) != 0:
            if self._prev_cell != None:
                self._prev_cell.change_state(CellState.Visited)
            curr_cell = self.result.search.pop(0)
            curr_cell.change_state(CellState.currLocation)
            self._prev_cell = curr_cell
            if len(self.result.search) == 0:
                curr_cell.change_state(CellState.Visited)
            return False
        elif len(self.result.path) != 0:
            curr_cell = self.result.path.pop(0)
            curr_cell.change_state(CellState.Path)
            return False
        return True


    def run(self):
        running = True
        while running:
            if self._visualizing:
                print(self._delay_counter)
                if self._delay_counter == 0:
                    is_done = self._next_animation()
                    if is_done:
                        self._visualizing = False
                    self._delay_counter += 1
                else:
                    if self._delay_counter == Constants.ANIMATION_DELAY:
                        self._delay_counter = 0
                        continue
                    self._delay_counter += 1

            keys = pygame.key.get_pressed()
            mouse_pressed = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

                if event.type == pygame.MOUSEBUTTONDOWN and not self._visualizing:

                    for row in self.board.board:
                        for cell in row:
                            if cell.rect.collidepoint(mouse_pos):
                                # # add a wall
                                # if keys[pygame.K_w]:
                                #     if cell.cell.state not in [CellState.Start, CellState.Destination]:
                                #         cell.cell.change_state(CellState.Wall)
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

                    if self._start.rect.collidepoint(mouse_pos) and self._has_dest and self._has_start and not self._solved:  
                        print("VISUALIZE")
                        self.result = self.solver.solve_board([[cell.cell for cell in row] for row in self.board.board], "Dijkstra")
                        if self.result.is_solved:
                            # start visualization
                            self._visualizing = True
                            self._prev_cell = None
                        else:
                            ...
                            # add message no path etc


                    if self._reset.rect.collidepoint(mouse_pos):
                        print("RESET")
                        self._has_dest = self._has_start = self._solved = False
                        for row in self.board.board:
                            for cell in row:
                                cell.cell.change_state(CellState.Unvisited)

            for row in self.board.board:
                for cell in row:
                    if mouse_pressed[0] and cell.rect.collidepoint(mouse_pos):
                        if keys[pygame.K_w]:
                            if cell.cell.state not in [CellState.Start, CellState.Destination]:
                                cell.cell.change_state(CellState.Wall)
                        else:
                            if cell.cell.state == CellState.Wall:
                                cell.cell.change_state(CellState.Unvisited)

            self.draw()
            self._clock.tick(Constants.FPS)



test = View(20, 50)
test.run()

