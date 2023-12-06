from spaceFilling import run_latin_hybercube_sampling, save_lhs_sampling_center, save_lhs_sampling_maximin, save_lhs_sampling_centermaximin, save_lhs_sampling_correlation, save_cvt_sampling
from adaptive import save_emukit_sampling_model_variance, save_emukit_sampling_model_variance_with_noise
from responseSurface import save_ccd_sampling, save_bb_sampling, save_bb_boxed_sampling, save_ccd_boxed_sampling, run_box_behnken_sampling_360
from classic import save_2_levelfullfactorial, save_placket_burman, save_2_levelfullfactorial
from optimal import save_d_optimal_design
from random_sampling import save_random_sampling
import base

sizes = [40, 50, 60, 80, 100, 120, 150, 200, 250, 300, 350, 400]

 
def run_space_filling_sampling(): 
    for size in sizes:
        save_lhs_sampling_center(size)
        save_lhs_sampling_maximin(size)
        save_lhs_sampling_centermaximin(size)
        save_lhs_sampling_correlation(size)  
        save_cvt_sampling(size)

def run_adaptive_sampling():
    save_emukit_sampling_model_variance(15, 25)
    save_emukit_sampling_model_variance(20, 40)
    save_emukit_sampling_model_variance(30, 50)
    save_emukit_sampling_model_variance(40, 60)
    save_emukit_sampling_model_variance(50, 70)

def run_adaptive_sampling_with_noise():
    percantage = 15
    save_emukit_sampling_model_variance_with_noise(15, 25, percantage)
    save_emukit_sampling_model_variance_with_noise(20, 40, percantage)
    save_emukit_sampling_model_variance_with_noise(30, 50, percantage)
    save_emukit_sampling_model_variance_with_noise(40, 60, percantage)
    save_emukit_sampling_model_variance_with_noise(50, 70, percantage)

def run_response_surface_sampling():  
    save_ccd_sampling()
    save_bb_sampling()

def run_response_surface_boxed_sampling():
    save_ccd_boxed_sampling()  
    save_bb_boxed_sampling()

def run_full_factorial_design():
    save_2_levelfullfactorial()
    save_placket_burman()

def run_optimal_design():
    for size in sizes:
        if size == 40:
            continue
        save_d_optimal_design(size)

def run_random_design():
    for size in sizes:
        save_random_sampling(size)



for size in [300, 350, 400]:
    save_cvt_sampling(size)

for size in sizes: 
    save_random_sampling(size)

