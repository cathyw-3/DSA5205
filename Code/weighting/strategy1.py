import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math import floor

factor_returns = pd.read_csv("../../Predict/factors_returns_pred.csv")
style_factors = list(factor_returns.columns)[1:11]
style_factor_returns = factor_returns[["Date"]+style_factors]
factors = pd.read_csv("../../Factors/merge_Factors.csv")
earning_factors = ["Momentum_1", "Momentum_2"]
risk_factors = ["Financial Quality", "Turnover"]
all_factors = earning_factors + risk_factors

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

# def strategy_2(date):
#     seg_num = 5
    
#     # get factors score from factors
#     factors_score = factors[["Date", "Index"]+earning_factors+risk_factors]
#     factors_score = factors_score.loc[factors_score["Date"]==date]
#     for factor in all_factors:
#         factors_score = factors_score.drop_duplicates(subset=[factor])
#     for factor in all_factors:
#         factors_score[factor+"_score"] = None
#     num_row = factors_score.shape[0]
#     cut_length = floor(num_row/seg_num)
#     cutting_point = [i*cut_length for i in range(seg_num)]
#     cutting_point.append(num_row)
#     stock_index = []
#     score_list = list(np.arange(0, 1, 1/seg_num)+1/seg_num)
#     score_list.reverse()
    
#     # get stock indexes in each region
#     for i in range(len(cutting_point)-1):
#         stock_index.append(list(range(cutting_point[i], cutting_point[i+1])))

#     for factor in earning_factors:
#         factors_score = factors_score.sort_values(by=factor, ascending=False)
#         col_index = list(factors_score.columns).index(factor+"_score")
#         for i in range(len(stock_index)):
#             factors_score.iloc[stock_index[i], col_index] = 100*score_list[i]
#     for factor in risk_factors:
#         factors_score = factors_score.sort_values(by=factor, ascending=True)
#         col_index = list(factors_score.columns).index(factor+"_score")
#         for i in range(len(stock_index)):
#             factors_score.iloc[stock_index[i], col_index] = 100*score_list[i]
#     factors_score["total_score"] = factors_score[earning_factors[0]+"_score"] + factors_score[earning_factors[1]+"_score"] + factors_score[risk_factors[0]+"_score"] + factors_score[risk_factors[1]+"_score"]

#     factors_score = factors_score.sort_values(by="total_score", ascending=False)
#     selected_stocks = factors_score["Index"].head(10).tolist()
#     return selected_stocks
    