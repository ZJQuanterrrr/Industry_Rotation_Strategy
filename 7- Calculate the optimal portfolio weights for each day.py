# -*- coding: utf-8 -*-
import pandas as pd
from gurobipy import *
from functools import reduce
import numpy as np

# data的读取和初步处理
# -----读取所需要的数据，并进行初步整理-----
df_boom = pd.read_csv('.\Analyzed_data\data_boom_industry.csv')
df_others = pd.read_csv('.\Analyzed_data\data_other_industries.csv')

# 读取收益率数据
df_return = pd.read_csv('.\Data_after_first_cleaning\Dataframe_1.csv')

window = 500 #当时所设的历史数据窗口期
df_return_used = df_return.iloc[window-1:]

# 发布日期这一列的向量后续可能有用，先存下
date = list(df_boom[df_boom.columns[0]])
date_return = list(df_return_used[df_return_used.columns[0]])

# 将日期数据作为index
df_boom.set_index(df_boom.columns[0], inplace=True)

df_others.set_index(df_others.columns[0], inplace=True)

df_return_used.set_index(df_return_used.columns[0], inplace=True)
df_return_used_1 = df_return_used.iloc[window:]





# -----从“处于泡沫破裂期”和“不存在泡沫”的行业中选择行业-----
df_boom.loc['Col_sum'] = df_boom.apply(lambda x: x.sum())
df_others.loc['Col_sum'] = df_others.apply(lambda x: x.sum())

df_add_all = df_boom + df_others

selected_industry = []
for i in list(df_add_all.columns):
    
    if df_add_all[i].iloc[701] == 701:
        
        selected_industry.append(i)
        
df_adjusted_return = reduce(lambda left, right: pd.merge(left, right, left_index=True, right_index=True), [df_return_used[i] for i in selected_industry])
df_adjusted_return.columns = [ i for i in range(df_adjusted_return.shape[1])]





# -----开始迭代优化运算-----
window = 500
days = len(df_adjusted_return)

Por_w = [] # 用以存储计算所得的权重
for n in range(days - window):
    
    df_analyzed_window = df_adjusted_return.iloc[n: n + window, : ] #设定窗口  
    
    por_w = [] #用以存储计算所得权重
    
    stocks = df_analyzed_window.columns
    ret_mean = np.full(df_analyzed_window.shape[1], 1.008241)
    ret_cov = df_analyzed_window.cov()

    budget = 1 #只需计算权重，所以设置1
    exp_ret = 1.008241 #目前只需要减小风险

    # model
    m = Model('portfolio')

    # variable
    x = m.addVars(stocks, name='invest')
    x = pd.Series(x)

    # objective function
    obj = ret_cov.dot(x).dot(x)
    m.setObjective(obj, sense=GRB.MINIMIZE)

    # constraints
    m.addConstr(sum(x[s] for s in stocks) <=budget, name='budget_con')
    m.addConstr(sum(x[s]*ret_mean[s] for s in stocks) >= exp_ret, name='ret_con')

    m.optimize()

    # analysis
    if m.status == GRB.OPTIMAL:
        for s in stocks:
            
            if x[s].x > 1e-4:
                
                por_w.append(x[s].x)
            
            else:
                
                por_w.append(0)
                
    Por_w.append(por_w)
    
Portfolio_weight = pd.DataFrame(Por_w, index=date, columns=selected_industry)

df_adjusted_return.columns = selected_industry

optimal_ = Portfolio_weight * df_adjusted_return[window: ]
optimal_['Row_sum'] = optimal_.apply(lambda x: x.sum(), axis=1)
ave_r_Optimal = np.array(optimal_['Row_sum'])

    
risk_optimal = np.std(ave_r_Optimal/100)

print("优化后的风险", risk_optimal)
    
    
    

