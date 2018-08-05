import unittest
import numpy as np
import cb_python.plot as cb_plot
import matplotlib.pylab as plt


class TestPlot(unittest.TestCase):

    def test_probplot(self):
        plt.figure()
        data = np.random.randn(100)*10000
        cb_plot.probplot(data)

    def test_probplot_sparse(self):
        plt.figure()
        data = np.random.randn(10)
        cb_plot.probplot(data)

    def test_probplot_huge(self):
        plt.figure()
        data = np.random.randn(10000)
        cb_plot.probplot(data)

    def test_probplot_multiple(self):
        plt.figure()
        data = np.random.randn(100)
        cb_plot.probplot(data, label='a')

        data = np.random.randn(100)*.1
        cb_plot.probplot(data, label='b')
        plt.legend(loc=0)

    @classmethod
    def tearDownClass(cls):
        print("teardown")
        cb_plot.plt.show()
