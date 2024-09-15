# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import time

# -----读取步骤三处理的数据，并进行初步整理-----
Dataframe_Centr = pd.read_csv('.\Data_after_second_cleaning\Centrality.csv')
Dataframe_r_pb = pd.read_csv('.\Data_after_second_cleaning\Relative_PB.csv')

# 发布日期这一列的向量将作为后续Dataframe的行名，先存下
date = list(Dataframe_Centr[Dataframe_Centr.columns[0]])

Dataframe_Centr.set_index(Dataframe_Centr.columns[0], inplace = True)
Dataframe_r_pb.set_index(Dataframe_r_pb.columns[0], inplace = True)

# 表头的名称向量将作为后续Dataframe的列名，先存下
name = list(Dataframe_Centr)

# 计算资产的数量，即行指的个数（获取Dataframe的列数）
n_assets = Dataframe_Centr.shape[1]





# -----得到index为交易日（2016-03-10至2021-02-19），列为各行业名称，值为0的Dataframe空表----
df_growing = pd.DataFrame(index=date, columns=name)
df_growing.replace(np.nan, 0, inplace=True)

df_boom = pd.DataFrame(index=date, columns=name)
df_boom.replace(np.nan, 0, inplace=True)

df_others = pd.DataFrame(index=date, columns=name)
df_others.replace(np.nan, 0, inplace=True)





# -----制作处于“泡沫膨胀期”“泡沫破裂期”和“其他”的行业的Dataframe表-----

start = time.time() #计时

# 由于pandas.DataFrame只能按列值对行进行重排，故对“Dataframe_Centr”“Dataframe_r_pb”进行转置
Central_T = Dataframe_Centr.T
Relative_pb_T = Dataframe_r_pb.T

# 对每日资产中心度（Centrality）和相对价值指标（Relative PB）排前7的行业进行记录
Central_list = []
R_PB_list =[]

# 开始循环计算
for i in range(len(date)):
    
    # 获取每日Centrality排名靠前行业
    central_d = Central_T.iloc[:, i: i+1] #把该日Centrality数据切出来
    central_res = central_d.sort_values(by=date[i], ascending=False) #按该列数据进行行重排
    
    central_list = list(central_res.index)[: 7] #把重排后的前7行index（行业名称取出）
    
    Central_list.append(central_list)
    
    
    # 获取每日Relative_PB排名靠前行业
    r_pb_d = Relative_pb_T.iloc[:, i: i+1] #把该日Centrality数据切出来
    r_pb_res = r_pb_d.sort_values(by=date[i], ascending=False) #按该列数据进行行重排
    
    r_pb_list = list(r_pb_res.index)[: 7] #把重排后的前7行index（行业名称取出）
    
    R_PB_list.append(r_pb_list)
    
end = time.time() #计时的
print("Running time: %s Seconds"%(end - start), "\n")


    
    

# 按照获得的list制作Dataframe

start = time.time() #计时

for i in range(len(date)):
    for j in name:
        
        if j in Central_list[i]:
            if j in R_PB_list[i]:
                
                df_boom.loc[date[i], j] = 1
                
                
            else:
                
                df_growing.loc[date[i], j] = 1
                
        else:
            
            df_others.loc[date[i], j] = 1
                
end = time.time() #计时的
print("Running time: %s Seconds"%(end - start), "\n")

print(df_boom.describe())


              

                
# 将获得两张dataframe表导入csv，预备做下一步处理
df_growing.to_csv('.\Analyzed_data\data_growing_industry.csv', encoding='utf_8_sig')
df_boom.to_csv('.\Analyzed_data\data_boom_industry.csv', encoding='utf_8_sig')
df_others.to_csv('.\Analyzed_data\data_other_industries.csv', encoding='utf_8_sig')