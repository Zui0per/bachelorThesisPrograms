from typing import Dict
import numpy as np
import pyDOE2
from freeCAD.my_API import get_displacement_magnitude
import base 
import GPy
from emukit.experimental_design.acquisitions import ModelVariance, IntegratedVarianceReduction
from emukit.experimental_design.experimental_design_loop import ExperimentalDesignLoop
from emukit.core import ParameterSpace, ContinuousParameter
from emukit.core.loop import OuterLoop
from GPy.models import GPRegression
from GPy.kern import RBF
from typing import Callable
from emukit.model_wrappers import GPyModelWrapper


def add_noise_to_disp(displacement: float, percantage: int):
    valueRange = 347.53 - 0.745
    noise_dis = valueRange * np.random.random() * float(percantage/100)
    direction=np.random.randint(0,2)
    if (direction == 0):
        return (displacement + noise_dis)
    else:
        return (displacement - noise_dis)

def run_emukit_sampling_with_noise(number_of_samples: int, number_of_lhs_samples: int, acquisition: str, percantage: int):
    results = {}

    #initial LH sampling    
    X_init = []
    Y_init = []
    counter = 0
    samples = pyDOE2.lhs(8, number_of_lhs_samples, 'center')
    for sample in samples:
        young_modulus: float = base.YOUNG_MODULUS_MIN + base.YOUNG_MODULUS_SPAN * sample[0]
        poisson_ratio: float = base.POISSON_RATIO_MIN + base.POISSON_RATIO_SPAN * sample[1]
        length: float = base.LENGTH_MIN + base.LENGTH_SPAN * sample[2]
        width: float = base.WIDTH_MIN + base.WIDTH_SPAN * sample[3]
        f1: float = base.F1_MIN + base.F1_SPAN * sample[4]
        f2: float = base.F2_MIN + base.F2_SPAN * sample[5]
        f3: float = base.F3_MIN + base.F3_SPAN * sample[6]
        f4: float = base.F4_MIN + base.F4_SPAN * sample[7]
        input = base.Input(young_modulus=young_modulus, poisson_ratio=poisson_ratio, length=length, width=width, f1=f1, f2=f2, f3=f3, f4=f4)
        displacement = get_displacement_magnitude(length, width, f1, f2, f3, f4, f"{young_modulus} MPa", str(poisson_ratio))

        displacement_with_noise = add_noise_to_disp(displacement, percantage)
        results.update({input: displacement_with_noise})

        X_init.append([length, width, f1, f2, f3, f4, young_modulus, poisson_ratio])
        Y_init.append([displacement])
        counter += 1
        print("LHS: " + str(counter))

    counter = 0

    def get_displacement_magnitude_with_list_param(list):
        list = list[0]
        input = base.Input(length=list[0], width=list[1], f1=list[2], f2=list[3], f3=list[4], f4=list[5], young_modulus=list[6], poisson_ratio=list[7])
        displacement = get_displacement_magnitude(list[0], list[1], list[2], list[3], list[4], list[5], f"{list[6]} MPa", str(list[7]))
        displacement_with_noise = add_noise_to_disp(displacement, percantage)
        results.update({input: displacement_with_noise})

        print("Emukit step done")

        return np.array([[np.round(displacement, 4)]], dtype=float)
        
    # define input space
    params = [ContinuousParameter("length", base.LENGTH_MIN, base.LENGTH_MAX),
                ContinuousParameter("width", base.WIDTH_MIN, base.WIDTH_MAX), 
                ContinuousParameter("force1", base.F1_MIN, base.F1_MAX),
                ContinuousParameter("force2", base.F2_MIN, base.F2_MAX), 
                ContinuousParameter("force3", base.F3_MIN, base.F3_MAX),
                ContinuousParameter("force4", base.F4_MIN, base.F4_MAX),
                ContinuousParameter("young_modulus", base.YOUNG_MODULUS_MIN, base.YOUNG_MODULUS_MAX),
                ContinuousParameter("poisson_ratio", base.POISSON_RATIO_MIN, base.POISSON_RATIO_MAX)]
    space = ParameterSpace(params)

    #model
    X = np.array(X_init, dtype=float)
    Y = np.array(Y_init, dtype=float)

    # Hyperparameter ergänzen Xingyu email!
    ker = GPy.kern.Bias(input_dim=8) + GPy.kern.Bias(1.0) * GPy.kern.RBF(input_dim=8, variance=1., lengthscale=1.,ARD=True) + GPy.kern.White(1)
    model_gpy = GPRegression(X, Y, kernel=ker)
    model_wrapper = GPyModelWrapper(model_gpy)

    if acquisition == "model variance":
        acq = ModelVariance(model_wrapper)    
    elif acquisition == "variance reduction":
        acq = IntegratedVarianceReduction(model_wrapper, space)
    else:
        raise Exception("Acquisition of type " + acquisition + "not available!")

    ed_loop = ExperimentalDesignLoop(space=space, model=model_wrapper, acquisition=acq)
    ed_loop.run_loop(get_displacement_magnitude_with_list_param, number_of_samples)
    return results

