from pyDOE2 import lhs
from idaes.core.surrogate.pysmo.sampling import CVTSampling
from scipy.stats.qmc import discrepancy, Sobol, Halton
import random
import numpy as np
import codecs, json
import os
import math
import matplotlib.pyplot as plt
from autosklearn.pipeline.components.regression import RegressorChoice

for name in RegressorChoice.get_components():
    print(name)


def run_random(size: int):
    res = []

    for _ in range(size):
        res.append([random.uniform(0, 1),
            random.uniform(0, 1),
            random.uniform(0, 1),
            random.uniform(0, 1),
            random.uniform(0, 1),
            random.uniform(0, 1), 
            random.uniform(0, 1),
            random.uniform(0, 1)
        ])
    return res

def run_cvt(size: int):

    if (f"CVT_{size}.json" in os.listdir()):
        obj_text = codecs.open(f"CVT_{size}.json", 'r', encoding='utf-8').read()
        samples = json.loads(obj_text)
        return np.array(samples)
    else:
        data_bounds = [[0, 0, 0, 0, 0, 0, 0, 0],
                    [1, 1, 1, 1, 1, 1, 1, 1]]
        #data_bounds = [[0, 0],
        #            [1, 1]]
        cvt = CVTSampling(data_bounds, size, sampling_type="creation")
        samples = cvt.sample_points()

        json.dump(samples.tolist(), codecs.open(f"CVT_{size}_2d.json", 'w', encoding='utf-8'), 
            separators=(',', ':'), 
            sort_keys=True, 
            indent=4) 
    
        return samples


def calc_euclidian_distance(point_1, point_2):
    return np.linalg.norm(np.array(point_1) - np.array(point_2))

def calc_maximin_distance_criterion(samples):
    min_dis = math.inf
    for i in range(len(samples)):
        for j in range(i+1, len(samples)):
            dis = calc_euclidian_distance(samples[i], samples[j])
            if (dis < min_dis):
                min_dis = dis

    return min_dis

def calc_min_infinity_norm(point_1, point_2):
    return abs(min(np.array(point_1) - np.array(point_2), key=abs))

def calc_min_projected_distance(samples):
    min_dis = math.inf
    for i in range(len(samples)):
        for j in range(i+1, len(samples)):
            dis = calc_min_infinity_norm(samples[i], samples[j])
            if (dis < min_dis):
                min_dis = dis

    return min_dis




res_lhs_center_disc = []
res_lhs_center_maximin = []
res_lhs_center_projected_dis = []
res_lhs_center_disc_d = []
res_lhs_center_maximin_d = []
res_lhs_center_projected_dis_d = []


res_lhs_maximin_disc = []
res_lhs_maximin_maximin = []
res_lhs_maximin_projected_dis = []

res_lhs_correlation_disc = []
res_lhs_correlation_maximin = []
res_lhs_correlation_projected_dis = []

res_lhs_centermaximin_disc = []
res_lhs_centermaximin_maximin = []
res_lhs_centermaximin_projected_dis = []

res_cvt_disc = [] 
res_cvt_maximin = []
res_cvt_projected_dis = []

res_sobol_disc = [] 
res_sobol_maximin = []
res_sobol_projected_dis = []

res_halton_disc = [] 
res_halton_maximin = []
res_halton_projected_dis = []

res_random_disc = [] 
res_random_maximin = [] 
res_ramdom_projected_dis = []

def calc_criterions(size: int):
    dim = 8
    lhs_center = lhs(dim, size, 'center')
    lhs_maximin = lhs(dim, size, 'maximin')
    lhs_correlation = lhs(dim, size, 'correlation')
    lhs_centermaximin = lhs(dim, size, 'centermaximin')

    lhs_center_double = lhs(dim, size, 'center')
    a = lhs_center_double[0]
    a[0] = a[0] + 0.005
    lhs_center_d = np.append(lhs_center_double, [a], axis=0)
    print(lhs_center_d.size)
    print(lhs_center.size)
    # -----------------------

    cvt = run_cvt(size)

    sobol = Sobol(d=dim).random(size)
    halton = Halton(d=dim).random(size)

    random = run_random(size)

    res_lhs_center_disc.append(discrepancy(lhs_center))
    res_lhs_center_maximin.append(calc_maximin_distance_criterion(lhs_center))
    res_lhs_center_projected_dis.append(calc_min_projected_distance(lhs_center))
    res_lhs_center_disc_d.append(discrepancy(lhs_center_d))
    res_lhs_center_maximin_d.append(calc_maximin_distance_criterion(lhs_center_d))
    res_lhs_center_projected_dis_d.append(calc_min_projected_distance(lhs_center_d))

    res_lhs_maximin_disc.append(discrepancy(lhs_maximin))
    res_lhs_maximin_maximin.append(calc_maximin_distance_criterion(lhs_maximin))
    res_lhs_maximin_projected_dis.append(calc_min_projected_distance(lhs_maximin))

    res_lhs_correlation_disc.append(discrepancy(lhs_correlation))
    res_lhs_correlation_maximin.append(calc_maximin_distance_criterion(lhs_correlation))
    res_lhs_correlation_projected_dis.append(calc_min_projected_distance(lhs_correlation))

    res_lhs_centermaximin_disc.append(discrepancy(lhs_centermaximin))
    res_lhs_centermaximin_maximin.append(calc_maximin_distance_criterion(lhs_centermaximin))
    res_lhs_centermaximin_projected_dis.append(calc_min_projected_distance(lhs_centermaximin))

    res_cvt_disc.append(discrepancy(cvt))
    res_cvt_maximin.append(calc_maximin_distance_criterion(cvt))
    res_cvt_projected_dis.append(calc_min_projected_distance(cvt))

    res_sobol_disc.append(discrepancy(sobol)) 
    res_sobol_maximin.append(calc_maximin_distance_criterion(sobol))
    res_sobol_projected_dis.append(calc_min_projected_distance(sobol))
    
    res_halton_disc.append(discrepancy(halton)) 
    res_halton_maximin.append(calc_maximin_distance_criterion(halton))
    res_halton_projected_dis.append(calc_min_projected_distance(halton))

    res_random_disc.append(discrepancy(random))
    res_random_maximin.append(calc_maximin_distance_criterion(random))
    res_ramdom_projected_dis.append(calc_min_projected_distance(random))

    print("-----------------------------------------")
    print(f"size {size} done")
    print("-----------------------------------------")

