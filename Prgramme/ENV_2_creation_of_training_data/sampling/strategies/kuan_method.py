import base 
import numpy as np
import GPy
from emukit.experimental_design.acquisitions import ModelVariance, IntegratedVarianceReduction
from emukit.experimental_design.experimental_design_loop import ExperimentalDesignLoop
from emukit.core.optimization import LocalSearchAcquisitionOptimizer
from emukit.core import ParameterSpace, ContinuousParameter
from emukit.core.loop import OuterLoop
from GPy.models import GPRegression
from GPy.kern import RBF
from emukit.model_wrappers import GPyModelWrapper
from my_acqusition import SmallDataContextAcquisition
from my_emukit_loop import SmallDataContextLoop
import scipy.stats as stats
import matplotlib.pyplot as plt
from emukit.test_functions import forrester_function
from typing import List
import math

def calculate_error_variance_of_group(list: List, real_val: float):
    error_variance = 0
    for el in list:
        error_variance = error_variance + (el-real_val)**2
    return error_variance

def calculate_total_error_variance(list: List, real_values: List):
    total_variance = 0
    number_of_groups = len(list)
    for i in range(number_of_groups):
        total_variance = total_variance + calculate_error_variance_of_group(list[i], real_values[i])
    return total_variance


def kuan_sampling_test():
    target_function, space = forrester_function()

    #X_init = np.array([[0.2],[0.6], [0.9]])
    X_init = np.array([[0.2], [0.9]])
    Y_init = target_function(X_init)

    y_real_at_02 = Y_init[0][0]
    y_real_at_09 = Y_init[1][0]
    res_02 = np.random.normal(y_real_at_02, 0.1, size=3)
    res_09 = np.random.normal(y_real_at_09, 0.1, size=3)

    f_statistic, p_value = stats.f_oneway(res_02, res_09)
    total_error_variance = calculate_total_error_variance([res_02, res_09], [y_real_at_02, y_real_at_09])
    N = 6 #total number of samples
    p = 2 #number of groups
    error_df = N - p
    prediction_df = p - 1

    relative_error_variance = total_error_variance / error_df
    f_crit = stats.f.ppf(q=1-.05, dfn=prediction_df, dfd=error_df)

    bgv_res = math.sqrt(f_crit * relative_error_variance)
    

    


    gpy_model = GPy.models.GPRegression(X_init, Y_init, GPy.kern.RBF(1, lengthscale=0.08, variance=20), noise_var=1e-10)
    emukit_model = GPyModelWrapper(gpy_model)
  
    acq = SmallDataContextAcquisition(model=emukit_model, acquisition=ModelVariance(emukit_model), bgv_res=[bgv_res])    

    #ed_loop = ExperimentalDesignLoop(space=space, model=emukit_model, acquisition=acq, acquisition_optimizer=LocalSearchAcquisitionOptimizer(space))
    acq = ModelVariance(emukit_model)
    ed_loop = SmallDataContextLoop(space=space, model=emukit_model, acquisition=acq)
    ed_loop.run(user_function=target_function, stopping_condition=10) 


kuan_sampling_test()