def run_emukit_sampling(number_of_samples: int, number_of_lhs_samples: int, acquisition: str):
    results = {}

    #initial LH sampling    
    X_init = []
    Y_init = []
    counter = 0
    samples = pyDOE2.lhs(8, number_of_lhs_samples, 'center')
    for sample in samples:
        young_modulus: float = base.YOUNG_MODULUS_MIN + base.YOUNG_MODULUS_SPAN * sample[0]
        poisson_ratio: float = base.POISSON_RATIO_MIN + base.POISSON_RATIO_SPAN * sample[1]
        length: float = base.LENGTH_MIN + base.LENGTH_SPAN * sample[2]
        width: float = base.WIDTH_MIN + base.WIDTH_SPAN * sample[3]
        f1: float = base.F1_MIN + base.F1_SPAN * sample[4]
        f2: float = base.F2_MIN + base.F2_SPAN * sample[5]
        f3: float = base.F3_MIN + base.F3_SPAN * sample[6]
        f4: float = base.F4_MIN + base.F4_SPAN * sample[7]
        input = base.Input(young_modulus=young_modulus, poisson_ratio=poisson_ratio, length=length, width=width, f1=f1, f2=f2, f3=f3, f4=f4)
        displacement = get_displacement_magnitude(length, width, f1, f2, f3, f4, f"{young_modulus} MPa", str(poisson_ratio))

        results.update({input: displacement})

        X_init.append([length, width, f1, f2, f3, f4, young_modulus, poisson_ratio])
        Y_init.append([displacement])
        counter += 1
        print("LHS: " + str(counter))

    counter = 0

    def get_displacement_magnitude_with_list_param(list):
        list = list[0]
        input = base.Input(length=list[0], width=list[1], f1=list[2], f2=list[3], f3=list[4], f4=list[5], young_modulus=list[6], poisson_ratio=list[7])
        displacement = get_displacement_magnitude(list[0], list[1], list[2], list[3], list[4], list[5], f"{list[6]} MPa", str(list[7]))
        results.update({input: displacement})

        print("Emukit step done")

        return np.array([[np.round(displacement, 4)]], dtype=float)
        
    # define input space
    params = [ContinuousParameter("length", base.LENGTH_MIN, base.LENGTH_MAX),
                ContinuousParameter("width", base.WIDTH_MIN, base.WIDTH_MAX), 
                ContinuousParameter("force1", base.F1_MIN, base.F1_MAX),
                ContinuousParameter("force2", base.F2_MIN, base.F2_MAX), 
                ContinuousParameter("force3", base.F3_MIN, base.F3_MAX),
                ContinuousParameter("force4", base.F4_MIN, base.F4_MAX),
                ContinuousParameter("young_modulus", base.YOUNG_MODULUS_MIN, base.YOUNG_MODULUS_MAX),
                ContinuousParameter("poisson_ratio", base.POISSON_RATIO_MIN, base.POISSON_RATIO_MAX)]
    space = ParameterSpace(params)

    #model
    X = np.array(X_init, dtype=float)
    Y = np.array(Y_init, dtype=float)

    # Hyperparameter ergänzen Xingyu email!
    ker = GPy.kern.Bias(input_dim=8) + GPy.kern.Bias(1.0) * GPy.kern.RBF(input_dim=8, variance=1., lengthscale=1.,ARD=True) + GPy.kern.White(1)
    model_gpy = GPRegression(X, Y, kernel=ker)
    model_wrapper = GPyModelWrapper(model_gpy)

    if acquisition == "model variance":
        acq = ModelVariance(model_wrapper)    
    elif acquisition == "variance reduction":
        acq = IntegratedVarianceReduction(model_wrapper, space)
    else:
        raise Exception("Acquisition of type " + acquisition + "not available!")

    ed_loop = ExperimentalDesignLoop(space=space, model=model_wrapper, acquisition=acq)
    ed_loop.run_loop(get_displacement_magnitude_with_list_param, number_of_samples) #220
    return results


