# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt

# -----读取需要展示的数据，并进行初步整理-----
d_return = pd.read_csv('.\Data_after_first_cleaning\Dataframe_1.csv')
d_mar_cap = pd.read_csv('.\Data_after_first_cleaning\Dataframe_2.csv')
d_PB = pd.read_csv('.\Data_after_first_cleaning\Dataframe_3.csv')

d_return.set_index(d_return.columns[0], inplace = True)
d_mar_cap.set_index(d_mar_cap.columns[0], inplace = True)
d_PB.set_index(d_PB.columns[0], inplace = True)

# -----
centrality = pd.read_csv('.\Data_after_second_cleaning\Centrality.csv')
relative_pb = pd.read_csv('.\Data_after_second_cleaning\Relative_PB.csv')

centrality.set_index(centrality.columns[0], inplace = True)
relative_pb.set_index(relative_pb.columns[0], inplace = True)

# -----
three_industries_return = pd.read_csv('.\Data_Results\data_return.csv')
three_industries_return.set_index(three_industries_return.columns[0], inplace = True)





# 描述性统计
print("各申万一级行业行指收益率（%）数据描述", "\n", d_return.describe(), "\n")
print("各申万一级行业行指市值（亿元）数据描述", "\n", d_mar_cap.describe(), "\n")
print("各申万一级行业行指市净率（PB）（倍）数据描述", "\n", d_PB.describe(), "\n")
print("各申万一级行业资产中心度（Centrality）数据描述", "\n", centrality.describe(), "\n")
print("各申万一级行业行指相对市净率（Relative PB）数据描述", "\n", relative_pb.describe(), "\n")





# -----Python生成折线图的函数-----
def draw_line_c(dataframe):
    import pandas as pd
    import matplotlib.pyplot as plt 
    import numpy as np
    
    x = list(dataframe.index)
    
    for i in list(dataframe):
        
        y = list(dataframe[i])
        
        plt.plot(x, y)
        
    plt.xlabel("Trading day")
    plt.ylabel("Cumulative return") #这两个参数在以后画图时灵活调控
    
    plt.legend(list(dataframe))
    plt.xticks(np.arange(0, 700, 50))
    
    plt.show()





# -----运行函数生成图像-----
draw_line_c(three_industries_return)
