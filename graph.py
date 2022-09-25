"""
Class for a graph to be plotted with related functions
"""
from typing import List, Any, Tuple
import random
import datetime
import pygame
import plotly.graph_objects as go
pygame.init()

OFFSET_X_TEXT_Y = 5
OFFSET_Y_TEXT_X = 20
FONT = pygame.font.Font(None, 18)  # default font of size 12


class Graph:
    """
    A scatter-plot graph class that holds basic information for a graph

    Instance Attributes:
        - x_values: the list of all x-values associated with the graph
        - y_values: the list of all y-values associated with the graph
        - x_portion: the current portion of x-values being displayed/operated on
        - y_portion: the current portion of y-values being displayed/operated on
        - labels: stores label for the x and y axis
        - properties: stores graph title, colour, window it draws on (in that order), and type
        - x_pos: restriction of the domain such that for all x, x_pos[0] < x < x_pos[1]

    Representation Invariants:
        - len(x_values > 0)
        - len(x_values) == len(y_values)
        - len(labels[0]) > 0
        - len(labels[1]) > 0
        - len(properties[0]) > 0
        - all([0 <= properties[1][i] <= 255 for i in range(3)])
        - x_pos[0] < len(x_values) - 2
        - all([type(x) == int or type(x) == float for x in x_values])\
        or all([type(x) == datetime.time for x in x_values])
        - all([type(y) == int or type(y) == float for y in y_values])

    """
    x_values: List[Tuple[int, datetime.datetime]]
    y_values: List[Any]
    x_portion: List[Any]
    y_portion: List[Any]
    labels: List[str]
    properties: List[Any]
    x_pos: List[int]

    def __init__(self, window: pygame.Surface) -> None:
        """
        Initialize a blank graph with a random colour
        domain is equal to x_values by default
        """
        self.x_values = []
        self.y_values = []
        self.labels = ['', '']
        self.properties = ['', random_colour(), window, False]
        self.x_pos = [0, 0]

    def draw_graph(self, x_se: Tuple[float, float],
                   y_se: Tuple[float, float],
                   x_fe: Tuple[int, int]) -> None:
        """
        Draws the graph with a given domain, labels the graph and adds the scale

        x_se has x_start and x_end
            x_start is x_val of the bottom left pixel of the drawn graph
            x_end is x_val of the top right pixel of the drawn graph

        y_se has y_start and y_end
            y_start is y_val of the Top left pixel of the drawn graph
            y_end is y_val of the Bottom right pixel of the drawn graph

        x_fe has first_x and end_x
            these represent the restriction on the graph's domain

        Preconditions:
            - x_start + 20 < x_end
            - y_start + 20 < y_end
        """

        # Adjusts the graphs domain
        self.x_pos[0], self.x_pos[1] = x_fe
        self.x_portion = [self.x_values[x][0] for x in range(self.x_pos[0], self.x_pos[1])]
        self.y_portion = [self.y_values[y] for y in range(self.x_pos[0], self.x_pos[1])]

        x_max = max(self.x_portion)
        x_min = min(self.x_portion)
        y_max = max(self.y_portion)
        y_min = min(self.y_portion)

        # Gets the scale per pixel in each direction, i.e one pixel = + 10 to the y value
        # Adjusts the scale so that graph just fits within the edges
        x_scale = (x_max - x_min) / (x_se[1] - x_se[0])
        y_scale = (y_max - y_min) / (y_se[1] - y_se[0])
        points = []

        # If the scale is too small default is 1, (prevents dividing by 0)
        if x_scale == 0:
            x_scale = 1
        if y_scale == 0:
            y_scale = 1

        # Converts the x-values, y-values to pixel co-ordinates via the scale
        for i in range(0, len(self.x_portion)):
            vals = (self.x_portion[i], self.y_portion[i])

            x_co = int(vals[0] / x_scale) + x_se[0] - x_min / x_scale
            y_co = int((y_se[1] - vals[1]) / y_scale) + y_se[1] - (y_se[1] - y_min) / y_scale
            points.append([x_co, y_co])

        self.helper_draw_graph_scale(x_se, y_se, (x_min, x_max), (y_min, y_max))
        self.helper_draw_graph_items(x_se, y_se, points)
        # update display
        pygame.display.flip()

    def helper_draw_graph_scale(self, x_se: Tuple[float, float],
                                y_se: Tuple[float, float],
                                x_minmax: Tuple[float, float],
                                y_minmax: Tuple[float, float]) -> None:
        """
        This is a helper function to draw_graph to draw
        the scale
        """
        # Display the scale for the x-axis
        x_min, x_max = x_minmax
        y_min, y_max = y_minmax
        x_dis_scale_min = FONT.render(str(x_min), False, self.properties[1])
        x_dis_scale_max = FONT.render(str(x_max), False, self.properties[1])
        self.properties[2].blit(x_dis_scale_min, (x_se[0]
                                                  - int(x_dis_scale_min.get_rect().width / 2),
                                                  y_se[1] + OFFSET_X_TEXT_Y
                                                  - int(x_dis_scale_min.get_rect().height / 2)))
        self.properties[2].blit(x_dis_scale_max, (x_se[1]
                                                  - int(x_dis_scale_max.get_rect().width / 2),
                                                  y_se[1] + OFFSET_X_TEXT_Y
                                                  - int(x_dis_scale_max.get_rect().height / 2)))

        # Display the scale for the y-axis
        y_dis_scale_min = FONT.render(str(y_min), False, self.properties[1])
        y_dis_scale_max = FONT.render(str(y_max), False, self.properties[1])
        self.properties[2].blit(y_dis_scale_min, (x_se[0] - OFFSET_Y_TEXT_X / 2
                                                  - int(y_dis_scale_min.get_rect().width),
                                                  y_se[1]
                                                  - int(y_dis_scale_min.get_rect().height / 2)))
        self.properties[2].blit(y_dis_scale_max, (x_se[0] - OFFSET_Y_TEXT_X / 2
                                                  - int(y_dis_scale_max.get_rect().width),
                                                  y_se[0]))

    def helper_draw_graph_items(self, x_se: Tuple[float, float],
                                y_se: Tuple[float, float],
                                points: List[List[float]]) -> None:
        """
        This is a helper function to draw_graph,
        its purpose being to draw the text to the screen
        """
        # Draw the points
        pygame.draw.lines(self.properties[2], self.properties[1], False, points, 1)

        # Draw the axis
        pygame.draw.line(self.properties[2], self.properties[1],
                         (x_se[0], y_se[0]), (x_se[0], y_se[1]), 3)
        pygame.draw.line(self.properties[2], self.properties[1],
                         (x_se[0], y_se[1]), (x_se[1], y_se[1]), 3)

        # Display the x-axis label
        x_text = FONT.render(self.labels[0], False, self.properties[1])
        self.properties[2].blit(x_text,
                                (int((x_se[0] + x_se[1]) / 2) - int(x_text.get_rect().width / 2),
                                 y_se[1] + OFFSET_X_TEXT_Y + x_text.get_rect().height))

        # Display the y-axis label
        y_text = FONT.render(self.labels[1], False, self.properties[1])
        y_text = pygame.transform.rotate(y_text, -90)
        self.properties[2].blit(y_text, (x_se[0] - OFFSET_Y_TEXT_X,
                                         (int((y_se[0] + y_se[1]) / 2)
                                          - int(y_text.get_rect().height / 2))))

        # Display the title
        title_text = FONT.render(self.properties[0], False, self.properties[1])
        self.properties[2].blit(title_text, (int((x_se[0] + x_se[1]) / 2)
                                             - int(title_text.get_rect().width / 2),
                                             y_se[0] - OFFSET_X_TEXT_Y
                                             - title_text.get_rect().height))

    def draw_bar_v(self, fig: go.Figure) -> None:
        """This is a helper function to plot Odd Oxygen Graphs"""
        title = self.properties[0]
        x_loc = None
        x_text = ''
        if "1999" in title:
            x_loc = datetime.datetime(1999, 9, 14)
            x_text = 'CEPA'
        elif "2001" in title:
            x_loc = datetime.datetime(2001, 2, 13)
            x_text = 'FACVEF'
        elif "2010" in title:
            x_loc = datetime.datetime(2010, 6, 10)
            x_text = 'CEPAA'
        y_max = max(self.y_portion)
        fig.add_trace(go.Scatter(x=[x_loc, x_loc], y=[0, y_max],
                                 mode='lines+text',
                                 name=x_text,
                                 text=[x_text],
                                 textposition='bottom center',
                                 fillcolor='rgb(255,0,0)'))

    def draw_bar_h(self, fig: go.Figure) -> None:
        """This is a helper function to plot limits on O3"""
        x_port = [self.x_values[i][1] for i in self.x_portion]
        fig.add_trace(go.Scatter(x=[x_port[0], x_port[-1]], y=[80, 80],
                                 mode='lines+text',
                                 name='danger limit for O3',
                                 text=['80 ppb'],
                                 textposition='middle left',
                                 fillcolor='rgb(255,0,0)'))

    def generate_plotly(self) -> None:
        """
        Generates the plot-ly graph according to the graphs domain

        The generated graph will look the same as the one displayed on the screen
        To generate the graph click the upper-left-most white rectangle
        """
        fig = go.Figure()
        pollutant = self.properties[0].split()[0]
        if not self.properties[3]:
            fig.add_trace(go.Scatter(x=self.x_portion, y=self.y_portion,
                                     mode='lines+markers',
                                     name=self.properties[0]))
        else:
            new_x_portion = [self.x_values[i][1]
                             for i in self.x_portion]
            fig.add_trace(go.Scatter(x=new_x_portion, y=self.y_portion,
                                     mode='lines+markers',
                                     name=pollutant))

            if 'Ox' in self.properties[0]:
                self.draw_bar_v(fig)

            if 'O3' in self.properties[0]:
                self.draw_bar_h(fig)

        fig.update_layout(title=self.properties[0],
                          xaxis_title=self.labels[0],
                          yaxis_title=self.labels[1])
        fig.show()

    def plotly_with_reg(self, lin_reg: Tuple[float, float],
                        quad_reg: List[float],
                        exp_reg: List[float]) -> None:
        """
        This function uses plotly to plot the currently viewed graph and
        three regressions on top of it
        """
        fig = go.Figure()
        title = self.properties[0]

        # Actual Graph
        fig.add_trace(go.Scatter(x=self.x_portion, y=self.y_portion,
                                 mode='lines+markers',
                                 name=title))

        # Linear Reg
        (a, b) = lin_reg
        vals_y = [a + b * x for x in self.x_portion]
        fig.add_trace(go.Scatter(x=self.x_portion, y=vals_y,
                                 mode='lines+markers',
                                 name="Linear"))

        # Quad Reg
        c, b, a = quad_reg[0], quad_reg[1], quad_reg[2]
        vals_y = [a * (x ** 2) + b * x + c for x in self.x_portion]
        fig.add_trace(go.Scatter(x=self.x_portion, y=vals_y,
                                 mode='lines+markers',
                                 name="Quadratic"))

        # Exp Reg
        a, b = exp_reg[0], exp_reg[1]
        vals_y = [b * (a ** x) for x in self.x_portion]
        fig.add_trace(go.Scatter(x=self.x_portion, y=vals_y,
                                 mode='lines+markers',
                                 name="Exponential"))

        fig.update_layout(title=self.properties[0],
                          xaxis_title=self.labels[0],
                          yaxis_title=self.labels[1])
        fig.show()


def generate_random_graph(window: pygame.Surface) -> Graph:
    """
    Generates a random graph as a default value or an example

    window is where the graph is drawn to, should be the default window
    """

    x = []
    y = []
    # Generates a random number of random (x, y) values
    for i in range(0, int(random.uniform(30, 400))):
        x.append((i, i))
        y.append(random.randint(0, 300))

    # Filler values
    ran_graph = Graph(window)
    ran_graph.x_values = x
    ran_graph.y_values = y
    ran_graph.labels[0] = 'X LABEL'
    ran_graph.labels[1] = 'Y LABEL'
    ran_graph.properties[0] = 'RANDOM GRAPH (for fun)'

    return ran_graph


def random_colour() -> Tuple[int, int, int]:
    """This is a helper function to generate a random graph colour"""
    return (int(random.uniform(100, 255)),
            int(random.uniform(100, 255)),
            int(random.uniform(100, 255)))


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['pygame', 'plotly.graph_objects',
                          'plotly.subplots', 'python_ta.contracts',
                          'graph', 'dataclass', 'user_input', 'random',
                          'datetime'],
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