def save_emukit_sampling_model_variance(size: int, lhs_size: int):
    res = run_emukit_sampling(size, lhs_size, "model variance")
    base.print_results_in_csv(res, f"emukit-with-model-variance-{size+lhs_size}-init-{lhs_size}.csv")

def save_emukit_sampling_model_variance_with_noise(size: int, lhs_size: int, percantage: int):
    res = run_emukit_sampling_with_noise(size, lhs_size, "model variance", percantage)
    base.print_results_in_csv(res, f"emukit-with-model-variance-{size+lhs_size}-init-{lhs_size}-noise-{percantage}.csv")

 



save_emukit_sampling_model_variance(175, 175)
save_emukit_sampling_model_variance(200, 200)


































def run_emukit_with_func(acquisition: str, function: Callable[[float, float, float, float, float, float], float], min, max, lhs_samples: int, number_of_samples: int):
    results = {}

    X_init = []
    Y_init = []
    samples = pyDOE2.lhs(6, lhs_samples, 'center')

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

        X_init.append([A, B, C, D, E, F])
        Y_init.append([res])   

    def get_func_res(list):
        list = list[0]
        res = function(list[0], list[1], list[2], list[3], list[4], list[5])
        results.update({tuple(list): res})

        return np.array([[np.round(res, 4)]], dtype=float)
        
    # define input space
    params = [ContinuousParameter("A", min[0], max[0]),
                ContinuousParameter("B", min[1], max[1]), 
                ContinuousParameter("C", min[2], max[2]),
                ContinuousParameter("D", min[3], max[3]), 
                ContinuousParameter("E", min[4], max[4]),
                ContinuousParameter("F", min[5], max[5])]
    
    space = ParameterSpace(params)

    #model
    X = np.array(X_init, dtype=float)
    Y = np.array(Y_init, dtype=float)

    # Hyperparameter ergänzen Xingyu email!
    ker = GPy.kern.Bias(input_dim=6) + GPy.kern.Bias(1.0) * GPy.kern.RBF(input_dim=6, variance=1., lengthscale=1.,ARD=True) + GPy.kern.White(1)
    model_gpy = GPRegression(X, Y, kernel=ker)
    model_wrapper = GPyModelWrapper(model_gpy)

    if acquisition == "model variance":
        acq = ModelVariance(model_wrapper)    
    elif acquisition == "variance reduction":
        acq = IntegratedVarianceReduction(model_wrapper, space)
    else:
        raise Exception("Acquisition of type " + acquisition + "not available!")

    ed_loop = ExperimentalDesignLoop(space=space, model=model_wrapper, acquisition=acq)
    ed_loop.run_loop(get_func_res, number_of_samples) 

    return results
























