"""
A class to hold the state of all of the variables used within the main pygame loop that change
and are needed in multiple functions. They all relate to the GUI as in things drawn to the screen
"""
from typing import Tuple, List, Any
import pygame
import graph

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)


WIN_WIDTH = 800
WIN_HEIGHT = 800
X_OFFSET = 20
X_START = 20
X_END = WIN_WIDTH - 20
Y_OFFSET = 20
Y_START = 20
Y_END = int(WIN_HEIGHT / 2) - 20
# RECT_WIDTH = WIN_WIDTH - X_OFFSET * 2
X_MAX_OFFSET = (WIN_WIDTH - 100) / 2
X_MIN_OFFSET = 20  # LIMIT ON GRAPH WIDTH
Y_MIN_OFFSET = -int(WIN_HEIGHT / 2 - 100)
Y_MAX_OFFSET = int(WIN_HEIGHT - Y_OFFSET * 9 - WIN_HEIGHT / 2)


class Gui:
    """
    This is an abstract class to store GUI properties

    Instance Attributes:
        - win_height: window height
        - win_width: window width
        - add_rect_col: colour for the add graph button
        - left_rect_col: colour for the left grpah button
        - right_rect_col: colour for the right graph button
        - reg_rect_col: colour for the regression graph button
        - window: pygame surface window

    Preconditions:
        - win_height > 350 and win_width > 350
    """
    win_height: int
    win_width: int
    add_rect_col: Tuple[int, int, int]
    left_graph_col: Tuple[int, int, int]
    right_graph_col: Tuple[int, int, int]
    reg_graph_col: Tuple[int, int, int]
    window: pygame.Surface

    def __init__(self, win_height: int, win_width: int, window: pygame.Surface) -> None:
        self.win_height = win_height
        self.win_width = win_width
        self.add_rect_col = RED
        self.left_graph_col = GREEN
        self.right_graph_col = BLUE
        self.reg_graph_col = CYAN
        self.window = window


class GuiSetup(Gui):
    """This inherited class sets up the GUI for a graphing using
    the pygame pixel coordinate system

    Instance Attributes:
        - x_offset: how far the x-axis is in pixels from both the left/right sides of the window
        - y_offset: How far from the middle the y co of the bottom pixel of the graph is
        - x_start: X coordinate of the top left pixel of the drawn graph
        - y_start: Y coordinate of the top left pixel of the drawn graph
        - x_end: X coordinate of the bottom right pixel of the drawn graph
        - y_end: Y coordinate of the bottom right pixel of the drawn graph
        - x_width: width of x axis
        - y_width: width of y axis

    Preconditions:
        - X_START <= x_start
        - x_end <= X_END
        - Y_START <= y_start
        - y_end <= Y_END
        - X_MIN_OFFSET < x_offset < X_MAX_OFFSET
        - Y_MIN_OFFSET < self.win_height/2 < Y_MAX_OFFSET
        - x_width > 100
        - y_width > 100
    """
    x_offset: float
    y_offset: float
    x_start: float
    x_end: float
    y_end: float
    x_width: float
    y_width: float

    def __init__(self, win_height: int, win_width: int, window: pygame.Surface) -> None:
        Gui.__init__(self, win_height, win_width, window)

        # default values
        self.x_offset = 20
        self.y_offset = -20
        self.x_start = 20
        self.x_end = win_width - 20
        self.y_end = int(win_height / 2) - 20
        self.x_width = (self.x_end - X_START) / 2
        self.y_width = self.y_end - Y_START


class GuiSlider(GuiSetup):
    """This inherited class takes a setup GUI graph and initializes
    the sliders

    Instance Attributes:
        - xy_slid_pos: positions of the scale x and the scale y slider circle -as in x val in pixels
        - x_start_slid_minmax: min and max values of starting x value
        - x_se_slid_pos: positions of the start_x and end_x slider circles (as in x_value in pixels)
        - x_end_slid_minmax: min and max values of ending x value
        - x_se_graph: The restriction on the domain of the graph, the starting and ending value
        - graph_ex: Holds a graph if it has not been added to the stored graphs list
        - slide_rad: radius of the slider circles

    Preconditions:
        - X_START <= xy_slid_pos[0] <= X_END
        - X_START <= xy_slid_pos[1] <= X_END
        - 0 <= x_start_slid_minmax[0] and x_start_slid_minmax[0] <= x_start_slid_minmax[1] - 2
        - X_START <= x_se_slid_pos[0] <= X_END
        - X_START <= x_se_slid_pos[1] <= X_END
        - slide_rad > 0
    """

    xy_slid_pos: List[float]
    x_start_slid_minmax: List[int]
    x_se_slid_pos: List[float]
    x_end_slid_minmax: List[int]
    x_se_graph: List[Any]
    graph_ex: graph.Graph
    slid_rad: int

    def __init__(self, win_height: int, win_width: int,
                 window: pygame.Surface) -> None:
        GuiSetup.__init__(self, win_height, win_width, window)

        # Default values
        y_max_offset = int(win_height - Y_OFFSET * 9 - win_height / 2)
        y_min_offset = -int(win_height / 2 - 100)
        rect_width = win_width - X_OFFSET * 2
        self.slid_rad = 5
        self.xy_slid_pos = [0.0, 0.0]
        self.xy_slid_pos[0] = (self.x_offset - X_MIN_OFFSET) * rect_width / \
                              ((win_width - 100) / 2 - X_MIN_OFFSET) + X_OFFSET
        self.xy_slid_pos[1] = (self.y_offset - y_min_offset) * rect_width / \
                              (y_max_offset - y_min_offset) + X_OFFSET

        self.graph_ex = graph_ex = graph.generate_random_graph(window)

        self.x_start_slid_minmax = [0.0, 0.0]
        self.x_start_slid_minmax[1] = len(graph_ex.x_values)
        self.x_start_slid_minmax[0] = 2

        self.x_se_graph = [0.0, 0.0]
        self.x_se_graph[0] = 0
        self.x_se_graph[1] = len(graph_ex.x_values)

        self.x_end_slid_minmax = [0.0, 0.0]
        self.x_end_slid_minmax[1] = len(graph_ex.x_values)
        self.x_end_slid_minmax[0] = 0

        self.x_se_slid_pos = [0.0, 0.0]
        denom_start = (self.x_start_slid_minmax[1] - self.x_start_slid_minmax[0])
        self.x_se_slid_pos[0] = X_OFFSET + self.x_se_graph[0] / denom_start * rect_width
        denom_end = (self.x_start_slid_minmax[1] - (self.x_start_slid_minmax[0] - 2))
        self.x_se_slid_pos[1] = X_OFFSET + self.x_se_graph[1] / denom_end * rect_width


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['pygame', 'plotly.graph_objects',
                          'plotly.subplots', 'python_ta.contracts',
                          'graph', 'dataclass', 'user_input', 'random'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200'],
        'generated-members': ['pygame.*']
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod(verbose=True)
