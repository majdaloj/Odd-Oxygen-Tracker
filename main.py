"""
Main file, runs the main pygame loop and stores all of the helper functions for handling user
interaction with the program

Also display the results of the computations

User interaction:
    - Scaling the graphs
    - Restriction the domain
    - Storing graphs and switching between them
    - selecting which graph to view
    - plotting graphs on plotly
    - plotting multiple graphs on the same axis
    - Display the results of computations
"""
from typing import List
import pygame
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import graph
import graphics_UI
import user_input
import generated_graphs
import compute

# **Constants** #

WIN_WIDTH = int(input('Enter the window width anything greater than 350: '))  # Window Width
WIN_HEIGHT = int(input('Enter the window height anything greater than 350: '))  # Window Height
FONT = pygame.font.Font(None, 16)  # Font used for buttons default is 12
FONT_TYPE = pygame.font.Font(None, 16)  # Font used for user input, default font of size 16
FONT_BUTTON = pygame.font.Font(None, 25)  # Font for graph labels

X_OFFSET = 20  # How many pixels (x) objects are from the edges of the screen, i.e large buttons
X_START = 20  # Default amount of pixels (x) that a displayed graph is from the edge of the screen
X_END = WIN_WIDTH - 20  # Default pixel that the displayed graph ends at (x)
Y_OFFSET = 20  # Default spacing between objects i.e sliders in the Y-dir
Y_START = 20  # The first pixel of a displayed graph in the y-dir (y) coord
Y_END = int(WIN_HEIGHT / 2) - 20  # The last pixel of a displayed graph in the y-dir
RECT_WIDTH = WIN_WIDTH - X_OFFSET * 2  # The default width for a large rectangle
SLIDER_HEIGHT = 3  # The default height for a slider bar

# Rectangle at the bottom of screen, lets you choose what graph to display, i.e from file
CHOOSE_DATA_RECT = pygame.Rect(X_OFFSET, int(WIN_HEIGHT) - Y_OFFSET * 2,
                               RECT_WIDTH, int(Y_OFFSET * 1.5))

# Y coordinate of the start of the scale x rect
SCALE_X_RECT_Y_S = int(WIN_HEIGHT) - Y_OFFSET * 3
# Y coordinate of the end of the scale x rect
SCALE_X_RECT_Y_E = int(WIN_HEIGHT - Y_OFFSET * 2.5)
# Y coordinate of the start of the scale y rect
SCALE_Y_RECT_Y_S = int(WIN_HEIGHT) - Y_OFFSET * 4
# Y coordinate of the end of the scale y rect
SCALE_Y_RECT_Y_E = int(WIN_HEIGHT - Y_OFFSET * 3.5)
# Y coordinate of the start of the plotly rectangles
PLOTLY_RECT_Y_S = int(WIN_HEIGHT) - Y_OFFSET * 7
# Y coordinate of the end of the plotly rectangles
PLOTLY_RECT_Y_E = int(WIN_HEIGHT - Y_OFFSET * 6)
# Y coordinate of the start of the start x slider
X_START_RECT_S = int(WIN_HEIGHT) - Y_OFFSET * 5
# Y coordinate of the end of the start x slider
X_START_RECT_Y_E = int(WIN_HEIGHT) - Y_OFFSET * 4.5
# Y coordinate of the start of any of the store graph buttons
EDIT_RECT_Y_S = int(WIN_HEIGHT - Y_OFFSET * 6)
# Y coordinate of the end of any of the store graph buttons
EDIT_RECT_Y_E = int(WIN_HEIGHT - Y_OFFSET * 5.5)

# X slider rectangle
SCALE_X_RECT = pygame.Rect(X_OFFSET, SCALE_X_RECT_Y_S, RECT_WIDTH, SLIDER_HEIGHT)
# Y slider rectangle
SCALE_Y_RECT = pygame.Rect(X_OFFSET, SCALE_Y_RECT_Y_S, RECT_WIDTH, SLIDER_HEIGHT)
# X restriction rectangle
X_START_SLID = pygame.Rect(X_OFFSET, X_START_RECT_S, RECT_WIDTH, SLIDER_HEIGHT)
# Create plotly of current graph rectangle
CREATE_PLOTLY_RECT = pygame.Rect(X_OFFSET, PLOTLY_RECT_Y_S, RECT_WIDTH / 2, SLIDER_HEIGHT * 5)
# Create plotly of all stored graphs rectangle
CREATE_PLOTLY_ALL_RECT = pygame.Rect(X_OFFSET + RECT_WIDTH / 2, PLOTLY_RECT_Y_S, RECT_WIDTH / 2,
                                     SLIDER_HEIGHT * 5)
# Store a graph rectangle
ADD_GRAPH_RECT = pygame.Rect(X_OFFSET, EDIT_RECT_Y_S, RECT_WIDTH / 4, SLIDER_HEIGHT * 5)

# Move left in stored graphs
LEFT_RECT = pygame.Rect(X_OFFSET + RECT_WIDTH / 4, EDIT_RECT_Y_S, RECT_WIDTH / 4,
                        SLIDER_HEIGHT * 5)
# Move Right in stored graphs
RIGHT_RECT = pygame.Rect(X_OFFSET + RECT_WIDTH / 2, EDIT_RECT_Y_S, RECT_WIDTH / 4,
                         SLIDER_HEIGHT * 5)
REG_RECT = pygame.Rect(X_OFFSET + RECT_WIDTH * 3 / 4, EDIT_RECT_Y_S, RECT_WIDTH / 4,
                       SLIDER_HEIGHT * 5)
# Tuples for certain colours
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)

X_MAX = WIN_WIDTH / 2 - X_OFFSET  # NOT USED FOR ANYTHING GET RID OF THIS CONSTANT
# The maximum x off-set (When x-offset = x_max_offset the graph is at it's smallest in x-dir)
X_MAX_OFFSET = (WIN_WIDTH - 100) / 2
# The minimum x off-set (When x-offset = x_min_offset the graph is at it's biggest in x-dir)
X_MIN_OFFSET = 20
# The minimum y off-set (When y-offset = y_min_offset the graph is at it's biggest in y-dir)
Y_MIN_OFFSET = -int(WIN_HEIGHT / 2 - 100)
# The maximum y off-set (When y-offset = y_max_offset the graph is at it's smallest in y-dir)
Y_MAX_OFFSET = int(WIN_HEIGHT - Y_OFFSET * 9 - WIN_HEIGHT / 2)


