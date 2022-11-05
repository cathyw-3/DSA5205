import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math import floor

factor_returns = pd.read_csv("../../Predict/factors_returns_pred.csv")
factors = pd.read_csv("../../Factors/merge_Factors.csv")
earning_factors = ["Momentum_1", "Momentum_2"]
risk_factors = ["Financial Quality", "Turnover"]
all_factors = earning_factors + risk_factors



def strategy3(date):
    seg_num = 5
    
    industry_factor_list = list(factor_returns.columns)[11:]
    industry_factor_return = factor_returns.loc[factor_returns["Date"]==date,["Date"]+industry_factor_list]
    return_list = industry_factor_return.values.reshape(-1)[1:]
    standarized_return_list = (return_list-min(return_list))/(max(return_list)-min(return_list))
    return_score_list = standarized_return_list/sum(standarized_return_list)*100

    factors_score = factors[["Date", "Index"]+earning_factors+risk_factors+industry_factor_list]
    factors_score = factors_score.loc[factors_score["Date"]==date]
    factors_score.loc[:, industry_factor_list] = factors_score.loc[:, industry_factor_list].multiply(return_score_list, axis=1)
    
    # get factors score from factors
    for factor in all_factors:
        factors_score = factors_score.drop_duplicates(subset=[factor])
    for factor in all_factors:
        factors_score[factor+"_score"] = None
    num_row = factors_score.shape[0]
    cut_length = floor(num_row/seg_num)
    cutting_point = [i*cut_length for i in range(seg_num)]
    cutting_point.append(num_row)
    stock_index = []
    score_list = list(np.arange(0, 1, 1/seg_num)+1/seg_num)
    score_list.reverse()
    
    # get stock indexes in each region
    for i in range(len(cutting_point)-1):
        stock_index.append(list(range(cutting_point[i], cutting_point[i+1])))

    for factor in earning_factors:
        factors_score = factors_score.sort_values(by=factor, ascending=False)
        col_index = list(factors_score.columns).index(factor+"_score")
        for i in range(len(stock_index)):
            factors_score.iloc[stock_index[i], col_index] = 100*score_list[i]
    for factor in risk_factors:
        factors_score = factors_score.sort_values(by=factor, ascending=True)
        col_index = list(factors_score.columns).index(factor+"_score")
        for i in range(len(stock_index)):
            factors_score.iloc[stock_index[i], col_index] = 100*score_list[i]
    # factors_score["total_score"] = factors_score[earning_factors[0]+"_score"] + factors_score[earning_factors[1]+"_score"] + factors_score[risk_factors[0]+"_score"] + factors_score[risk_factors[1]+"_score"]
    column_index = 2+len(all_factors)
    factors_score["total_score"] = factors_score.iloc[:, column_index:].sum(axis=1)

    factors_score = factors_score.sort_values(by="total_score", ascending=False)
    selected_stocks = factors_score["Index"].head(10).tolist()
    return selected_stocks