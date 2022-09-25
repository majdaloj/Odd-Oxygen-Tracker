"""Loading data from the csv module"""

import csv
import datetime as d
from typing import List, Optional, Dict, Tuple, Any


class DataFile:
    """
    This class stores a csv file and allows you to return
    data to be computed / plotted. This is a tool for our
    main application framework. This also includes basic
    statisticl analysis.

    Some CSV files have been provided for example usage

    Instance Attributes:
        - data: stores all the data
        - file_path: string to store the csv file path
        - header_row: represents the column headers:
        - stations: represents data rows corresponding to station ids
        - pollutant: pollutant in this data file
        - year: year this data was collected
    """
    data: List[List[Any]]
    file_path: str
    header_row: List[Any]
    stations: Dict[str, List[int]]
    pollutant: str
    year: str

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.data = []
        self.header_row = []
        self.stations = {}
        self.pollutant = ""
        self.year = ""

    def format(self) -> None:
        """standardize the data appearance for ID and DATE
        This is for ease of use, so data can be accessed easily"""

        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if j == 1 and len(self.data[i][j]) < 6:  # format ID
                    self.data[i][j] = '0' + self.data[i][j]
                if j == 6:  # format DATE
                    self.data[i][j] = self.data[i][j].replace('-', '')
                    self.data[i][j] = self.data[i][j].replace('/', '')
                if i > 0 and 7 <= j <= 31:  # format measurements
                    self.data[i][j] = float(self.data[i][j])

    def load(self) -> None:
        """Read from file_path into the collection 'data'

        >>> my_data = DataFile('doctest_dataset/O3_2019.csv')
        >>> my_data.load()
        >>> len(my_data.data)
        52554
        """

        found_header = False
        self.data = []
        with open(self.file_path, 'r', errors='replace') as file:
            csv_reader = csv.reader(file, delimiter=',')
            line_count = 0

            for row in csv_reader:  # csv reader using module
                if not found_header and helper_header(row):  # finding table header
                    found_header = True
                    self.header_row = row
                    self.data.append(row)
                    line_count += 1
                    continue
                if found_header:
                    good_row = False
                    if '-999' not in row:
                        good_row = True
                        self.data.append(row)
                        line_count += 1
                    st_id = row[1]
                    if st_id in self.stations and good_row:  # updating stations dictionary
                        self.stations[st_id][1] = line_count - 1
                    elif good_row:
                        self.stations[st_id] = [line_count - 1, line_count - 1]
        file.close()

        self.pollutant = self.data[1][0]
        self.year = self.data[1][6][0:4]
        self.format()

    def helper_is_valid_date(self, station_id: str, date: str) -> bool:
        """
        This function is used as a helper for precondition testing
        of the date

        Preconditions:
            - station_id in self.stations

        """

        col = self.get_col(6, self.stations[station_id][0], self.stations[station_id][1])
        return date in col

    def get_row(self, station_id: str, date: str,
                start_col: Optional[int] = 0,
                end_col: Optional[int] = -1) -> List[Any]:
        """Given a station id and row, this function returns
        that row's data using specified start and end row
        indices (0 and -1 if not specified).

        Returns an empty list if such a row doesn't exist.

        NOTE: start and end bounds are INCLUSIVE

        Preconditions:
            - start_col <= end_col
            - station_id in self.stations
            - helper_is_valid_date(station_id, date)

        """
        row_index = self.stations[station_id][0]
        for ind in range(self.stations[station_id][0], self.stations[station_id][1]):
            if self.data[ind][6] == date:
                row_index = ind
                break
        return self.data[row_index][start_col: end_col]

    def get_col(self, header_ind: int,
                start_row: Optional[int] = 0,
                end_row: Optional[int] = -1) -> List[Any]:
        """ Given a column header, this function returns the column
        using specified start and end row indicies (0 and -1 if not specified).

        If the column doesn't exist an empty list is returned

        NOTE: start and end bounds are INCLUSIVE

        Preconditions:
            - start_row <= end_row
        """

        if 0 <= header_ind <= len(self.header_row):
            return [self.data[i][header_ind] for i in range(start_row, end_row + 1)]
        else:
            return []

    def return_plot_hourly(self, station_id: str) \
            -> Tuple[Tuple[str, str, str], List[d.datetime], List[float]]:
        """ Return the coordinates of average concentration versus
        time

        The x-coordinates are strings representing the date formated as:
            'YYYYMMDDHH'

        Preconditions:
            - station_id in self.stations
        """

        [a, b] = self.stations[station_id]
        x_cor = []
        y_cor = []
        for i in range(a, b + 1):
            for j in range(7, 31):
                x_coord = self.data[i][6]
                if (j - 6) < 10:
                    x_coord += '0'
                x_coord += str(j - 6)

                x_cor.append(str_to_date(x_coord))
                y_cor.append(int(self.data[i][j]))
        title = self.pollutant + " over " + self.year
        (x_lab, y_lab) = (self.year, self.pollutant + ' (ppb)')
        return((title, x_lab, y_lab), x_cor, y_cor)

    def return_plot_daily(self, station_id: str)\
            -> Tuple[Tuple[str, str, str], List[d.datetime], List[float]]:
        """This returns the x-coordinates and corresponding y-coordinates
        for the daily average emissions given a station_id.

        Preconditions:
            - station_id in self.stations
        """
        [a, b] = self.stations[station_id]
        x_cor = []
        y_cor = []
        for i in range(a, b + 1):
            x_cor.append(str_to_date(self.data[i][6]))
            y_cor.append(help_average_day(self.data[i]))
        title = self.pollutant + " over " + self.year
        (x_lab, y_lab) = (self.year, self.pollutant + ' (ppb)')
        return ((title, x_lab, y_lab), x_cor, y_cor)

    def return_plot_monthly(self, station_id: str) -> Tuple[List[d.datetime], List[float]]:
        """ Returns the monthly averages for a given station

        Preconditions:
            - station_id in self.stations
        """
        x_cor = self.return_plot_daily(station_id)[1]
        y_cor = self.return_plot_daily(station_id)[2]
        months = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [],
                  7: [], 8: [], 9: [], 10: [], 11: [], 12: []}
        prev = x_cor[0].month
        for x in range(len(x_cor)):
            month = x_cor[x].month
            months[month].append(y_cor[x])
            if month != prev:
                months[prev] = sum(months[prev]) / len(months[prev])
                prev = month
        months[prev] = sum(months[prev]) // len(months[prev])

        x_cor, y_cor = [], []
        for k in months:
            if months[k] != []:
                x_cor.append(k)
                y_cor.append(months[k])
        return (x_cor, y_cor)


def str_to_date(date: str) -> d.datetime:
    """This helper function converts string dates to datetime objects

    Preconditions:
        - len(date) == 8 or len(date) == 10
        - all([e.isdigit() for e in date])
    """
    year = int(date[0:4])
    month = int(date[4:6])
    day = int(date[6:8])
    hour = 0
    if len(date) == 10:
        hour = int(date[8::]) - 1
    dt_obj = d.datetime(year, month, day, hour)
    return dt_obj


def help_average_day(row: List[int]) -> float:
    """This returns the emission average for
    a given day, given the row
     """
    day_vals = row[7: len(row)]
    return sum(day_vals) / len(day_vals)


def helper_header(row: List[str]) -> bool:
    """Helper function to determine if a string
    marks the beginning of the data header"""
    if len(row) < 2:
        return False
    item_2 = row[1]

    if "NAPS" in item_2 and "ID" in item_2:
        return True
    else:
        return False


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['csv', 'typing', 'datetime'],
        'allowed-io': ['helper_header', 'format',
                       'load', 'helper_is_valid_date',
                       'get_row', 'get_col',
                       'return_plot_hourly',
                       'help_average_day',
                       'return_plot_daily',
                       'return_plot_monthly'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