def plotly_all(graphs: List[graph.Graph], title: str, xaxis_title: str) -> None:
    """
    Plots all of the graphs in the list
    """
    fig = make_subplots(rows=len(graphs), cols=1)

    for graph_i in range(1, len(graphs) + 1):
        if not graphs[graph_i - 1].properties[3]:
            fig.add_trace(go.Scatter(x=graphs[graph_i - 1].x_portion,
                                     y=graphs[graph_i - 1].y_portion,
                                     name=graphs[graph_i - 1].properties[0]),
                          row=graph_i, col=1)
        else:
            new_x_portion = [graphs[graph_i - 1].x_values[i][1]
                             for i in graphs[graph_i - 1].x_portion]
            fig.add_trace(go.Scatter(x=new_x_portion, y=graphs[graph_i - 1].y_portion,
                                     name=graphs[graph_i - 1].properties[0]),
                          row=graph_i, col=1)

    fig.update_layout(title=title, xaxis_title=xaxis_title)
    fig.show()


def handle_x_slid(u_input: user_input.Userinput) -> None:
    """Allow the graph's domain to be restricted
    Called when the user presses on the x_start circle

    * u_input has been initialized correctly *
    """
    u_input.adjust_scale_x = True


def handle_y_slid(u_input: user_input.Userinput) -> None:
    """
    Allow the graph to be scaled in the y-direction
    Called when the user presses on the y-slider circle

    * u_input has been initialized correctly *
    """
    u_input.adjust_scale_y = True


def handle_add_graph(window: pygame.surface, u_input: user_input.Userinput,
                     gui: graphics_UI.GuiSlider) -> None:
    """
    Store the current previewed graph into a list of graphs.
    Any of the stored graphs can be viewed by clicking the blue/green buttons
    they can be graphed simultaneously
    Additionally fade the button when pressed to indicate that its been pressed

    Preconditions:
        - window.width > 350
        - window.height > 350

    * gui has been initialized correctly *
    * u_input has been initialized correctly *
    """
    # adds the graph
    if gui.graph_ex not in u_input.list_of_graphs:
        u_input.list_of_graphs.append(gui.graph_ex)
        u_input.current_graph = len(u_input.list_of_graphs) - 1

    # fade the pressed button
    gui.add_rect_col = (255, 255, 255)
    pygame.draw.rect(window, gui.add_rect_col, ADD_GRAPH_RECT)
    u_input.fade_buttons = True


def handle_left_graph(window: pygame.surface, u_input: user_input.Userinput,
                      gui: graphics_UI.GuiSlider) -> None:
    """
    Move left in the stored graphs and update the display. The display is updated to match what the
    display was of the stored graphed last time it was on screen.
    update the displayed graph's settings:
    - update the start_x slider
    - update the end_x slider
    - Tell the program to draw the stored graph (preview_graph = False)
    Additionally fade the button when pressed to indicate that its been pressed

    * Only redraw the start_x and end_x slider,
    update the parameters for graph to display but do not redraw the graph that is
    done in handle_update_display() *

    Preconditions:
        - window.width > 350
        - window.height > 350

    * gui has been initialized correctly *
    * u_input has been initialized correctly *
    """
    # moves left in stored graphs
    if u_input.current_graph > 0 or len(u_input.list_of_graphs) == 1:

        # update the parameters for the drawn graph and x_slider and indicate to draw it
        if len(u_input.list_of_graphs) == 1:
            u_input.current_graph = 0
        else:
            u_input.current_graph -= 1

        u_input.preview_graph = False

        # Update the start_x and end_x positions respectively
        gui.x_se_graph[0] = u_input.list_of_graphs[u_input.current_graph].x_pos[0]

        gui.x_se_graph[1] = u_input.list_of_graphs[u_input.current_graph].x_pos[1]
        denom_start = (len(u_input.list_of_graphs[u_input.current_graph].x_values)
                       - gui.x_start_slid_minmax[0])

        # Update the start_x and end_x slider positions respectively
        gui.x_se_slid_pos[0] = X_OFFSET + gui.x_se_graph[0] / denom_start * RECT_WIDTH
        denom_end = (len(u_input.list_of_graphs[u_input.current_graph].x_values)
                     - gui.x_end_slid_minmax[0])
        gui.x_se_slid_pos[1] = X_OFFSET + gui.x_se_graph[1] / denom_end * RECT_WIDTH

        # Re draw slider
        pygame.draw.rect(window, (0, 0, 0), pygame.Rect(0, int(
            int(WIN_HEIGHT) - Y_OFFSET * 5) - gui.slid_rad / 2, WIN_WIDTH, 10))
        pygame.draw.rect(window, (255, 255, 255), X_START_SLID)

        pygame.draw.circle(window, (255, 255, 255), (gui.x_se_slid_pos[0], int(
            int(WIN_HEIGHT) - Y_OFFSET * 5 + gui.slid_rad / 2)), gui.slid_rad)
        pygame.draw.circle(window, (255, 255, 255), (gui.x_se_slid_pos[1], int(
            X_START_RECT_S + gui.slid_rad / 2)), gui.slid_rad)

    # fade the pressed button
    gui.left_graph_col = (255, 255, 255)
    pygame.draw.rect(window, gui.left_graph_col, LEFT_RECT)
    u_input.fade_buttons = True


def handle_right_graph(window: pygame.surface, u_input: user_input.Userinput,
                       gui: graphics_UI.GuiSlider) -> None:
    """
    Move right in the stored graphs and update the display. The display is updated to match what the
    display was of the stored graphed last time it was on screen.
    update the displayed graph's settings:
    - update the start_x slider
    - update the end_x slider
    - Tell the program to draw the stored graph (Preview_graph = False)
    Additionally fade the button when pressed to indicate that its been pressed

    * Only redraw the start_x and end_x slider,
    update the parameters for graph to display but do not redraw the graph that is
    done in handle_update_display() *

    Preconditions:
        - window.width > 350
        - window.height > 350

    * gui has been initialized correctly *
    * u_input has been initialized correctly
    """
    # move right in stored graphs
    if u_input.current_graph < len(u_input.list_of_graphs) - 1 or len(u_input.list_of_graphs) == 1:

        # update the parameters for the drawn graph and x_slider and indicate to draw it
        if len(u_input.list_of_graphs) == 1:
            u_input.current_graph = 0
        else:
            u_input.current_graph += 1
        u_input.preview_graph = False

        # Update the start_x and end_x positions respectively
        gui.x_se_graph[0] = u_input.list_of_graphs[u_input.current_graph].x_pos[0]
        gui.x_se_graph[1] = u_input.list_of_graphs[u_input.current_graph].x_pos[1]

        denom_start = (len(u_input.list_of_graphs[u_input.current_graph].x_values)
                       - gui.x_start_slid_minmax[0])

        # Update the start_x and end_x slider positions respectively
        gui.x_se_slid_pos[0] = X_OFFSET + gui.x_se_graph[0] / denom_start * RECT_WIDTH

        denom_end = (len(u_input.list_of_graphs[u_input.current_graph].x_values)
                     - gui.x_end_slid_minmax[0])
        gui.x_se_slid_pos[1] = X_OFFSET + gui.x_se_graph[1] / denom_end * RECT_WIDTH

        # Re draw slider
        pygame.draw.rect(window, (0, 0, 0), pygame.Rect(0, int(
            int(WIN_HEIGHT) - Y_OFFSET * 5) - gui.slid_rad / 2, WIN_WIDTH, 10))
        pygame.draw.rect(window, (255, 255, 255), X_START_SLID)

        pygame.draw.circle(window, (255, 255, 255), (gui.x_se_slid_pos[0], int(
            int(WIN_HEIGHT) - Y_OFFSET * 5 + gui.slid_rad / 2)), gui.slid_rad)
        pygame.draw.circle(window, (255, 255, 255), (gui.x_se_slid_pos[1], int(
            X_START_RECT_S + gui.slid_rad / 2)), gui.slid_rad)

    # fade the pressed button
    gui.right_graph_col = (255, 255, 255)
    pygame.draw.rect(window, gui.right_graph_col, RIGHT_RECT)
    u_input.fade_buttons = True


