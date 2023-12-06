import base
from freeCAD.my_API import get_displacement_magnitude
import random
from typing import Callable

def run_random_sampling(size: int):
    results = {}

    def create_random_input():
        young_modulus: float = base.YOUNG_MODULUS_MIN + random.uniform(0, 1) * base.YOUNG_MODULUS_SPAN 
        poisson_ratio: float = base.POISSON_RATIO_MIN + random.uniform(0, 1) * base.POISSON_RATIO_SPAN
        length: float = base.LENGTH_MIN + random.uniform(0, 1) * base.LENGTH_SPAN 
        width: float = base.WIDTH_MIN + base.WIDTH_SPAN 
        f1: float = base.F1_MIN + random.uniform(0, 1) * base.F1_SPAN
        f2: float = base.F2_MIN + random.uniform(0, 1) * base.F2_SPAN 
        f3: float = base.F3_MIN + random.uniform(0, 1) * base.F3_SPAN 
        f4: float = base.F4_MIN + random.uniform(0, 1) * base.F4_SPAN
        input = base.Input(young_modulus=young_modulus, poisson_ratio=poisson_ratio, length=length, width=width, f1=f1, f2=f2, f3=f3, f4=f4)
        return input

    for _ in range(size):   
        while (True):
            input = create_random_input()
            if (results.get(input) is None):
                break

        displacement = get_displacement_magnitude(input.length, input.width, input.f1, input.f2, input.f3, input.f4, f"{input.young_modulus} MPa", str(input.poisson_ratio))
        results.update({input: displacement})
    return results



def save_random_sampling(size: int):
    res = run_random_sampling(size)
    base.print_results_in_csv(res, f"random2-{size}.csv")
    res2 = run_random_sampling(size)
    base.print_results_in_csv(res2, f"random3-{size}.csv")









































def run_random_with_func(function: Callable[[float, float, float, float, float, float], float], min, max, number_of_samples: int):
    results = {}

    def get_real_val(min: float, max: float):
        return min + random.uniform(0, 1) * (max - min)

    for _ in range(number_of_samples): 
        A: float = get_real_val(min[0], max[0])
        B: float = get_real_val(min[1], max[1])
        C: float = get_real_val(min[2], max[2])
        D: float = get_real_val(min[3], max[3])
        E: float = get_real_val(min[4], max[4])
        F: float = get_real_val(min[5], max[5])

        res = function(A, B, C, D, E, F)   
        results.update({(A, B, C, D, E, F): res})
    return results   