for size in [40, 60, 80, 100, 120, 150, 200, 250]:
    calc_criterions(size)

x = [40, 60, 80, 100, 120, 150, 200, 250]

linewidth = 2
plt.figure(figsize=(12, 6))
plt.plot(x, res_lhs_center_disc, label="LHS-center", color="#FFF700", linewidth=linewidth)
plt.plot(x, res_lhs_maximin_disc, label="LHS-maximin", color="#053908", linewidth=linewidth)
plt.plot(x, res_lhs_correlation_disc, label="LHS-correlation", color="#5FA163", linewidth=linewidth)
plt.plot(x, res_lhs_centermaximin_disc, label="LHS-centermaximin", color="#BEE239", linewidth=linewidth)
#plt.plot(x, res_lhs_center_disc_d, label="LHS-center_d", color="red")

plt.plot(x, res_cvt_disc, label="CVT", color="#FF8F00", linewidth=linewidth)
plt.plot(x, res_sobol_disc, label="Sobol", color="#ff4fc1", linewidth=linewidth)
plt.plot(x, res_halton_disc, label="Halton", color="#000000", linewidth=linewidth)
plt.plot(x, res_random_disc, label="Random", color="#f8766d", linewidth=linewidth)

#lt.title("Diskrepanz Kriterium") 
plt.xlabel("Anzahl an Stichproben", fontsize=16)
plt.ylabel("Diskrepanz [-]", fontsize=16)
plt.grid(True)
plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=16) 
plt.tight_layout()

plt.savefig('dikrepanz_last2.png')
plt.close() 

plt.figure(figsize=(12, 6))
plt.plot(x, res_lhs_center_maximin, label="LHS-center", color="#FFF700", linewidth=linewidth)
plt.plot(x, res_lhs_maximin_maximin, label="LHS-maximin", color="#053908", linewidth=linewidth)
plt.plot(x, res_lhs_correlation_maximin, label="LHS-correlation", color="#5FA163", linewidth=linewidth)
plt.plot(x, res_lhs_centermaximin_maximin, label="LHS-centermaximin", color="#BEE239", linewidth=linewidth)
#plt.plot(x, res_lhs_center_maximin_d, label="LHS-center_d", color="red")

plt.plot(x, res_cvt_maximin, label="CVT", color="#FF8F00", linewidth=linewidth)
plt.plot(x, res_sobol_maximin, label="Sobol", color="#ff4fc1", linewidth=linewidth)
plt.plot(x, res_halton_maximin, label="Halton", color="#000000", linewidth=linewidth)
plt.plot(x, res_random_maximin, label="Random", color="#f8766d", linewidth=linewidth)

#plt.title("Maximin Kriterium") 
plt.xlabel("Anzahl an Stichproben", fontsize=16)
plt.ylabel("Maximin [-]", fontsize=16)
plt.grid(True)
plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=16)
plt.tight_layout()

plt.savefig('maximin_last2.png')
plt.close() 

plt.figure(figsize=(12, 6))
plt.plot(x, res_lhs_center_projected_dis, label="LHS-center", color="#FFF700", linewidth=linewidth)
plt.plot(x, res_lhs_maximin_projected_dis, label="LHS-maximin", color="#053908", linewidth=linewidth)
plt.plot(x, res_lhs_correlation_projected_dis, label="LHS-correlation", color="#5FA163", linewidth=linewidth)
plt.plot(x, res_lhs_centermaximin_projected_dis, label="LHS-centermaximin", color="blue" , linestyle=(0, (5, 10))) #color="#BEE239"
#plt.plot(x, res_lhs_center_projected_dis_d, label="LHS-center_d", color="red")

plt.plot(x, res_cvt_projected_dis, label="CVT", color="#FF8F00", linewidth=linewidth)
plt.plot(x, res_sobol_projected_dis, label="Sobol", color="#ff4fc1", linewidth=linewidth)
plt.plot(x, res_halton_projected_dis, label="Halton", color="#000000", linewidth=linewidth)
plt.plot(x, res_ramdom_projected_dis, label="Random", color="#f8766d", linewidth=linewidth)

#plt.title("Projizierte Distanz - Kriterium") 
plt.xlabel("Anzahl an Stichproben", fontsize=16)
plt.ylabel("projizierte Distanz [-]", fontsize=16)
plt.grid(True)
plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=16)
plt.tight_layout()

plt.savefig('projected_distance_last2.png') 
plt.close() 