def handle_reg_graph(window: pygame.surface, u_input: user_input.Userinput,
                     gui: graphics_UI.GuiSlider) -> None:
    """ This handles the event of computing the best regression on a graph
    It plots linear, polynomial, and exponential regressions """

    # fade the pressed button
    gui.reg_graph_col = (255, 255, 255)
    pygame.draw.rect(window, gui.reg_graph_col, REG_RECT)
    u_input.fade_buttons = True

    graph_r = u_input.list_of_graphs[u_input.current_graph]

    lin_reg = compute.simple_linear_regression((graph_r.x_portion, graph_r.y_portion))
    quad_reg = compute.polynomial_regression(2, graph_r.x_portion, graph_r.y_portion)
    exp_reg = compute.exponential_regression(graph_r.x_portion, graph_r.y_portion)

    graph_r.plotly_with_reg(lin_reg, quad_reg, exp_reg)


def handle_plotly_all(u_input: user_input.Userinput) -> None:
    """
    Graph all of the stored graphs in plotly in one window
    Called when the user presses on the pink rectangle

    * u_input has been initialized correctly *
    """
    plotly_all(u_input.list_of_graphs, 'All Plots', ' ')


def handle_plotly(u_input: user_input.Userinput, gui: graphics_UI.GuiSlider) -> None:
    """
    generate the plotly for the currently viewed graph
    Called when the user presses on the upper left most whit rectangle

    * u_input has been initialized correctly *
    """

    # Different calls depending on if the graph has been stored or not
    if u_input.preview_graph:
        gui.graph_ex.generate_plotly()
    else:
        u_input.list_of_graphs[u_input.current_graph].generate_plotly()


def handle_start_x(u_input: user_input) -> None:
    """
    Allow the graph to be scaled in the x-direction
    Called when the user presses on the x-slider circle

    * u_input has been initialized correctly *
    """
    u_input.adjust_start_x = True


def handle_end_x(u_input: user_input) -> None:
    """
    Allow the graph to be scaled in the x-direction
    Called when the user presses on the x-slider circle

    * u_input has been initialized correctly *
    """
    u_input.adjust_end_x = True


def add_new_graph(window: pygame.Surface, gui: graphics_UI.GuiSlider,
                  u_input: user_input.Userinput,
                  graph_in: graph.Graph) -> None:
    """
    Set the current graph being viewed to a random graph
    Done by clicking the white rectangle at the bottom of the screen

    * Used for demonstrating functionality *

    Preconditions:
        - window.width > 350
        - window.height > 350

    * gui has been initialized correctly *
    * u_input has been initialized correctly *
    """

    # Generate the random graph and adjust the x_start slider position
    # gui.graph_ex = graph.generate_random_graph(window)
    gui.graph_ex = graph_in
    gui.graph_ex.draw_graph((gui.x_start, gui.x_end), (Y_START, gui.y_end),
                            (0, len(gui.graph_ex.x_values)))
    gui.x_se_graph[0] = 0
    gui.x_se_graph[1] = len(gui.graph_ex.x_values)
    u_input.preview_graph = True
    denom_start = (len(gui.graph_ex.x_values) - gui.x_start_slid_minmax[0])
    gui.x_se_slid_pos[0] = X_OFFSET + gui.x_se_graph[0] / denom_start * RECT_WIDTH
    denom_end = (len(gui.graph_ex.x_values) - gui.x_end_slid_minmax[0])
    gui.x_se_slid_pos[1] = X_OFFSET + gui.x_se_graph[1] / denom_end * RECT_WIDTH
    # Redraw the x_start slider
    pygame.draw.rect(window, (0, 0, 0), pygame.Rect(0, int(
        int(WIN_HEIGHT) - Y_OFFSET * 5) - gui.slid_rad / 2, WIN_WIDTH, 10))

    pygame.draw.rect(window, (255, 255, 255), X_START_SLID)

    pygame.draw.circle(window, (255, 255, 255), (gui.x_se_slid_pos[0], int(
        int(WIN_HEIGHT) - Y_OFFSET * 5 + gui.slid_rad / 2)), gui.slid_rad)

    pygame.draw.circle(window, (255, 255, 255), (gui.x_se_slid_pos[1], int(
        int(WIN_HEIGHT) - Y_OFFSET * 5 + gui.slid_rad / 2)), gui.slid_rad)


