from typing import Dict, Callable
import pyDOE2
from freeCAD.my_API import get_displacement_magnitude
import base 
from idaes.core.surrogate.pysmo.sampling import CVTSampling
import json
import os
import locale

def run_latin_hybercube_sampling(number_of_samples: int, criterion: str) -> Dict[base.Input, float]:
    results = {}
    samples = pyDOE2.lhs(8, number_of_samples, criterion)
    print(samples)
    counter = 0
    for sample in samples:
            young_modulus: float = round(base.YOUNG_MODULUS_MIN + base.YOUNG_MODULUS_SPAN * sample[0], 4)
            poisson_ratio: float = round(base.POISSON_RATIO_MIN + base.POISSON_RATIO_SPAN * sample[1], 4)
            length: float = round(base.LENGTH_MIN + base.LENGTH_SPAN * sample[2], 4)
            width: float = round(base.WIDTH_MIN + base.WIDTH_SPAN * sample[3], 4)
            f1: float = round(base.F1_MIN + base.F1_SPAN * sample[4], 4)
            f2: float = round(base.F2_MIN + base.F2_SPAN * sample[5], 4)
            f3: float = round(base.F3_MIN + base.F3_SPAN * sample[6], 4)
            f4: float = round(base.F4_MIN + base.F4_SPAN * sample[7], 4)
            input = base.Input(young_modulus=young_modulus, poisson_ratio=poisson_ratio, length=length, width=width, f1=f1, f2=f2, f3=f3, f4=f4)
            
            if (results.get(input) is not None):
                  raise Exception("No duplicates allowed!")

            
            counter += 1

            displacement = get_displacement_magnitude(length, width, f1, f2, f3, f4, f"{young_modulus} MPa", str(poisson_ratio))
            print("LHS-" + criterion + ": "  + str(counter) + "|" + str(displacement))

            results.update({input: displacement})
    return results

def save_lhs_sampling_center(size: int):
      res = run_latin_hybercube_sampling(size, 'center')
      base.print_results_in_csv(res, f"lhs-center1-{size}.csv")
      res2 = run_latin_hybercube_sampling(size, 'center')
      base.print_results_in_csv(res2, f"lhs-center2-{size}.csv")
      res3 = run_latin_hybercube_sampling(size, 'center')
      base.print_results_in_csv(res3, f"lhs-center3-{size}.csv")

def save_lhs_sampling_maximin(size):
    res = run_latin_hybercube_sampling(size, 'maximin')
    base.print_results_in_csv(res, f"lhs-maximin1-{size}.csv")
    res2 = run_latin_hybercube_sampling(size, 'maximin')
    base.print_results_in_csv(res2, f"lhs-maximin2-{size}.csv")
    res3 = run_latin_hybercube_sampling(size, 'maximin')
    base.print_results_in_csv(res3, f"lhs-maximin3-{size}.csv")

def save_lhs_sampling_centermaximin(size):
    res = run_latin_hybercube_sampling(size, 'centermaximin')
    base.print_results_in_csv(res, f"lhs-centermaximin1-{size}.csv")
    res2 = run_latin_hybercube_sampling(size, 'centermaximin')
    base.print_results_in_csv(res2, f"lhs-centermaximin2-{size}.csv")
    res3 = run_latin_hybercube_sampling(size, 'centermaximin')
    base.print_results_in_csv(res3, f"lhs-centermaximin3-{size}.csv")

def save_lhs_sampling_correlation(size):
    res = run_latin_hybercube_sampling(size, 'correlation')
    base.print_results_in_csv(res, f"lhs-correlation1-{size}.csv")
    res2 = run_latin_hybercube_sampling(size, 'correlation')
    base.print_results_in_csv(res2, f"lhs-correlation2-{size}.csv")
    res3 = run_latin_hybercube_sampling(size, 'correlation')
    base.print_results_in_csv(res3, f"lhs-correlation3-{size}.csv")


