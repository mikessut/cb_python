

"""
Black-Scholes options pricing

"""

import math
from scipy.stats import norm


class Option:

    def __init__(self, und_price, strike, t, iv):
        self._und_price = und_price
        self._strike = strike
        self._t = t  # calendar time in years
        self._iv = iv

    def underlying_price(self):
        return self._und_price

    def days_to_expiry(self):
        return self._t*365

    def strike(self):
        return self._strike

    def t(self):
        return self._t

    def iv(self):
        return self._iv

    def moneyness(self) -> float:
        """
        https://www.fdic.gov/bank/analytical/cfr/2005/apr/mbedendo-shodges.pdf
        :return:
        """
        return math.log(self.strike() / self.underlying_price()) / math.sqrt(self.days_to_expiry())

    def BScalc(self, r, iv=None, t=None, und_price=None):
        if iv is None:
            iv = self.iv()
        if t is None:
            t = self.t()
        if und_price is None:
            und_price = self.underlying_price()
        d1 = 1/iv/math.sqrt(t)*(math.log(und_price/self.strike()) + (r + iv**2/2)*t)
        d2 = d1 - iv*math.sqrt(t)
        return d1, d2, t

    def BSgamma(self, r, iv=None, t=None):
        if iv is None:
            iv = self.iv()
        d1, d2, t = self.BScalc(r, iv, t)
        return norm.pdf(d1)/self.underlying_price()/iv/math.sqrt(t)


class Call(Option):

    def BSprice(self, r=0, iv=None, t=None, und_price=None):
        d1, d2, t = self.BScalc(r, iv, t, und_price)
        PV = self.strike()*math.exp(-r*t)
        if und_price is None:
            und_price = self.underlying_price()
        return norm.cdf(d1)*und_price - norm.cdf(d2)*PV

    def BSdelta(self, r=0, iv=None, t=None, und_price=None):
        d1, d2, t = self.BScalc(r, iv, t, und_price)
        return norm.cdf(d1)

    def BStheta(self, r=0, iv=None, t=None):
        d1, d2, t = self.BScalc(r, iv, t)
        if iv is None:
            iv = self.iv()
        return -self.underlying_price()*norm.pdf(d1)*iv/2/math.sqrt(t) - r*self.strike()*math.exp(-r*t)*norm.pdf(d2)


class Put(Option):

    def BSprice(self, r=0, iv=None, t=None, und_price=None):
        d1, d2, t = self.BScalc(r, iv, t, und_price)
        PV = self.strike()*math.exp(-r*t)
        if und_price is None:
            und_price = self.underlying_price()
        return norm.cdf(-d2)*PV - norm.cdf(-d1)*und_price

    def BSdelta(self, r=0, iv=None, t=None, und_price=None):
        d1, d2, t = self.BScalc(r, iv, t, und_price)
        return -norm.cdf(-d1)

    def BStheta(self, r=0, iv=None, t=None):
        d1, d2, t = self.BScalc(r, iv, t)
        if iv is None:
            iv = self.iv()
        return -self.underlying_price()*norm.pdf(d1)*iv/2/math.sqrt(t) + r*self.strike()*math.exp(-r*t)*norm.pdf(-d2)