def handle_mouse_press(window: pygame.Surface, mouse_x: int, mouse_y: int, gui: graphics_UI.GuiSlider,
                       u_input: user_input.Userinput) -> None:
    """
    Preform the correct action when the mouse is pressed depending on where the mouse was
    pressed

    Preconditions:
        - window.width > 350
        - window.height > 350

    * gui has been initialized correctly *
    * u_input has been initialized correctly *
    """

    # allows mouse held actions
    u_input.mouse_held = True

    if X_OFFSET <= pygame.mouse.get_pos()[0] <= WIN_WIDTH - X_OFFSET:

        if SCALE_X_RECT_Y_S <= mouse_y <= SCALE_X_RECT_Y_E \
                and gui.xy_slid_pos[0] - gui.slid_rad <= mouse_x <= gui.xy_slid_pos[0] + \
                gui.slid_rad:
            handle_x_slid(u_input)  # adjust size of the graph in the x direction
        elif SCALE_Y_RECT_Y_S <= mouse_y <= SCALE_Y_RECT_Y_E \
                and gui.xy_slid_pos[1] - gui.slid_rad <= mouse_x <= gui.xy_slid_pos[1] + \
                gui.slid_rad:
            handle_y_slid(u_input)  # adjust size of the graph in the y direction
        elif X_START_RECT_S <= mouse_y <= X_START_RECT_Y_E \
                and gui.x_se_slid_pos[0] - gui.slid_rad <= mouse_x <= gui.x_se_slid_pos[0] \
                + gui.slid_rad:
            handle_start_x(u_input)  # adjust restriction on graph's domain
        elif X_START_RECT_S <= mouse_y <= X_START_RECT_Y_E \
                and gui.x_se_slid_pos[1] - gui.slid_rad <= mouse_x <= gui.x_se_slid_pos[1] \
                + gui.slid_rad:
            handle_end_x(u_input)  # adjust restriction on graph's domain
        elif PLOTLY_RECT_Y_S <= mouse_y <= PLOTLY_RECT_Y_E \
                and X_OFFSET <= mouse_x <= X_OFFSET + RECT_WIDTH / 2:
            handle_plotly(u_input, gui)  # Draw the plotly for the current graph
        elif PLOTLY_RECT_Y_S <= mouse_y <= PLOTLY_RECT_Y_E \
                and X_OFFSET + RECT_WIDTH / 2 <= mouse_x <= X_OFFSET + RECT_WIDTH:
            handle_plotly_all(u_input)  # Draw all stored graph's plotly graph
        elif EDIT_RECT_Y_S <= mouse_y <= EDIT_RECT_Y_E \
                and X_OFFSET <= mouse_x <= X_OFFSET + RECT_WIDTH / 4:
            handle_add_graph(window, u_input, gui)  # store a graph
        elif EDIT_RECT_Y_S <= mouse_y <= EDIT_RECT_Y_E \
                and X_OFFSET + RECT_WIDTH / 4 <= mouse_x <= X_OFFSET + RECT_WIDTH / 2:
            handle_left_graph(window, u_input, gui)  # go left in the stored graphs
        elif EDIT_RECT_Y_S <= mouse_y <= EDIT_RECT_Y_E \
                and X_OFFSET + RECT_WIDTH / 2 <= mouse_x <= X_OFFSET + 3 * RECT_WIDTH / 4:
            handle_right_graph(window, u_input, gui)  # go right in the stored graphs
        elif EDIT_RECT_Y_S <= mouse_y <= EDIT_RECT_Y_E \
                and X_OFFSET + RECT_WIDTH * 3 / 4 <= mouse_x <= X_OFFSET + RECT_WIDTH:
            handle_reg_graph(window, u_input, gui)  # run the regressions
        elif int(WIN_HEIGHT) - Y_OFFSET * 2 <= pygame.mouse.get_pos()[1] <= int(WIN_HEIGHT):
            add_new_graph(window, gui, u_input, graph.generate_random_graph(window))


def handle_mouse_up(u_input: user_input.Userinput) -> None:
    """
    Stop any action that is done by holding down the mouse when the mouse button is raised

    * u_input has been initialized correctly *
    """
    u_input.mouse_held = False
    u_input.adjust_scale_x = False
    u_input.adjust_scale_y = False
    u_input.adjust_start_x = False
    u_input.adjust_end_x = False


def handle_mouse_held(window: pygame.Surface, u_input: user_input.Userinput, mouse_x: float,
                      gui: graphics_UI.GuiSlider) -> None:
    """
    Preform an action that is done by holding down the mouse, i.e moving a slider,
    depending on where the user initially clicked when the mouse button is held

    Preconditions:
        - window.width > 350
        - window.height > 350

    * gui has been initialized correctly *
    * u_input has been initialized correctly *
    """

    if u_input.adjust_scale_x:
        handle_adjust_scale_x(window, gui, mouse_x)
    if u_input.adjust_scale_y:
        handle_adjust_scale_y(window, gui, mouse_x)
    if u_input.adjust_start_x:
        handle_adjust_start_x(window, gui, u_input, mouse_x)
    if u_input.adjust_end_x:
        handle_adjust_end_x(window, gui, u_input, mouse_x)


def handle_fade_buttons(window: pygame.Surface, gui: graphics_UI.GuiSlider,
                        u_input: user_input.Userinput) -> None:
    """
    Fade any of the three RGB buttons after they're pressed
    * To indicate if you clicked them *

    Render button labels and paste them overtop the fading buttons

    Preconditions:
        - window.width > 350
        - window.height > 350

    * gui has been initialized correctly *
    * u_input has been initialized correctly *
    """
    # fade the red button
    if gui.add_rect_col != RED:
        gui.add_rect_col = (gui.add_rect_col[0], gui.add_rect_col[1] - 3, gui.add_rect_col[2] - 3)
        pygame.draw.rect(window, gui.add_rect_col, ADD_GRAPH_RECT)

        # Re render the button label
        add_button_label = FONT.render('Store graph', True, (0, 0, 0))

        window.blit(add_button_label, (X_OFFSET + 1 * RECT_WIDTH / 8
                                       - int(add_button_label.get_rect().width / 2),
                                       (int(EDIT_RECT_Y_E + EDIT_RECT_Y_S) / 2)
                                       - int(add_button_label.get_rect().height / 3)))

    # fade the green button
    if gui.left_graph_col != GREEN:
        gui.left_graph_col = (gui.left_graph_col[0] - 3, gui.left_graph_col[1],
                              gui.left_graph_col[2] - 3)
        pygame.draw.rect(window, gui.left_graph_col, LEFT_RECT)

        # Re render the button label
        left_button_label = FONT.render('Left in stored graphs', True, (0, 0, 0))

        window.blit(left_button_label, (X_OFFSET + 3 * RECT_WIDTH / 8
                                        - int(left_button_label.get_rect().width / 2),
                                        (int(EDIT_RECT_Y_E + EDIT_RECT_Y_S) / 2)
                                        - int(left_button_label.get_rect().height / 3)))

    # fade the blue button
    if gui.right_graph_col != BLUE:
        gui.right_graph_col = (gui.right_graph_col[0] - 3, gui.right_graph_col[1] - 3,
                               gui.right_graph_col[2])
        pygame.draw.rect(window, gui.right_graph_col, RIGHT_RECT)

        # Re render the button label
        right_button_label = FONT.render('Right in stored graphs', True, (0, 0, 0))

        window.blit(right_button_label, (X_OFFSET + 5 * RECT_WIDTH / 8
                                         - int(right_button_label.get_rect().width / 2),
                                         (int(EDIT_RECT_Y_E + EDIT_RECT_Y_S) / 2)
                                         - int(right_button_label.get_rect().height / 3)))

    # Fade regression button
    if gui.reg_graph_col != CYAN:
        gui.reg_graph_col = (gui.reg_graph_col[0] - 3, gui.reg_graph_col[1],
                             gui.reg_graph_col[2])
        pygame.draw.rect(window, gui.reg_graph_col, REG_RECT)

        # Re render the button label
        reg_button_label = FONT.render('Preform Regression', True, (0, 0, 0))

        window.blit(reg_button_label, (X_OFFSET + 7 * RECT_WIDTH / 8
                                       - int(reg_button_label.get_rect().width / 2),
                                       (int(EDIT_RECT_Y_E + EDIT_RECT_Y_S) / 2)
                                       - int(reg_button_label.get_rect().height / 3)))

    # Stop fading if no button has been pressed recently
    if gui.add_rect_col == RED and gui.left_graph_col == GREEN and gui.right_graph_col == BLUE\
            and gui.reg_graph_col == CYAN:
        u_input.fade_buttons = False


