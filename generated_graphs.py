"""This file generates the necessary DataFiles for the viewing part of our project, and preloads
them into the software.
"""
from typing import List, Any, Tuple
import pygame
from loading_data import DataFile
import graph
import compute
NO2_1999 = DataFile('csv_files/NO2_1999.csv')
NO2_2001 = DataFile('csv_files/NO2_2001.csv')
NO2_2010 = DataFile('csv_files/NO2_2010.csv')
O3_1999 = DataFile('csv_files/O3_1999.csv')
O3_2001 = DataFile('csv_files/O3_2001.csv')
O3_2010 = DataFile('csv_files/O3_2010.csv')

FILES = [NO2_1999, NO2_2001, NO2_2010, O3_1999, O3_2001, O3_2010]

for FILE in FILES:
    FILE.load()


def generate_time_graphs(station_id: str, window: pygame.Surface) -> List[graph.Graph]:
    """This function generates the graphs needed to fulfill our research goals
    and stores them for viewing and plotting. This returns our preloaded graphs
    which is called in main() and added to the general inventory."""

    new_graphs = []

    ox_matches = [(NO2_1999, O3_1999), (NO2_2001, O3_2001), (NO2_2010, O3_2010)]
    for tup in ox_matches:
        (properties_no2, x_cor_no2, y_cor_no2) \
            = tup[0].return_plot_daily(station_id)
        (properties_o3, x_cor_o3, y_cor_o3) \
            = tup[1].return_plot_daily(station_id)

        # NO2 GRAPH
        new_graphs.append(make_a_graph(window, properties_no2, x_cor_no2, y_cor_no2))

        # O3 GRAPH
        new_graphs.append(make_a_graph(window, properties_o3, x_cor_o3, y_cor_o3))

        # Ox GRAPH
        coord_sets = compute.add_values((x_cor_no2, y_cor_no2), (x_cor_o3, y_cor_o3))
        properties_ox = ("Ox " + tup[0].year, tup[0].year, "Ox (ppb)")
        new_graph = graph.Graph(window)
        new_graph.properties[0] = properties_ox[0]
        new_graph.labels = properties_ox[1], properties_ox[2]
        new_graph.x_values = [(i, coord_sets[0][i]) for i in range(len(coord_sets[0]))]
        new_graph.y_values = coord_sets[1]
        new_graph.properties[3] = True
        new_graphs.append(new_graph)

        # O3 vs NO2
        coord_sets = compute.gen_points_matching_date((x_cor_o3, y_cor_o3),
                                                      (x_cor_no2, y_cor_no2))
        new_graph = graph.Graph(window)
        new_graph.properties[0] = "NO2 vs O3 " + tup[0].year
        new_graph.labels = "O3 (ppb)", "NO2 (ppb)"
        new_graph.x_values = [(coord_sets[0][i], "fill") for i in range(len(coord_sets[0]))]
        new_graph.y_values = coord_sets[1]
        new_graph.properties[3] = False
        new_graphs.append(new_graph)

    return new_graphs


def make_a_graph(window: pygame.Surface,
                 properties: Tuple[str],
                 x_cor: List[Any],
                 y_cor: List[Any]) -> graph.Graph:
    """This is a helper function to generate a generic graph"""
    title, x_lab, y_lab = properties[0], properties[1], properties[2]
    new_graph = graph.Graph(window)
    new_graph.properties[0] = title
    new_graph.labels = x_lab, y_lab
    x_coords = [(i, x_cor[i]) for i in range(len(x_cor))]
    new_graph.x_values = x_coords
    new_graph.y_values = y_cor
    new_graph.properties[3] = True
    return new_graph


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['pygame', 'plotly.graph_objects',
                          'plotly.subplots', 'python_ta.contracts',
                          'graph', 'dataclass', 'user_input', 'random',
                          'loading_data', 'compute'],
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
