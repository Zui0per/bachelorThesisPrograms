import locale
from collections import namedtuple
from typing import Dict
from os import listdir

YOUNG_MODULUS_MIN = 60000
YOUNG_MODULUS_MAX = 500000
YOUNG_MODULUS_SPAN = YOUNG_MODULUS_MAX - YOUNG_MODULUS_MIN

POISSON_RATIO_MIN = 0.1
POISSON_RATIO_MAX = 0.45
POISSON_RATIO_SPAN = POISSON_RATIO_MAX - POISSON_RATIO_MIN

LENGTH_MIN = 8000
LENGTH_MAX = 10000
LENGTH_SPAN = LENGTH_MAX - LENGTH_MIN

WIDTH_MIN = 1000
WIDTH_MAX = 2000
WIDTH_SPAN = WIDTH_MAX - WIDTH_MIN

F1_MIN = 1000000
F1_MAX = 10000000
F1_SPAN = F1_MAX - F1_MIN

F2_MIN = 1000000
F2_MAX = 5000000
F2_SPAN = F2_MAX - F2_MIN

F3_MIN = 1000000
F3_MAX = 10000000
F3_SPAN = F3_MAX - F3_MIN

F4_MIN = 1000000
F4_MAX = 5000000
F4_SPAN = F4_MAX - F4_MIN

locale.setlocale(locale.LC_ALL, "de_DE.utf8")
Input = namedtuple("Input", ["young_modulus", "poisson_ratio", "length", "width", "f1", "f2", "f3", "f4"])

def print_results_in_csv(res: Dict[Input, float], name: str):
    with open(name, "x") as file:
        file.write("young_modulus; poisson_ratio; length; width; f1; f2; f3; f4; displacement \n")
        for input, displacement in res.items():
            length: float = input.length
            width: float = input.width
            f1: float = input.f1
            f2: float = input.f2
            f3: float = input.f3
            f4: float = input.f4
            young_modulus: float = input.young_modulus
            poisson_ratio: float = input.poisson_ratio

            file.write(locale.format("%.4f", young_modulus) + ";" + locale.format("%.4f", poisson_ratio) + ";" + locale.format("%.4f", length) + ";"
                        + locale.format("%.4f", width) + ";" + locale.format("%.4f", f1) + ";" + locale.format("%.4f", f2) + ";" + locale.format("%.4f", f3) + ";" +
                          locale.format("%.4f", f4) + ";" + locale.format("%.4f", displacement) + "\n")

def get_results_from_csv_as_dict(fileName: str): 
    results = {}
    with open(fileName, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            cells: list[str] = line.split(';')
            cells = list(map(lambda cell: cell.replace(",", "."), cells))
            results.update({(float(cells[0]), float(cells[1]), float(cells[2]), float(cells[3]), float(cells[4]), float(cells[5]), float(cells[6]), float(cells[7])): float(cells[8])})
    return results

def get_results_form_csv(fileName: str):
    X = []
    Y = []

    def transform_string_cell_to_float(cell: str) -> float:
        cell = cell.replace(",", ".")
        return float(cell)

    with open(fileName, "r") as file:
        lines = file.readlines()
        for line in lines[1:]:
            cells = [x.strip() for x in line.split(';')]
            cells = list(map(transform_string_cell_to_float, cells))
            last = cells.pop()
            X.append(cells[:8])
            Y.append(last)

    return [X, Y]