def handle_update_screen(window: pygame.Surface, gui: graphics_UI.GuiSlider,
                         u_input: user_input.Userinput) -> None:
    """
    Handle general updates to the screen
     - cover previous graph with a black rectangle
    - update the current graph if it's been scaled/restricted/changed
    - fade buttons if they've been pressed
    - render user entered text
    """
    if u_input.fade_buttons:
        handle_fade_buttons(window, gui, u_input)

    # cover previous graph
    pygame.draw.rect(window, (0, 0, 0), pygame.Rect(0, 0, WIN_WIDTH,
                                                    int(WIN_HEIGHT - Y_OFFSET * 7)))

    # redraw the adjusted new graph
    if u_input.preview_graph:
        gui.graph_ex.draw_graph((gui.x_start, gui.x_end), (Y_START, gui.y_end),
                                (int(gui.x_se_graph[0]), int(gui.x_se_graph[1])))
    else:
        u_input.list_of_graphs[u_input.current_graph].draw_graph((gui.x_start, gui.x_end),
                                                                 (Y_START, gui.y_end),
                                                                 (int(gui.x_se_graph[0]),
                                                                  int(gui.x_se_graph[1])))

    # # render user entered text
    # entered_text = FONT_TYPE.render(u_input.typed_string, False, (200, 50, 10))
    # window.blit(entered_text, (X_OFFSET, int(WIN_HEIGHT) - Y_OFFSET * 2))

    pygame.display.flip()


def handle_adjust_scale_y(window: pygame.Surface, gui: graphics_UI.GuiSlider, mouse_x: float) -> None:
    """
    When the adjust scale y slider is moved adjust what is the size of the displayed graph in the y
    direction. Adjust how far from the bottom of the screen the graph is (y_end)
    which is calculated with Gui's y_offset.

    The graph always starts from the same y value, (y_start)
    Every graph has the same size, since its based off of the Gui

    - adjust the current graph's y_offset property
    - Based of y_offset adjust the graph's y_end and y_start properties
    - Redraw the scale_y slider to it's appropriate position
    * Do not actually redraw the graph, that is done in handle_update_screen() *

     Preconditions:
        - window.width > 350
        - window.height > 350

    * gui has been initialized correctly *
    * u_input has been initialized correctly *
    """

    # set current graph's y_offset property
    y_off_num = max(min((mouse_x - X_OFFSET), WIN_WIDTH - 2 * X_OFFSET), 0)
    gui.y_offset = Y_MIN_OFFSET + y_off_num / RECT_WIDTH * (Y_MAX_OFFSET - Y_MIN_OFFSET)

    # set the scale_y slider to it's appropriate position
    gui.xy_slid_pos[1] = (gui.y_offset - Y_MIN_OFFSET) * RECT_WIDTH / (Y_MAX_OFFSET
                                                                       - Y_MIN_OFFSET) + Y_OFFSET

    # Redraw the y_scale slider bar
    pygame.draw.rect(window, (0, 0, 0), pygame.Rect(0, int(
        int(WIN_HEIGHT) - Y_OFFSET * 4) - gui.slid_rad / 2, WIN_WIDTH, 10))
    pygame.draw.rect(window, (255, 255, 255), SCALE_Y_RECT)

    # Redraw the y_scale slider circle
    pygame.draw.circle(window, (255, 255, 255), (gui.xy_slid_pos[1], int(
        int(WIN_HEIGHT) - Y_OFFSET * 4 + gui.slid_rad / 2)), gui.slid_rad)

    # adjust graph's y_end
    gui.y_end = int(WIN_HEIGHT / 2) + gui.y_offset


def handle_adjust_scale_x(window: pygame.Surface, gui: graphics_UI.GuiSlider, mouse_x: float) -> None:
    """
    When the adjust scale x slider is moved adjust what is the size of the displayed graph in the x
    direction. Adjust how far from either side of the screen the graph is (x_start and x_end)
    which is calculated with Gui's x_offset.

    The graph is always centered in the x direction
    Every graph has the same size, since its based off of the Gui

    - set the current graph's x_offset property
    - Based of x_offset adjust the graph's x_end and x_start properties
    - Redraw the scale_x slider to it's appropriate position
    * Do not actually redraw the graph, that is done in handle_update_screen() *

     Preconditions:
        - window.width > 350
        - window.height > 350

    * gui has been initialized correctly *
    * u_input has been initialized correctly *
    """

    # set current graph's x_offset property
    x_off_num = max(min((mouse_x - X_OFFSET), WIN_WIDTH - 2 * X_OFFSET), 0)
    gui.x_offset = X_MIN_OFFSET + x_off_num / RECT_WIDTH * (X_MAX_OFFSET - X_MIN_OFFSET)

    # set the scale_x slider to it's appropriate position
    gui.xy_slid_pos[0] = (gui.x_offset - X_MIN_OFFSET) * RECT_WIDTH / (X_MAX_OFFSET
                                                                       - X_MIN_OFFSET) + X_OFFSET

    # Redraw the x_scale slider bar
    pygame.draw.rect(window, (0, 0, 0), pygame.Rect(0, int(
        int(WIN_HEIGHT) - Y_OFFSET * 3) - gui.slid_rad / 2, WIN_WIDTH, 10))
    pygame.draw.rect(window, (255, 255, 255), SCALE_X_RECT)

    # Redraw the x_scale slider circle
    pygame.draw.circle(window, (255, 255, 255), (gui.xy_slid_pos[0], int(
        int(WIN_HEIGHT) - Y_OFFSET * 3 + gui.slid_rad / 2)), gui.slid_rad)

    # adjust Gui's x_start and x_end properties
    gui.x_start = gui.x_offset
    gui.x_end = WIN_WIDTH - gui.x_offset


