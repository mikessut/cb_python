
from scipy.stats import norm
import enum
import datetime
import numpy as np
from numpy import log, exp, sqrt

class OPTION_TYPE(enum.Enum):
    CALL = 'call'
    PUT = 'put'


def iv_prob(vol, cal_days, price, target_price=None, n_sigma=1.0, req_prob=.1, annual_ret=.12):
    move_n_sigma = sqrt(cal_days/365)*vol*price*n_sigma
    print(f"{n_sigma}-sigma move in {cal_days} days is {move_n_sigma:.2f}")
    prob = norm.cdf(n_sigma) - norm.cdf(-n_sigma)
    low = price - move_n_sigma
    high = price + move_n_sigma
    print(f"{prob*100:.1f}% probability between {low:.2f} and {high:.2f}")

    if target_price:
        if target_price > price:
            n = (target_price/price - 1) / vol / sqrt(cal_days/365)
            prob = norm.cdf(-n)
            print(f"{prob*100:.1f}% probability price above {target_price}")
        else:
            n = -(target_price/price - 1) / vol / sqrt(cal_days/365)
            prob = norm.cdf(-n)
            print(f"{prob*100:.1f}% probability price below {target_price}")

    if req_prob:
        n = -norm.ppf(req_prob)
        high = price * (1 + n*vol*sqrt(cal_days/365))
        low = price * (1 - n*vol*sqrt(cal_days/365))
        print(f"{req_prob*100:.1f}% probability price below {low:.2f} OR above {high:.2f}")

        ret = annual_ret*cal_days/365
        p = ret * price
        print(f"Covered call with annual return of {annual_ret*100:.1f}% must sell for {p:.2f}")



