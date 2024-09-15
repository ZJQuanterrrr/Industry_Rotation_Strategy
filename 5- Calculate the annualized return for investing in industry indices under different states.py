# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

# -----读取所需要的数据，并进行初步整理-----
df_growing = pd.read_csv('.\Analyzed_data\data_growing_industry.csv')
df_boom = pd.read_csv('.\Analyzed_data\data_boom_industry.csv')
df_others = pd.read_csv('.\Analyzed_data\data_other_industries.csv')

# 读取收益率数据
df_return = pd.read_csv('.\Data_after_first_cleaning\Dataframe_1.csv')

window = 500 #当时所设的历史数据窗口期
df_return_used = df_return.iloc[window-1:]

# 发布日期这一列的向量后续可能有用，先存下
date = list(df_growing[df_growing.columns[0]])

# 将日期数据作为index
df_growing.set_index(df_growing.columns[0], inplace=True)

df_boom.set_index(df_boom.columns[0], inplace=True)

df_others.set_index(df_others.columns[0], inplace=True)

df_return_used.set_index(df_return_used.columns[0], inplace=True)
df_return_used = df_return_used.iloc[window:]





# -----开始计算各状态收益率-----
#获取三张不同状态收益率表
df_growing_return = df_growing * df_return_used

df_boom_return = df_boom * df_return_used

df_others_return = df_others * df_return_used

# 开始计算
# 将三张原表和三张return表各自按行加总
df_growing['Row_sum'] = df_growing.apply(lambda x: x.sum(), axis=1)
df_boom['Row_sum'] = df_boom.apply(lambda x: x.sum(), axis=1)
df_others['Row_sum'] = df_others.apply(lambda x: x.sum(), axis=1)

df_growing_return['Row_sum'] = df_growing_return.apply(lambda x: x.sum(), axis=1)
df_boom_return['Row_sum'] = df_boom_return.apply(lambda x: x.sum(), axis=1)
df_others_return['Row_sum'] = df_others_return.apply(lambda x: x.sum(), axis=1)

# 获得各状态的每日平均收益
df_growing_return['Average return'] = df_growing_return['Row_sum']/df_growing['Row_sum']
df_others_return['Average return'] = df_others_return['Row_sum']/df_others['Row_sum']

ave_r_boom = []
for i in range(len(date)):
    
    if df_boom.loc[date[i], 'Row_sum'] == 0:
        
        ave_r_boom.append(0)
        
    else:
        
        ave_r_boom.append(df_boom_return.loc[date[i], 'Row_sum']/df_boom.loc[date[i], 'Row_sum'])
        
ave_r_boom = np.array(ave_r_boom)


# 获得投资各状态的年化收益率
# 先取出各个状态的日度收益率数据
ave_r_growing = np.array(df_growing_return['Average return'])
# ave_r_boom = list(df_boom_return['Average return'])
ave_r_others = np.array(df_others_return['Average return'])

principal = 10000
volumn_growing = 10000 #设本金为10000
# 计算“泡沫膨胀期”
for i in ave_r_growing:
    
    volumn_growing = (1+i/100)*volumn_growing


volumn_boom = 10000 #设本金为10000
# 计算“泡沫破裂期”
for i in ave_r_boom:
    
    volumn_boom = (1+i/100)*volumn_boom
    # print(volumn_boom)
    
volumn_others = 10000 #设本金为10000
# 计算投资其他行业
for i in ave_r_others:
    
    volumn_others = (1+i/100)*volumn_others
    
y_return_growing = (volumn_growing - principal)/principal * 365/len(date) * 100 #计算年化收益率

y_return_boom = (volumn_boom - principal)/principal * 365/len(date) * 100

y_return_others = (volumn_others - principal)/principal * 365/len(date) * 100

risk_growing = np.std(ave_r_growing/100) #计算风险

risk_boom = np.std(ave_r_boom/100)

risk_others = np.std(ave_r_others/100)





# -----计算如若平均投资每个行业的收益-----
df_return_used['Row_sum'] = df_return_used.apply(lambda x: x.sum(), axis=1)
df_return_used['Average return'] = df_return_used['Row_sum']/27

ave_r_all = np.array(df_return_used['Average return'])

principal = 10000
volumn_all = 10000
for i in ave_r_all:
    
    volumn_all = (1+i/100)*volumn_all
    
y_return_all = (volumn_all - principal)/principal * 365/len(date) * 100 #计算年化收益率
risk_all = np.std(ave_r_all/100)




# 将三种情形下的累积日收益率取出，存为csv文件
df_final_return = pd.DataFrame(index=date)

df_final_return["Bubble growing"] = np.cumsum(np.array(ave_r_growing))
df_final_return["Bubble broke"] = np.cumsum(np.array(ave_r_boom))
df_final_return["Others"] = np.cumsum(np.array(ave_r_others))
df_final_return["Average"] = np.cumsum(np.array(ave_r_all))


df_final_return.to_csv('.\Data_Results\data_return.csv', encoding='utf_8_sig')

# 将数据导出保存至csv文件
df_results = pd.DataFrame([[y_return_growing, y_return_boom, y_return_others, y_return_all],
                           [risk_growing, risk_boom, risk_others, risk_all]], 
                          index=["return (%)", "risk"],
                          columns=["bubble growing industry", "bubble broke industry", "other industry", "average all industry"])

df_results.to_csv('.\Data_Results\data_results.csv', encoding='utf_8_sig')

    