def handle_adjust_start_x(window: pygame.Surface, gui: graphics_UI.GuiSlider,
                          u_input: user_input.Userinput, mouse_x: float) -> None:
    """
    When the adjust start x slider is moved adjust what is the first point on the displayed
    graph to be graphed. (Restriction on the displayed graph's domain by setting a min x-value)

    - set the current graph's start_x property
    - Redraw the start_x and end_x slider to it's appropriate position
    * Do not actually redraw the graph, that is done in handle_update_screen() *

     Preconditions:
        - window.width > 350
        - window.height > 350

    * gui has been initialized correctly *
    * u_input has been initialized correctly *
    """

    # adjust the graph's start_x property based on the mouse position
    if u_input.preview_graph:
        max_portion = max(
            min((mouse_x - X_OFFSET), gui.x_se_slid_pos[1]
                - 2 * RECT_WIDTH / len(gui.graph_ex.x_values) - X_OFFSET), 0)
        gui.x_se_graph[0] = max_portion / RECT_WIDTH * (len(gui.graph_ex.x_values)
                                                        - gui.x_start_slid_minmax[0])
    else:
        len_portion = len(u_input.list_of_graphs[u_input.current_graph].x_values)
        sub_part = gui.x_start_slid_minmax[0]
        gui.x_se_graph[0] = max(min((mouse_x - X_OFFSET),
                                    gui.x_se_slid_pos[1] - 2 * RECT_WIDTH / len_portion
                                    - X_OFFSET), 0) / RECT_WIDTH * (len_portion - sub_part)

    # adjust where the slider circle will be, different depending on if the graph has been added to
    # the list of graphs
    if u_input.preview_graph:
        portion_num = gui.x_se_graph[0]
        portion_den = (len(gui.graph_ex.x_values) - gui.x_start_slid_minmax[0])
        gui.x_se_slid_pos[0] = X_OFFSET + portion_num / portion_den * RECT_WIDTH
    else:
        len_portion = len(u_input.list_of_graphs[u_input.current_graph].x_values)
        sub_part = gui.x_start_slid_minmax[0]
        gui.x_se_slid_pos[0] = X_OFFSET + gui.x_se_graph[0] / (len_portion - sub_part) * RECT_WIDTH

    # Redraw the x_start slider bar
    pygame.draw.rect(window, (0, 0, 0), pygame.Rect(0, int(
        int(WIN_HEIGHT) - Y_OFFSET * 5) - gui.slid_rad / 2, WIN_WIDTH, 10))
    pygame.draw.rect(window, (255, 255, 255), X_START_SLID)

    # Redraw the x_start slider circle
    pygame.draw.circle(window, (255, 255, 255), (gui.x_se_slid_pos[0], int(
        int(WIN_HEIGHT) - Y_OFFSET * 5 + gui.slid_rad / 2)), gui.slid_rad)

    # Redraw the x_end slider circle (since its on the same slider)
    pygame.draw.circle(window, (255, 255, 255), (gui.x_se_slid_pos[1], int(
        int(WIN_HEIGHT) - Y_OFFSET * 5 + gui.slid_rad / 2)), gui.slid_rad)


def handle_adjust_end_x(window: pygame.Surface, gui: graphics_UI.GuiSlider,
                        u_input: user_input.Userinput, mouse_x: float) -> None:
    """
    When the adjust end x slider is moved adjust what is the last point on the displayed
    graph to be graphed. (Restriction on the displayed graph's domain by setting a max x-value)

    - set the current graph's end_x property
    - Redraw the end_x and start_x slider to it's appropriate position
    * Do not actually redraw the graph, that is done in handle_update_screen() *

     Preconditions:
        - window.width > 350
        - window.height > 350

    * gui has been initialized correctly *
    * u_input has been initialized correctly *
    """

    # adjust the graph's end_x property based on the mouse's x position
    if u_input.preview_graph:
        min_p = min((mouse_x - X_OFFSET), WIN_WIDTH - 2 * X_OFFSET)
        len_p = len(gui.graph_ex.x_values)
        max_p = max(min_p, gui.x_se_slid_pos[0] + 2 * RECT_WIDTH / len_p - X_OFFSET)
        gui.x_se_graph[1] = max_p / RECT_WIDTH * (len_p - gui.x_end_slid_minmax[0])
    else:
        len_p = len(u_input.list_of_graphs[u_input.current_graph].x_values)
        min_p = min((mouse_x - X_OFFSET), WIN_WIDTH - 2 * X_OFFSET)
        max_p = max(min_p, gui.x_se_slid_pos[0] + 2 * RECT_WIDTH / len_p - X_OFFSET)
        gui.x_se_graph[1] = max_p / RECT_WIDTH * (len_p - gui.x_end_slid_minmax[0])

    # adjust where the slider circle will be, different depending on if the graph has been added to
    # the list of graphs
    if u_input.preview_graph:
        len_p = (len(gui.graph_ex.x_values) - gui.x_end_slid_minmax[0])
        gui.x_se_slid_pos[1] = X_OFFSET + gui.x_se_graph[1] / len_p * RECT_WIDTH
    else:
        len_p = len(u_input.list_of_graphs[u_input.current_graph].x_values)
        denom_p = (len_p - gui.x_end_slid_minmax[0])
        gui.x_se_slid_pos[1] = X_OFFSET + gui.x_se_graph[1] / denom_p * RECT_WIDTH

    # Redraw the x_start slider bar
    pygame.draw.rect(window, (0, 0, 0), pygame.Rect(0, int(
        int(WIN_HEIGHT) - Y_OFFSET * 5) - gui.slid_rad / 2, WIN_WIDTH, 10))
    pygame.draw.rect(window, (255, 255, 255), X_START_SLID)

    # Redraw the x_start slider circles
    pygame.draw.circle(window, (255, 255, 255), (gui.x_se_slid_pos[1], int(
        int(WIN_HEIGHT) - Y_OFFSET * 5 + gui.slid_rad / 2)), gui.slid_rad)

    pygame.draw.circle(window, (255, 255, 255), (gui.x_se_slid_pos[0], int(
        int(WIN_HEIGHT) - Y_OFFSET * 5 + gui.slid_rad / 2)), gui.slid_rad)


