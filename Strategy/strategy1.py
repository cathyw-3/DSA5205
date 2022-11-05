import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math import floor

factor_returns = pd.read_csv("../Analysis/factors_returns_multi.csv")
style_factors = list(factor_returns.columns)[1:11]
style_factor_returns = factor_returns[["Date"]+style_factors]
factors = pd.read_csv("../Factors/merge_Factors.csv")

# 1. pick the factor with the highest factor return on a specific date 
# 2. pick the 10 stocks with the highest factor value on that date
def strategy1(date):
    predicted_factor_return = style_factor_returns.loc[style_factor_returns["Date"]==date]
    predicted_factor_return = predicted_factor_return.set_index("Date")
    max_factor = predicted_factor_return.idxmax(axis=1)[0]
    max_factor_stock = factors.loc[factors["Date"]==date, ["Index", max_factor]] 
    max_value = max_factor_stock[max_factor].max()
    max_factor_stock = max_factor_stock.loc[max_factor_stock[max_factor]!=max_value]
    max_factor_stock = max_factor_stock.sort_values(by=max_factor, ascending=False) 
    selected_stocks = max_factor_stock["Index"].head(10).tolist()
    return selected_stocks