"""
hold all of the computations that are preformed on the collected data
"""

from typing import List, Tuple, Any
from math import log, sqrt
from matrix import Matrix


def add_values(val1: Tuple[List[Any], List[int]], val2: Tuple[List[Any], List[int]]) -> \
        Tuple[List[str], List[int]]:
    """
    Calculate the combined average of the inputted values for the days that have data available.

    Preconditions:
        - len(val1[1]) > 0
        - len(val2[1]) > 0

    >>> a = (['2019010101', '2019010103', '2019010104', '2019010105'], [35, 34, 36, 34])
    >>> b = (['2019010101', '2019010102', '2019010103', '2019010105'], [4, 5, 5, 4])
    >>> add_values(a, b)
    (['2019010101', '2019010103', '2019010105'], [39, 39, 38])
    """

    # resulting dates and summed values
    date_list = []
    sum_list = []

    for i in range(0, len(val1[0])):
        for j in range(0, len(val2[0])):
            # matching the dates
            if val1[0][i] == val2[0][j]:

                # calculating summed value
                date_list.append(val1[0][i])
                sum_list.append(val1[1][i] + val2[1][j])

    return (date_list, sum_list)


def calculate_average_collection(points: tuple) -> tuple:
    """Return the two averages of a collection of numbers passed in as a tuple.

    points is a tuple of two lists: ([x_1, x_2 ...], [y_1, y_2, ...])
    This function returns the averages of the two lists in the form of a tuple.

    You may ASSUME that:
        - both lists are not empty

    >>> calculate_average_collection(([1, 2, 3], [1, 2, 3]))
    (2.0, 2.0)
    >>> calculate_average_collection(([10.0, 20.0, 30.0], [3.0, 6.0, 12.0]))
    (20.0, 7.0)
    """
    return (sum(points[0]) / len(points[0]), sum(points[1]) / len(points[1]))


def calculate_r_squared(points: Tuple[List[float], List[float]], a: float, b: float) -> float:
    """Return the R squared value when the given points are modelled as the line y = a + bx.

    points is a list of pairs of numbers: [(x_1, y_1), (x_2, y_2), ...]

    Assume that:
        - points is not empty and contains tuples
        - each element of points is a tuple containing two floats
    """
    y_bar = calculate_average_collection(points)[1]
    s_tot = sum([(y - y_bar) ** 2 for y in points[1]])
    s_res = sum([(points[1][i] - (a + b * points[0][i])) ** 2 for i in range(len(points[0]))])
    r_squared = 1 - (s_res / s_tot)
    return r_squared


def simple_linear_regression(points: Tuple[List[float], List[float]]) -> tuple:
    """Perform a linear regression on the given points.

    points is a list of pairs of floats: [(x_1, y_1), (x_2, y_2), ...]
    This function returns a pair of floats (a, b) such that the line
    y = a + bx is the approximation of this data.

    Further reading: https://en.wikipedia.org/wiki/Simple_linear_regression

    You may ASSUME that:
        - len(points) > 0
        - each element of points is a tuple of two floats

    >>> simple_linear_regression(([1.0, 2.0, 3.0], [1.0, 2.0, 3.0]))
    (0.0, 1.0)
    >>> simple_linear_regression(([10.0, 20.0, 30.0], [3.0, 6.0, 12.0]))
    (-2.0, 0.45)

    Hint: you might want to define a separate function that calculates the average
    of a collection of numbers.
    """
    x_bar, y_bar = calculate_average_collection(points)
    x_bracket = [x - x_bar for x in points[0]]
    y_bracket = [y - y_bar for y in points[1]]
    b_top = sum(x_bracket[i] * y_bracket[i] for i in range(len(x_bracket)))
    b_bottom = sum(x_b ** 2 for x_b in x_bracket)
    b = b_top / b_bottom
    a = y_bar - b * x_bar
    return (a, b)


def polynomial_regression(deg: int, x_val: List[float], y_val: List[float]) -> List[float]:
    """
    Calculate the coefficients of a polynomial function with degree deg
    that best fits the input data

    the output is ordered in increasing degree

    Preconditions:
        - deg > 0
        - len(x_val) > 0
        - len(x_val) == len(y_val)

    >>> polynomial_regression(2, [10, 20, 30, 40, 50, 60, 0.354, 0.38, 0.405, 0.43],\
        [0.1245, 0.185, 0.2285, 0.265, 0.297, 0.3285, 70, 80, 90, 100])
    [80.44857677401095, -4.871378463853153, 0.06236668350454819]
    >>> polynomial_regression(1, [1985, 1990, 1995, 2000, 2005, 2010, 2015],\
        [116576, 130482, 145562, 155328, 158401, 159440, 167543])
    [-3047466.8571428573, 1597.5428571428572]
    """

    matrix_r = Matrix(deg + 1, deg + 1)
    matrix_l = [[]]

    # fills the coefficient matrix
    for row in range(0, (deg + 1)):
        for column in range(0, deg + 1):
            matrix_l[row].append(sum([pow(x, row + column) for x in x_val]))
        if row != deg:
            matrix_l.append([])

    constant_vec = []
    x_temp = 0

    # fills the column vector of constants
    for row in range(0, (deg + 1)):
        for i in range(0, len(x_val)):
            x_temp += pow(x_val[i], row) * y_val[i]
        constant_vec.append(x_temp)
        x_temp = 0

    matrix_r.set_matrix(matrix_l)
    return matrix_r.solve(constant_vec)