def init_visuals(window: pygame.Surface, gui: graphics_UI.GuiSlider) -> None:
    """
    Draw all the 'buttons' and 'sliders' when the main loop is first called

    Preconditions:
        - window.width > 350
        - window.height > 350

    *gui is initialized correctly*
    """

    # buttons
    pygame.draw.rect(window, (255, 255, 255), CHOOSE_DATA_RECT)
    pygame.draw.rect(window, (255, 255, 255), CREATE_PLOTLY_RECT)
    pygame.draw.rect(window, (255, 0, 255), CREATE_PLOTLY_ALL_RECT)
    pygame.draw.rect(window, (255, 0, 0), ADD_GRAPH_RECT)
    pygame.draw.rect(window, (0, 255, 0), LEFT_RECT)
    pygame.draw.rect(window, (0, 0, 255), RIGHT_RECT)
    pygame.draw.rect(window, (0, 255, 255), REG_RECT)

    # Plotly button labels
    plotly_button_label_s = FONT_BUTTON.render('Plotly Current Graph', True, (0, 0, 0))
    plotly_button_label_a = FONT_BUTTON.render('Plotly All Stored graphs', True, (0, 0, 0))

    # Store graph button labels
    add_button_label = FONT.render('Store graph', True, (0, 0, 0))
    left_button_label = FONT.render('Left in stored graphs', True, (0, 0, 0))
    right_button_label = FONT.render('Right in stored graphs', True, (0, 0, 0))
    reg_button_label = FONT.render('Perform Regression', True, (0, 0, 0))

    # Blit the button labels
    window.blit(plotly_button_label_s, (X_OFFSET + RECT_WIDTH / 4
                                        - int(plotly_button_label_s.get_rect().width / 2),
                                        (int(PLOTLY_RECT_Y_S + PLOTLY_RECT_Y_E) / 2)
                                        - int(plotly_button_label_s.get_rect().height / 2)))
    window.blit(plotly_button_label_a, (X_OFFSET + 3 * RECT_WIDTH / 4
                                        - int(plotly_button_label_a.get_rect().width / 2),
                                        (int(PLOTLY_RECT_Y_S + PLOTLY_RECT_Y_E) / 2)
                                        - int(plotly_button_label_a.get_rect().height / 2)))
    window.blit(add_button_label, (X_OFFSET + 1 * RECT_WIDTH / 8
                                   - int(add_button_label.get_rect().width / 2),
                                   (int(EDIT_RECT_Y_E + EDIT_RECT_Y_S) / 2)
                                   - int(add_button_label.get_rect().height / 3)))
    window.blit(left_button_label, (X_OFFSET + 3 * RECT_WIDTH / 8
                                    - int(left_button_label.get_rect().width / 2),
                                    (int(EDIT_RECT_Y_E + EDIT_RECT_Y_S) / 2)
                                    - int(left_button_label.get_rect().height / 3)))
    window.blit(right_button_label, (X_OFFSET + 5 * RECT_WIDTH / 8
                                     - int(right_button_label.get_rect().width / 2),
                                     (int(EDIT_RECT_Y_E + EDIT_RECT_Y_S) / 2)
                                     - int(right_button_label.get_rect().height / 3)))
    window.blit(reg_button_label, (X_OFFSET + 7 * RECT_WIDTH / 8
                                   - int(reg_button_label.get_rect().width / 2),
                                   (int(EDIT_RECT_Y_E + EDIT_RECT_Y_S) / 2)
                                   - int(reg_button_label.get_rect().height / 3)))

    # sliders
    pygame.draw.rect(window, (255, 255, 255), SCALE_X_RECT)
    pygame.draw.rect(window, (255, 255, 255), SCALE_Y_RECT)
    pygame.draw.rect(window, (255, 255, 255), X_START_SLID)

    # slider circles
    pygame.draw.circle(window, (255, 255, 255), (gui.xy_slid_pos[0], int(
        SCALE_X_RECT_Y_S + gui.slid_rad / 2)), gui.slid_rad)
    pygame.draw.circle(window, (255, 255, 255), (gui.xy_slid_pos[1], int(
        SCALE_Y_RECT_Y_S + gui.slid_rad / 2)), gui.slid_rad)
    pygame.draw.circle(window, (255, 255, 255), (gui.x_se_slid_pos[0], int(
        X_START_RECT_S + gui.slid_rad / 2)), gui.slid_rad)
    pygame.draw.circle(window, (255, 255, 255), (gui.x_se_slid_pos[1], int(
        X_START_RECT_S + gui.slid_rad / 2)), gui.slid_rad)


def handle_scroll_up(mouse_x: int, window: pygame.Surface, gui: graphics_UI.GuiSlider,
                     u_input: user_input.Userinput) -> None:
    """
    When the mouse has scrolled upwards recently
    restrict the domain of the graph towards where the mouse was scrolled. (Zoom in onto the graph)
        - Change the graph's x_start parameter
        - Change the graph's x_end parameter
        - Restrict slider movement so they do not overlap
        - Restrict slider movement so the sliders do not move past the mouse

    Preconditions:
        - window.width > 350
        - window.height > 350

    * gui has been initialized correctly *
    * u_input has been initialized correctly *
    """

    # Adjusts both sliders position, max and min prevent overlap and going past the mouse
    # different depending on if the graph has been stored or not

    if gui.x_start < mouse_x < gui.x_end:
        if u_input.preview_graph:
            denom = ((gui.x_end - gui.x_start) / len(gui.graph_ex.x_values))
            gui.x_se_graph[1] = max((gui.x_se_graph[1] - 1), gui.x_se_graph[0] + 2,
                                    (mouse_x - gui.x_start) / denom)

            gui.x_se_graph[0] = min((gui.x_se_graph[0] + 1), int(gui.x_se_graph[1] - 2),
                                    int((mouse_x - X_OFFSET) / denom))
        else:
            len_p = len(u_input.list_of_graphs[u_input.current_graph].x_values)
            gui.x_se_graph[1] = max((gui.x_se_graph[1] - 1), gui.x_se_graph[0] + 2,
                                    (mouse_x - gui.x_start) / ((gui.x_end - gui.x_start) / len_p))

            gui.x_se_graph[0] = min((gui.x_se_graph[0] + 1), int(gui.x_se_graph[1] - 2),
                                    int((mouse_x - X_OFFSET) / ((gui.x_end - gui.x_start) / len_p)))

        # Adjust the x_end and x_start slider positions
        if u_input.preview_graph:
            denom = (len(gui.graph_ex.x_values) - gui.x_end_slid_minmax[0])
            gui.x_se_slid_pos[1] = X_OFFSET + gui.x_se_graph[1] / denom * RECT_WIDTH
            denom = (len(gui.graph_ex.x_values) - gui.x_start_slid_minmax[0])
            gui.x_se_slid_pos[0] = X_OFFSET + gui.x_se_graph[0] / denom * RECT_WIDTH
        else:
            len_p = len(u_input.list_of_graphs[u_input.current_graph].x_values)
            denom = (len_p - gui.x_end_slid_minmax[0])
            gui.x_se_slid_pos[1] = X_OFFSET + gui.x_se_graph[1] / denom * RECT_WIDTH

            gui.x_se_slid_pos[0] = X_OFFSET + gui.x_se_graph[0] / (
                len(u_input.list_of_graphs[u_input.current_graph].x_values)
                - gui.x_start_slid_minmax[0]) * RECT_WIDTH

        # Redraw the slider
        pygame.draw.rect(window, (0, 0, 0), pygame.Rect(0, int(
            int(WIN_HEIGHT) - Y_OFFSET * 5) - gui.slid_rad / 2, WIN_WIDTH, 10))
        pygame.draw.rect(window, (255, 255, 255), X_START_SLID)

        pygame.draw.circle(window, (255, 255, 255), (gui.x_se_slid_pos[1], int(
            int(WIN_HEIGHT) - Y_OFFSET * 5 + gui.slid_rad / 2)), gui.slid_rad)

        pygame.draw.circle(window, (255, 255, 255), (gui.x_se_slid_pos[0], int(
            int(WIN_HEIGHT) - Y_OFFSET * 5 + gui.slid_rad / 2)), gui.slid_rad)


