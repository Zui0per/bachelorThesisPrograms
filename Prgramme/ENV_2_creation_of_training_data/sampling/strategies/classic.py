from pyDOE2 import *
from freeCAD.my_API import get_displacement_magnitude
import base
from typing import Callable
import concurrent.futures

def get_real_val(val: float, min: float, max: float):
    if (val == 1):
        return max
    if (val == -1):
        return min

    raise AttributeError(val)

def run_level_fullfactorial():
    results = {}
    samples = ff2n(8)

    for sample in samples:
        young_modulus: float = get_real_val(sample[0], base.YOUNG_MODULUS_MIN, base.YOUNG_MODULUS_MAX)
        poisson_ratio: float = get_real_val(sample[1], base.POISSON_RATIO_MIN, base.POISSON_RATIO_MAX)
        length: float = get_real_val(sample[2], base.LENGTH_MIN, base.LENGTH_MAX)
        width: float = get_real_val(sample[3], base.WIDTH_MIN, base.WIDTH_MAX)
        f1: float = get_real_val(sample[4], base.F1_MIN, base.F1_MAX)
        f2: float = get_real_val(sample[5], base.F2_MIN, base.F2_MAX)
        f3: float = get_real_val(sample[6], base.F3_MIN, base.F3_MAX)
        f4: float = get_real_val(sample[7], base.F4_MIN, base.F4_MAX)
        input = base.Input(young_modulus=young_modulus, poisson_ratio=poisson_ratio, length=length, width=width, f1=f1, f2=f2, f3=f3, f4=f4)

        displacement = get_displacement_magnitude(length, width, f1, f2, f3, f4, f"{young_modulus} MPa", str(poisson_ratio))   
        results.update({input: displacement})
        
    return results

def run_level_fullfactorial_2box():

    YOUNG_MODULUS_MID = (base.YOUNG_MODULUS_MAX + base.YOUNG_MODULUS_MIN) / 2
    POISSON_RATIO_MID = (base.POISSON_RATIO_MAX + base.POISSON_RATIO_MIN) / 2
    LENGTH_MID = (base.LENGTH_MAX + base.LENGTH_MIN) / 2
    WIDTH_MID = (base.WIDTH_MAX + base.WIDTH_MIN) / 2
    F1_MID = (base.F1_MAX + base.F1_MIN) / 2
    F2_MID = (base.F2_MAX + base.F2_MIN) / 2
    F3_MID = (base.F3_MAX + base.F3_MIN) / 2
    F4_MID = (base.F4_MAX + base.F4_MIN) / 2

    results = {}
    samples = ff2n(8)
    counter = 0

    def get_real_val(val: float, min: float, max: float):
        if (val == 1):
            return round(max,3)
        if (val == -1):
            return round(min, 3)

        raise AttributeError(val)

    for sample in samples:
        young_modulus: float = get_real_val(sample[0], base.YOUNG_MODULUS_MIN, YOUNG_MODULUS_MID)
        poisson_ratio: float = get_real_val(sample[1], base.POISSON_RATIO_MIN, POISSON_RATIO_MID)
        length: float = get_real_val(sample[2], base.LENGTH_MIN, LENGTH_MID)
        width: float = get_real_val(sample[3], base.WIDTH_MIN, WIDTH_MID)
        f1: float = get_real_val(sample[4], base.F1_MIN, F1_MID)
        f2: float = get_real_val(sample[5], base.F2_MIN, F2_MID)
        f3: float = get_real_val(sample[6], base.F3_MIN, F3_MID)
        f4: float = get_real_val(sample[7], base.F4_MIN, F4_MID)
        input1 = base.Input(young_modulus=young_modulus, poisson_ratio=poisson_ratio, length=length, width=width, f1=f1, f2=f2, f3=f3, f4=f4)
        
        if (results.get(input1) is None):             
                displacement = get_displacement_magnitude(length, width, f1, f2, f3, f4, f"{young_modulus} MPa", str(poisson_ratio))            
                counter += 1
                print("FF-2box: " + str(counter))
                results.update({input1: displacement})

        young_modulus: float = get_real_val(sample[0], YOUNG_MODULUS_MID, base.YOUNG_MODULUS_MAX)
        poisson_ratio: float = get_real_val(sample[1], POISSON_RATIO_MID, base.POISSON_RATIO_MAX)
        length: float = get_real_val(sample[2], LENGTH_MID, base.LENGTH_MAX)
        width: float = get_real_val(sample[3], WIDTH_MID, base.WIDTH_MAX)
        f1: float = get_real_val(sample[4], F1_MID, base.F1_MAX)
        f2: float = get_real_val(sample[5], F2_MID, base.F2_MAX)
        f3: float = get_real_val(sample[6], F3_MID, base.F3_MAX)
        f4: float = get_real_val(sample[7], F4_MID, base.F4_MAX)
        input2 = base.Input(young_modulus=young_modulus, poisson_ratio=poisson_ratio, length=length, width=width, f1=f1, f2=f2, f3=f3, f4=f4)
        
        if (results.get(input2) is None):             
                displacement = get_displacement_magnitude(length, width, f1, f2, f3, f4, f"{young_modulus} MPa", str(poisson_ratio))            
                counter += 1
                print("FF-2box: " + str(counter))
                results.update({input2: displacement})
             
    return results