class Option(object) :

    """
    S, be the price of the stock, which will sometimes be a random variable and other times a constant (context should make this clear).
    V(S, t), the price of a derivative as a function of time and stock price.
    C(S, t) the price of a European call option and P(S, t) the price of a European put option.
    K, the strike price of the option.
    r, the annualized risk-free interest rate, continuously compounded (the force of interest).
    \mu, the drift rate of S, annualized.
    \sigma, the standard deviation of the stock's returns; this is the square root of the quadratic variation of the stock's log price process.
    t, a time in years; we generally use: now=0, expiry=T.
    \Pi, the value of a portfolio.

    put_call: either 'put' or 'call'


    """

    def __init__(self,T,S,K,r,sigma,put_call):
        if isinstance(T,datetime.datetime):
            self.T = (T - datetime.datetime.now()).days / 365.0
        else:
            self.T = T
        self.S = S
        self.K = K
        self.r = r
        self.sigma = sigma
        self.put_call = put_call

    @staticmethod
    def fromDF(df,idx,r=.01):
        K = idx[0]
        T = datetime.datetime.strptime(idx[1],'%Y-%m-%d')
        put_call = idx[2]
        S = df.loc[idx,'Underlying_Price'][0]
        IV = float(df.loc[idx,'IV'][0][:-1])/100

        bid = df.loc[idx,'Bid'][0]
        ask = df.loc[idx,'Ask'][0]

        o = Option(T,S,K,r,IV,put_call)
        o.price()  # necessary to calc d1/d2
        #print("Calcated price of {:.2f} vs. B/A of {:.2f}/{:.2f}".format(o.price(),bid,ask))
        return o


    def calc(self):
        self.d1 = 1.0/self.sigma/sqrt(self.T)*(log(self.S/self.K) +\
                                          (self.r+self.sigma**2/2)*self.T)
        self.d2 = self.d1 - self.sigma*sqrt(self.T)

    def callPrice(self):
        self.calc()
        return norm.cdf(self.d1)*self.S - norm.cdf(self.d2)*self.K*exp(-self.r*self.T)

    def putPrice(self):
        self.calc()
        return self.K*exp(-self.r*self.T) - self.S + self.callPrice()
        #return norm.cdf(-self.d2)*self.K*exp(-self.r*self.T) \
        #    - norm.cdf(-self.d1)*self.S

    def price(self):
        if self.put_call == 'call':
            return self.callPrice()
        elif self.put_call == 'put':
            return self.putPrice()
        else:
            print('put_call not set.')

    def delta(self):
        """d[C,P]/dS: Change in option price with change in underlying price.
        """
        if self.put_call == 'call':
            return norm.cdf(self.d1)
        elif self.put_call == 'put':
            return -norm.cdf(-self.d1)

    def KfromDelta(self,delta,iv_func_K=None):
        if iv_func_K == None:
            iv_func_K = lambda K : self.sigma

        origK = self.K
        origSigma = self.sigma
        def objFunc(K):
            self.K = K
            self.sigma = iv_func_K(K)
            self.price() # updates d1/d2
            return self.delta() - delta
        K = brentq(objFunc,self.S*.5,self.S*1.5)
        self.K = origK
        self.sigma = origSigma
        return K

    def gamma(self):
        """d2[C,P]/dS2
        Calculate numerically
        """
        eps = .001
        Sorig = self.S

        delta1 = self.delta()
        self.S = self.S + eps
        self.price()
        delta2 = self.delta()

        # restore S
        self.S = Sorig

        return (delta2-delta1)/eps

    def vega(self):
        """d[C,P]/dsigma
        Calculate numerically
        """
        eps = .01
        sigma_orig = self.sigma

        oPrice1 = self.price()
        self.sigma = self.sigma + eps
        oPrice2 = self.price()

        # restore sigma
        self.sigma = sigma_orig

        return (oPrice2-oPrice1)

    def theta(self):
        """Change per day."""
        eps = .001

        Torig = self.T
        oPrice1 = self.price()
        self.T = self.T - eps
        oPrice2 = self.price()

        # restore T
        self.T = Torig

        return (oPrice2-oPrice1)/(eps*365.25)

    def rho(self):
        """Change per 1% change in r. (SOmething not correct here)"""
        eps = .0001
        # eps*sf = .01
        sf = .01/eps

        r_orig = self.r
        oPrice1 = self.price()
        self.r = self.r + eps
        oPrice2 = self.price()

        # restore r
        self.r = r_orig

        return (oPrice2-oPrice1)/(eps*sf)



    def whatIf(self,Svector,output_method='price',**kwargs):
        orig = {}
        for k in kwargs.keys():
            if k in self.__dict__.keys():
                orig[k] = getattr(self,k)
                setattr(self,k,kwargs[k])
            else:
                print("Warning kwarg passed that isn't doing anything {}".format(k))
        orig['S'] = self.S

        output = zeros(len(Svector))

        for n in range(len(Svector)):
            setattr(self,'S',Svector[n])
            self.price()
            output[n] = getattr(self,output_method)()

        # restore modified values
        for k in orig.keys():
            setattr(self,k,orig[k])

        self.price()

        return output



    def IV(self,price,guess=.21,sf=1.0):
        origK = self.K
        origS = self.S
        self.K = self.K*sf
        self.S = self.S*sf
        def objFunc(sigma):
            #self.sigma = sigma[0]
            self.sigma = sigma
            return (price*sf - self.price())**2
        #sigma = fmin(objFunc,guess,disp=False,xtol=1e-12,ftol=1e-12)[0]
        #sigma = fminbound(objFunc,0.05,1,)
        #sigma = brute(objFunc,[(.05,1.0)])[0]
        #sigma = basinhopping(objFunc,guess).x
        #sigma = minimize_scalar(objFunc,bracket=(.05,1.0),method='golden').x
        def objFunc2(sigma):
            self.sigma = sigma
            return price - self.price()
        sigma = brentq(objFunc2,.000001,10)
        self.sigma = sigma
        self.K = origK
        self.S = origS
        return sigma


def covered_call_yield():
    from clearbox import vol
    import numpy as np
    import matplotlib.pylab as plt
    from scipy.stats import norm



    iv = np.linspace(.1, .7, 50)
    all_days_to_expiration = [10,20,30,60]
    ret = np.zeros((len(iv), len(all_days_to_expiration)))

    ndays = 30

    P = 50
    plt.clf()
    for m, ndays in enumerate(all_days_to_expiration):
        for n, i in enumerate(iv):
            # assume we want 90% confidence
            n_sigma = norm.ppf(.9)
            Pstrike = P*(1 + n_sigma*i*np.sqrt(ndays/365))
            call = vol.Option(ndays/365, P, Pstrike, .02, i, 'call')
            ret[n, m] = call.price() / P * 365 / ndays
        plt.plot(iv, ret[:, m], label=f'{ndays} to expiration')

    plt.grid(True)
    plt.xlabel('Implied volatility')
    plt.ylabel('Annualized return')
    plt.legend(loc=0)
    plt.show()
