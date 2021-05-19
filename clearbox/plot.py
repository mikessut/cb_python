

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


class DistPlot:

    def __init__(self, name=''):
        self.name = name
        self.data = []
        self.labels = []

    def add(self, y, label=None):
        self.data.append(np.array(y))
        self.labels.append(label)

    def plot(self, ax):
        for d, n in zip(self.data, self.labels):
            quantiles, order_response, _ = probplot(d)
            ax.plot(order_response, quantiles, 'o', label=n)
        newticks = np.array([.1, 1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99.0, 99.9])
        q = norm.ppf(newticks/100)
        #ax.set_xlim()
        ax.set_ylim(min(q), max(q))

        ax.set_yticks(q)
        yvals = ax.get_yticks()
        newy = ['{norm.cdf(x):.0f} %' for x in yvals]
        newy[0] = '0.1 %'
        newy[-1] = '99.9 %'

        ax.set_yticklabels(newy)
        ax.grid(True)
        ax.legend(loc=0)
        ax.set_title(self.name)

        #ax.set_xlabel(self.)

    def plot_stats_fig(self):
        f = plt.figure()
        ax = f.add_axes([.1, .4, .8, .5])
        f.text(.05, .3, self.stats(), verticalalignment='top', family='monospace')
        f.canvase.set_window_title(self.name)
        self.plot(ax)
        return f, ax

    def stats(self):
        pass


def plot11(ax=None):
    if ax is None:
        ax = plt.gca()

    minval = min(np.min([np.min(x.get_xdata()) for x in ax.lines]),
                 np.min([np.min(x.get_ydata()) for x in ax.lines]))
    maxval = max(np.max([np.max(x.get_xdata()) for x in ax.lines]),
                 np.max([np.max(x.get_ydata()) for x in ax.lines]))
    ax.plot([minval, maxval], [minval, maxval])