def exponential_regression(x_val: List[float], y_val: List[float]) -> List[float]:
    """
    Calculates the coefficients of an exponential function that best fits
    the given input

    output is a list in the form [a, b], where y = b * a^x

    Preconditions:
        - len(x_val) > 0
        - len(x_val) == len(y_val)

    >>> exponential_regression([1985, 1990, 1995, 2000, 2005, 2010, 2015] ,\
        [56593071, 56719240, 56844303, 56942108, 57969485, 59277417, 61336387])
    [1.0024980484455097, 394317.0737279723]
    """
    valids = [log(y) for y in y_val if y != 0]
    place_avg = sum(valids) / len(valids)

    log_values = []
    for value in y_val:
        if value != 0:
            log_values.append(log(value, 10))
        else:
            log_values.append(place_avg)

    coefficients = polynomial_regression(1, x_val, log_values)
    return [pow(10, coefficients[1]), pow(10, coefficients[0])]


def standard_deviation(points: Tuple[List[float], List[float]]) -> float:
    """Return the standard deviation of a sample of data passed in as a tuple of floats.

    points is a tuple of two lists: ([x_1, x_2 ...], [y_1, y_2, ...])
    This function returns the standard deviation of the sample of data as a float.

    You may ASSUME that:
        - both lists are not empty

    >>> points = ([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0], [10.0, 12.0, 23.0, 23.0, 16.0, 23.0, 21.0, 16.0])
    >>> standard_deviation(points)
    5.237229365663817
    """
    x_coords, y_coords = points[0], points[1]

    # Finding the mean of the y values in the data set:
    mean = sum(y_coords) / len(x_coords)

    # Calculating the sum of the square of every y value minus the mean y value
    total = 0
    for y in y_coords:
        total = total + ((y - mean) ** 2)

    # Dividing the total by the number of x values minus 1 and then taking the square root
    standard_dev = sqrt(total / (len(x_coords) - 1))

    return standard_dev


def relative_standard_deviation(points: Tuple[List[float], List[float]]) -> float:
    """Return the relative standard deviation of a sample of data passed in as a tuple of floats.

    points is a tuple of two lists: ([x_1, x_2 ...], [y_1, y_2, ...])
    This function returns the standard deviation of the sample of data as a float.

    You may ASSUME that:
        - both lists are not empty

    >>> points = ([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0], [10.0, 12.0, 23.0, 23.0, 16.0, 23.0, 21.0, 16.0])
    >>> relative_standard_deviation(points)
    29.095718698132316
    """
    x_coords, y_coords = points[0], points[1]

    # Finding the mean of the y values in the sample data set:
    mean = sum(y_coords) / len(x_coords)

    # Calculating the standard deviation of a sample size:
    standard_dev = standard_deviation(points)

    # Determining the percentage of the standard deviation by the mean
    rel_standard_dev = (standard_dev / mean) * 100

    return rel_standard_dev


def gen_points_matching_date(data1: Tuple[List[Any], List[float]],
                             data2: Tuple[List[Any], List[float]]) -> Tuple[List[int], List[int]]:
    """
    This function returns plots for O3 vs NO2 using matching dates

    NOTE: data1 y-values become the x-values, and data2 y-values become the y-values
    NOTE: x-values are sorted in ascending order for the plotting software

    Preconditions:
        - len(data1) > 0 and len(data2) > 0
        - len(data1[0]) == len(data1[1]) and len(data2[0]) == len(data2[1])

    >>> gen_points_matching_date((['a', 'b', 'd'], [1, 2, 3]), (['a', 'b', 'c'], [4, 5, 6]))
    ([1, 2], [4, 5])
    """
    x_cor, y_cor = [], []
    for i in range(len(data1[0])):
        date = data1[0][i]
        for j in range(len(data2[0])):
            other_date = data2[0][j]
            if date == other_date:
                x_cor.append(int(data1[1][i]))
                y_cor.append(int(data2[1][j]))
    zippy = zip(x_cor, y_cor)
    x_cor, y_cor = [list(a) for a in zip(*sorted(zippy))]

    return (x_cor, y_cor)


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['matrix', 'math', 'python_ta.contracts'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200'],
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod(verbose=True)
