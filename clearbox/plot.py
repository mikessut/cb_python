

from scipy.stats import probplot as scipy_probplot
from matplotlib import pylab as plt
from scipy.stats import norm
import numpy as np


def probplot(data, **kwargs):
    grid_lines = np.array([.1, 5, 1, 10, 25, 50,
                           75, 90, 95, 99, 99.9])
    grid_lines_std = norm.ppf(grid_lines/100)
    osm, osr = scipy_probplot(data, fit=False)
    # osr are the ordered values of data
    # osm are the corresponding number of standard deviations

    pct = 100 * norm.cdf(osm)
    h = plt.plot(osr, osm, '.', **kwargs)

    ax = h[0].axes
    ax.grid(True)

    idx = (grid_lines_std > min(osm)) & (grid_lines_std < max(osm))
    grid_lines = grid_lines[idx]
    grid_lines_std = grid_lines_std[idx]

    ax.set_yticks(grid_lines_std)
    ax.set_yticklabels(grid_lines)
    ax.set_ylabel('% of population')

