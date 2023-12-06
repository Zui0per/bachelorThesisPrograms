import pyDOE2
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from idaes.core.surrogate.pysmo.sampling import CVTSampling

def vis_lhs(count: int, criterion: str):
    samples = pyDOE2.lhs(2, count, criterion)

    fig, ax = plt.subplots()
    ax.scatter(samples[:, 0], samples[:, 1], c='blue', marker='o')
    ax.set_xlabel('Faktor 1')
    ax.set_ylabel('Faktor 2')
    ax.set_title(f'LHS - {criterion}')

    ax.grid()

    ax.xaxis.set_major_locator(MultipleLocator(base=1/count))
    ax.yaxis.set_major_locator(MultipleLocator(base=1/count))

    ax.set_xlim(0, 1)  # Assuming your parameter range is [0, 1]
    ax.set_ylim(0, 1)

    plt.savefig(f"LHS-{criterion}")


def vis_cvt(size: int):
    data_bounds = [[0, 0], [1, 1]]
    b = CVTSampling(data_bounds, size, sampling_type="creation")
    samples = b.sample_points()

    fig, ax = plt.subplots()
    ax.scatter(samples[:, 0], samples[:, 1], c='blue', marker='o')
    ax.set_xlabel('Faktor 1')
    ax.set_ylabel('Faktor 2')
    ax.set_title(f'CVT')

    #ax.grid()

    ax.set_xlim(0, 1)  # Assuming your parameter range is [0, 1]
    ax.set_ylim(0, 1)

    plt.savefig(f"CVT2")

vis_cvt(10)