
from scipy.stats import norm
from math import sqrt

def iv_prob(vol, cal_days, price, target_price=None, n_sigma=1.0, req_prob=None):
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
