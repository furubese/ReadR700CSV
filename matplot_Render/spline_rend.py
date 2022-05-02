from matplotlib import pyplot as p
from . import rend
import numpy as np
from scipy import interpolate

class Render_Spline(rend.Render):
    def __init__(self, AntenaData, reverse=True, default_value=0):
        super().__init__(AntenaData, reverse, default_value)

    def spline1(self, x, y, point):
        f = interpolate.interp1d(x, y, kind="cubic")
        X = np.linspace(x[0], x[-1], num=point, endpoint=True)
        Y = f(X)
        return X, Y

    def spline2(self, x, y, point):
        f = interpolate.Akima1DInterpolator(x, y, )
        X = np.linspace(x[0], x[-1], num=point, endpoint=True)
        Y = f(X)
        return X, Y

    def spline3(self, x, y, point, deg=3):
        tck, u = interpolate.splprep([x, y], k=deg, s=0)
        u = np.linspace(0, 1, num=point, endpoint=True)
        spline = interpolate.splev(u, tck)
        return spline[0], spline[1]

    def line_spline(self):
        for key in self.enable_keys:
            xy = rend.DictData_to_matplotData(self.AntenaData[key], self.firstData)
            a1, b1 = self.spline2(xy[0], list(map(lambda y: y+self.default_value, xy[1])), 100)
            p.plot(a1, b1)