def save_2_levelfullfactorial():
    results = run_level_fullfactorial()
    base.print_results_in_csv(results, "2-level-full-factorial.csv")



def save_2_levelfullfactorial_2box():
    results = run_level_fullfactorial_2box()
    base.print_results_in_csv(results, "2-level-full-factorial-2box.csv")


def run_placket_burman():
    results = {}
    samples = pbdesign(8)
    for sample in samples:
        young_modulus: float = get_real_val(sample[0], base.YOUNG_MODULUS_MIN, base.YOUNG_MODULUS_MAX)
        poisson_ratio: float = get_real_val(sample[1], base.POISSON_RATIO_MIN, base.POISSON_RATIO_MAX)
        length: float = get_real_val(sample[2], base.LENGTH_MIN, base.LENGTH_MAX)
        width: float = get_real_val(sample[3], base.WIDTH_MIN, base.WIDTH_MAX)
        f1: float = get_real_val(sample[4], base.F1_MIN, base.F1_MAX)
        f2: float = get_real_val(sample[5], base.F2_MIN, base.F2_MAX)
        f3: float = get_real_val(sample[6], base.F3_MIN, base.F3_MAX)
        f4: float = get_real_val(sample[7], base.F4_MIN, base.F4_MAX)
        input = base.Input(young_modulus=young_modulus, poisson_ratio=poisson_ratio, length=length, width=width, f1=f1, f2=f2, f3=f3, f4=f4)

        displacement = get_displacement_magnitude(length, width, f1, f2, f3, f4, f"{young_modulus} MPa", str(poisson_ratio))   
        results.update({input: displacement})
    return results

def save_placket_burman():
    res = run_placket_burman()
    base.print_results_in_csv(res, "placket-burman.csv")












def run_full_factorial_with_func(function: Callable[[float, float, float, float, float, float], float], min, max):
    results = {}
    samples = ff2n(6)

    for sample in samples:
        A: float = get_real_val(sample[0], min[0], max[0])
        B: float = get_real_val(sample[1], min[1], max[1])
        C: float = get_real_val(sample[2], min[2], max[2])
        D: float = get_real_val(sample[3], min[3], max[3])
        E: float = get_real_val(sample[4], min[4], max[4])
        F: float = get_real_val(sample[5], min[5], max[5])
        
        res = function(A, B, C, D, E, F)   
        results.update({(A, B, C, D, E, F): res})
        
    return results




def run_placket_burman_with_func(function: Callable[[float, float, float, float, float, float], float], min, max):
    results = {}
    samples = pbdesign(6)
    for sample in samples:
        A: float = get_real_val(sample[0], min[0], max[0])
        B: float = get_real_val(sample[1], min[1], max[1])
        C: float = get_real_val(sample[2], min[2], max[2])
        D: float = get_real_val(sample[3], min[3], max[3])
        E: float = get_real_val(sample[4], min[4], max[4])
        F: float = get_real_val(sample[5], min[5], max[5])
        
        res = function(A, B, C, D, E, F)   
        results.update({(A, B, C, D, E, F): res})
        
    return results