def run_centroidal_voronoi_tesselation(size):
    data_bounds = [[base.YOUNG_MODULUS_MIN, base.POISSON_RATIO_MIN, base.LENGTH_MIN, base.WIDTH_MIN, base.F1_MIN, base.F2_MIN, base.F3_MIN, base.F4_MIN],
                   [base.YOUNG_MODULUS_MAX, base.POISSON_RATIO_MAX, base.LENGTH_MAX, base.WIDTH_MAX, base.F1_MAX, base.F2_MAX, base.F3_MAX, base.F4_MAX]]
    b = CVTSampling(data_bounds, size, sampling_type="creation")
    samples = b.sample_points()
    results = {}
    counter = 0
    for sample in samples:
        young_modulus: float = sample[0]
        poisson_ratio: float = sample[1]
        length: float = sample[2]
        width: float = sample[3]
        f1: float = sample[4]
        f2: float = sample[5]
        f3: float = sample[6]
        f4: float = sample[7]
        input = base.Input(young_modulus=young_modulus, poisson_ratio=poisson_ratio, length=length, width=width, f1=f1, f2=f2, f3=f3, f4=f4)
        
        if (results.get(input) is not None):
                raise Exception("No duplicates allowed!")

        displacement = get_displacement_magnitude(length, width, f1, f2, f3, f4, f"{young_modulus} MPa", str(poisson_ratio))

        counter += 1
        print("CVT: "  + str(counter))

        results.update({input: displacement})
    return results

def save_cvt_sampling(size: int):
    res = run_centroidal_voronoi_tesselation(size)
    base.print_results_in_csv(res, f"CVR2-{size}.csv")

    res = run_centroidal_voronoi_tesselation(size)
    base.print_results_in_csv(res, f"CVR3-{size}.csv")





















def run_lhs_with_func(function: Callable[[float, float, float, float, float, float], float], min, max, number_of_samples: int, criterion: str):
    results = {}
    samples = pyDOE2.lhs(6, number_of_samples, criterion)

    def get_real_val(percentage: float, min: float, max: float):
        span = max - min
        return round(min + span * percentage, 4)

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


def run_cvt_with_func(function: Callable[[float, float, float, float, float, float], float], min, max, number_of_samples: int):
    data_bounds = [min, max]
    b = CVTSampling(data_bounds, number_of_samples, sampling_type="creation")
    samples = b.sample_points()
    print(samples)
    results = {}

    for sample in samples:
        A: float = sample[0]
        B: float = sample[1]
        C: float = sample[2]
        D: float = sample[3]
        E: float = sample[4]
        F: float = sample[5]

        res = function(A, B, C, D, E, F)   
        results.update({(A, B, C, D, E, F): res})

    return results



































































































































def create_sample_input_file(file_name: str, count: int):
    samples = pyDOE2.lhs(8, count, "center")
    count = len(samples)
    with open(f'{file_name}.json', 'w') as file:
        json.dump(samples.tolist(), file)


def save_and_run_lhs_center_with_input_file(input_file: str, res_file: str):
    
    if (res_file not in os.listdir()):
        with open(res_file, "x") as res_file:
            res_file.write("young_modulus; poisson_ratio; length; width; f1; f2; f3; f4; displacement \n")
    
    sample_array: list = json.load(open(input_file, "r"))
    try:   
        with open(f"{res_file}", "a") as file:
             
            while sample_array:
                print("Left: "  + str(len(sample_array)))

                sample = sample_array[-1]

                young_modulus: float = round(base.YOUNG_MODULUS_MIN + base.YOUNG_MODULUS_SPAN * round(sample[0], 3), 4)
                poisson_ratio: float = round(base.POISSON_RATIO_MIN + base.POISSON_RATIO_SPAN * round(sample[1], 3), 4)
                length: float = round(base.LENGTH_MIN + base.LENGTH_SPAN * round(sample[2], 3), 4)
                width: float = round(base.WIDTH_MIN + base.WIDTH_SPAN * round(sample[3], 3), 3)
                f1: float = round(base.F1_MIN + base.F1_SPAN * round(sample[4], 3), 4)
                f2: float = round(base.F2_MIN + base.F2_SPAN * round(sample[5], 3), 4)
                f3: float = round(base.F3_MIN + base.F3_SPAN * round(sample[6], 3), 4)
                f4: float = round(base.F4_MIN + base.F4_SPAN * round(sample[7], 3), 4)
                
                displacement = get_displacement_magnitude(length, width, f1, f2, f3, f4, f"{young_modulus} MPa", str(poisson_ratio))
                file.write(locale.format("%.4f", young_modulus) + ";" + locale.format("%.4f", poisson_ratio) + ";" + locale.format("%.4f", length) + ";"
                            + locale.format("%.4f", width) + ";" + locale.format("%.4f", f1) + ";" + locale.format("%.4f", f2) + ";" + locale.format("%.4f", f3) + ";" +
                            locale.format("%.4f", f4) + ";" + locale.format("%.4f", displacement) + "\n")
                
                sample_array.pop()
                         
    except Exception as e:
        print(e)
        with open(input_file, "w") as samples_file:
            json.dump(sample_array, samples_file)

    

#create_sample_input_file("10.000_samples", 10000)
#save_and_run_lhs_center_with_input_file("10.000_samples.json", "lhs-center-10.000.csv")