import dexpy.optimal
from dexpy.model import make_quadratic_model, ModelOrder
from patsy import dmatrix
from dexpy.design import coded_to_actual
import numpy as np
import base
from freeCAD.my_API import get_displacement_magnitude

def run_d_optimal_design(count: int):
    design = dexpy.optimal.build_optimal(8, run_count=count, order=ModelOrder.quadratic)

    design.columns = ["young_modulus", "poisson_ratio", "length", "width", "f1", "f2", "f3", "f4"]
    actual_lows = {"young_modulus": base.YOUNG_MODULUS_MIN, "poisson_ratio": base.POISSON_RATIO_MIN, "length": base.LENGTH_MIN, "width": base.WIDTH_MIN, "f1": base.F1_MIN, 
                   "f2": base.F2_MIN, "f3": base.F3_MIN, "f4": base.F4_MIN}
    actual_highs = {"young_modulus": base.YOUNG_MODULUS_MAX, "poisson_ratio": base.POISSON_RATIO_MAX, "length": base.LENGTH_MAX, "width": base.WIDTH_MAX, "f1": base.F1_MAX, 
                   "f2": base.F2_MAX, "f3": base.F3_MAX, "f4": base.F4_MAX}
    res = coded_to_actual(design, actual_lows, actual_highs)
    samples = res.values

    results = {}
    counter = 0
    duplicates = 0

    for sample in samples:
        young_modulus: float = round(sample[0], 4)
        poisson_ratio: float = round(sample[1], 4)
        length: float = round(sample[2], 4)
        width: float = round(sample[3], 4)
        f1: float = round(sample[4], 4)
        f2: float = round(sample[5], 4)
        f3: float = round(sample[6], 4)
        f4: float = round(sample[7], 4)
        input = base.Input(young_modulus=young_modulus, poisson_ratio=poisson_ratio, length=length, width=width, f1=f1, f2=f2, f3=f3, f4=f4)
        
        if (results.get(input) is not None):
                duplicates += 1
                continue
    
        displacement = get_displacement_magnitude(length, width, f1, f2, f3, f4, f"{young_modulus} MPa", str(poisson_ratio))
        results.update({input: displacement})

        counter += 1
        print("D-Optimal:"   + str(counter))
    
    print("Number of duplicates: " + str(duplicates))

    return results

def save_d_optimal_design(count: int):
    res = run_d_optimal_design(count)
    base.print_results_in_csv(res, f"d-optimal-{count}.csv")