def handle_scroll_down(window: pygame.Surface, gui: graphics_UI.GuiSlider,
                       u_input: user_input.Userinput, mouse_x: int) -> None:
    """
    When the mouse has scrolled downwards recently
    relax the restriction on the domain of the graph (Zoom out of the graph)
        - Change the graph's x_start parameter
        - Change the graph's x_end parameter
        - prevent any of the sliders from going to values out of the domain i.e point with x = -1

    Preconditions:
        - window.width > 350
        - window.height > 350

    * gui has been initialized correctly *
    * u_input has been initialized correctly *
    """

    # Change the value of x_end and x_start

    if gui.x_start < mouse_x < gui.x_end:
        if u_input.preview_graph:
            gui.x_se_graph[1] = min((gui.x_se_graph[1] + 1), len(gui.graph_ex.x_values))
            gui.x_se_graph[0] = max((gui.x_se_graph[0] - 1), 0)
        else:
            gui.x_se_graph[1] = min((gui.x_se_graph[1] + 1),
                                    len(u_input.list_of_graphs[u_input.current_graph].x_values))
            gui.x_se_graph[0] = max((gui.x_se_graph[0] - 1), 0)

        # change the position of the sliders
        if u_input.preview_graph:
            denom = (len(gui.graph_ex.x_values) - gui.x_end_slid_minmax[0])
            gui.x_se_slid_pos[1] = X_OFFSET + gui.x_se_graph[1] / denom * RECT_WIDTH
            denom = (len(gui.graph_ex.x_values) - gui.x_start_slid_minmax[0])
            gui.x_se_slid_pos[0] = X_OFFSET + gui.x_se_graph[0] / denom * RECT_WIDTH
        else:
            len_p = len(u_input.list_of_graphs[u_input.current_graph].x_values)
            denom = (len_p - gui.x_end_slid_minmax[0])
            gui.x_se_slid_pos[1] = X_OFFSET + gui.x_se_graph[1] / denom * RECT_WIDTH

            gui.x_se_slid_pos[0] = X_OFFSET + gui.x_se_graph[0] / (
                len(u_input.list_of_graphs[u_input.current_graph].x_values)
                - gui.x_start_slid_minmax[0]) * RECT_WIDTH

        # Redraw the sliders
        pygame.draw.rect(window, (0, 0, 0), pygame.Rect(0, int(
            int(WIN_HEIGHT) - Y_OFFSET * 5) - gui.slid_rad / 2, WIN_WIDTH, 10))
        pygame.draw.rect(window, (255, 255, 255), X_START_SLID)

        # Redraw the x_start slider circle
        pygame.draw.circle(window, (255, 255, 255),
                           (gui.x_se_slid_pos[1],
                            int(int(WIN_HEIGHT) - Y_OFFSET * 5 + gui.slid_rad / 2)), gui.slid_rad)

        pygame.draw.circle(window, (255, 255, 255), (gui.x_se_slid_pos[0], int(
            int(WIN_HEIGHT) - Y_OFFSET * 5 + gui.slid_rad / 2)), gui.slid_rad)


def handle_mouse_scroll(u_input: user_input.Userinput, scroll_y: int) -> None:
    """
    When the mouse has been scrolled allow the restriction on the
    graph to be changed and gather the strength at with the mouse
    was scrolled at *scroll_y*

    * u_input has been initialized correctly *
    """
    u_input.recently_scrolled = True
    u_input.scroll_y = scroll_y


def handle_recently_scrolled(mouse_x: int, window: pygame.Surface,
                             gui: graphics_UI.GuiSlider, u_input: user_input.Userinput) -> None:
    """
    If the mouse has recently be scrolled restrict the domain of the current graph
    depending on where the mouse is placed

    After the mouse was scrolled set a timer to continue to change the restriction
    Makes the scrolling more fluid
    Length of timer depends on strength of scroll

    Does not actually restrict the graph that is done in handle_mouse_scroll_up() or down

    Preconditions:
        - window.width > 350
        - window.height > 350

    * gui has been initialized correctly *
    * u_input has been initialized correctly *
    """
    # Count down the timer
    u_input.scroll_counter -= 1

    if u_input.scroll_counter < 0:

        if u_input.preview_graph:
            u_input.scroll_counter = max(3, len(gui.graph_ex.x_portion) / 12)
        else:
            len_graphs = len(u_input.list_of_graphs[u_input.current_graph].x_portion) / 12
            u_input.scroll_counter = max(3, len_graphs)

        if u_input.scroll_y > 0:
            u_input.scroll_y = max(0, u_input.scroll_y / 2 - 1)
        else:
            u_input.scroll_y = min(0, u_input.scroll_y / 2 + 1)

        # Stop restricting the graph when the timer ends
        if u_input.scroll_y == 0:
            u_input.recently_scrolled = False

    # If the timer has not ended continue to restrict the graph
    if u_input.scroll_y <= 0:
        handle_scroll_up(mouse_x, window, gui, u_input)
    else:
        handle_scroll_down(window, gui, u_input, mouse_x)


def main() -> None:
    """
    The main pygame loop, when called opens pygame and GUI.
    Also Handles user input
    """

    # init pygame and screen
    pygame.init()
    pygame.font.init()
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.draw.rect(window, (0, 0, 0), pygame.Rect(0, 0, WIN_WIDTH, WIN_HEIGHT))

    # init the data classes for updating pygame and the window
    gui = graphics_UI.GuiSlider(WIN_HEIGHT, WIN_WIDTH, window)
    u_input = user_input.Userinput()

    # generate time graphs for pollutants
    time_graphs = generated_graphs.generate_time_graphs('010102', window)
    for graph_in in time_graphs:
        add_new_graph(window, gui, u_input, graph_in)
        handle_add_graph(window, u_input, gui)

    # Draw all the default visuals when screen is first loaded, i.e default graph the sliders

    init_visuals(window, gui)
    gui.graph_ex.draw_graph((gui.x_start, gui.x_end), (Y_START, gui.y_end),
                            (0, len(gui.graph_ex.x_values)))

    while True:
        for event in pygame.event.get():

            # Handel user generated events

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_press(window, pygame.mouse.get_pos()[0],
                                   pygame.mouse.get_pos()[1], gui, u_input)
                u_input.scroll_y = 0

            if event.type == pygame.MOUSEBUTTONUP:
                handle_mouse_up(u_input)

            if event.type == pygame.MOUSEWHEEL:
                handle_mouse_scroll(u_input, event.y)

            if u_input.mouse_held:
                handle_mouse_held(window, u_input, pygame.mouse.get_pos()[0], gui)

            # Graph is restricted to where current mouse is
            # Prevents the restriction following mouse after you scrolled
            if event.type == pygame.MOUSEMOTION:
                u_input.recently_scrolled = False

        if u_input.recently_scrolled:
            handle_recently_scrolled(pygame.mouse.get_pos()[0], window, gui, u_input)

        # update the visuals
        handle_update_screen(window, gui, u_input)


if __name__ == '__main__':
    # import python_ta
    #
    # python_ta.check_all(config={
    #     'extra-imports': ['pygame', 'plotly.graph_objects',
    #                       'plotly.subplots', 'python_ta.contracts',
    #                       'graph', 'dataclass', 'user_input', 'generated_graphs',
    #                       'compute'],
    #     'allowed-io': [],
    #     'max-line-length': 100,
    #     'disable': ['R1705', 'C0200'],
    #     'generated-members': ['pygame.*']
    # })
    #
    # import python_ta.contracts
    #
    # python_ta.contracts.DEBUG_CONTRACTS = False
    # python_ta.contracts.check_all_contracts()

    # import doctest
    #
    # doctest.testmod(verbose=True)

    main()
