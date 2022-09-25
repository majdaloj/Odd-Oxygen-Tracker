"""
A class to hold the state of all of the variables used within the main pygame loop that change
and are needed in multiple functions. They all relate to userinput
"""
from typing import List
from graph import Graph


class UserinputGeneral:
    """
    Class to hold the current state of variables associated with
    user input -> general mouse and key inputs

    Instance Attributes:
        - mouse_held: True if the mouse is held
        - delete_held: True if the delete key is held
        - delete_buffer: the minimum amount of frames before a second delete input can be recieved
        - recently_scrolled: True if the mouse wheel was recently scrolled
        - scroll_y: The strength and direction by which the mouse wheel was recently scrolled
        - scroll_counter: A timer that determines how since a scroll was recently scrolled
    """
    mouse_held: bool
    delete_held: bool
    delete_buffer: int
    fade_buttons: bool
    recently_scrolled: bool
    scroll_y: int
    scroll_counter: int

    def __init__(self) -> None:
        self.mouse_held = False
        self.delete_held = False
        self.delete_buffer = 0
        self.fade_buttons = True
        self.recently_scrolled = False
        self.scroll_y = 0
        self.scroll_counter = 5


class Userinput(UserinputGeneral):
    """
    Class to hold the current state of variables associated with
    user input -> directly affect the graph

    Instance Attributes:
        - adjust_scale_x: True if slider to adjust the size of the graph in x dir is being moved
        - adjust_scale_y: True if slider to adjust the size of the graph in y dir is being moved
        - adjust_start_x: True if slider to adjust the starting x value of the graph being moved
        - list_of_graphs: The list of stored graphs
        - current_graph: which stored graph is being viewed if a stored graph is being viewed
        - preview_graph: True if you are viewing a graph that is not stored
        - adjust_end_x:True if slider to adjust the ending x value of the graph being moved
    """

    adjust_scale_x: bool
    adjust_scale_y: bool
    adjust_start_x: bool
    list_of_graphs: List[Graph]
    current_graph: int
    preview_graph: bool
    adjust_end_x: bool

    def __init__(self) -> None:
        UserinputGeneral.__init__(self)
        self.adjust_scale_y = False
        self.adjust_scale_x = False
        self.adjust_start_x = False
        self.list_of_graphs = []
        self.current_graph = 0
        self.preview_graph = True
        self.adjust_end_x = False


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['pygame', 'plotly.graph_objects',
                          'plotly.subplots', 'python_ta.contracts',
                          'graph', 'dataclass', 'user_input'],
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
