# -*- coding: utf-8 -*-
import os
import pandas as pd
import time
from functools import reduce

#-----读取所有excel表的收益率数据，合并为一个index为日期，col_name为行业名称，值为该行业行指日度收益率的Dataframe_1-----
def Excels_to_Dataframe_1(files_dir):
    import os
    import pandas as pd
    import time
    from functools import reduce
    
    start = time.time() #计时
    
    
    dfs = [] #用以存储读取的各表中的收益率数据，方便后续合并
    
    # 显示进度
    print("Dataframe_1 process:")
    
    #对Raw_data文件夹进行遍历，获取其中所有文件的路径
    for cur_dir, dirs, files in os.walk(files_dir):
        for file in files:
            
            file_path = cur_dir + "\\\\" + file #合并三者为"pd.read_excel"可以读取的路径形式
            
            # 在制作该Dataframe的时候，需要读取如下数据
            # 该步骤为获取这些数据在源数据中的列index
            df_index = list(pd.read_excel(file_path, nrows=1))
            return_index_1 = df_index.index("涨跌幅(%)")
            return_index_2 = df_index.index("发布日期")
            return_index_3 = df_index.index("指数名称")
            
            # 根据获取的列index进行读取
            df = pd.read_excel(file_path, usecols=[return_index_1, return_index_2])
            col_name = pd.read_excel(file_path, nrows=1, usecols=[return_index_3]).iat[0,0] #指数名称最后是作为新的Dataframe的col_name，这里只需获取标量即可

            df.set_index("发布日期", inplace=True) #将日期作为index

            new_df = df.iloc[::-1] #源数据为时间倒序，将其转换为时间正序
            
            new_df.columns = [col_name] #修改列名为行业名称
            new_df
            
            dfs.append(new_df)
            
            # 显示进度
            print(col_name, "is finished")
            
    # print(dfs)
    
    # 拼接dfs中的dataframe
    df_final = reduce(lambda left, right: pd.merge(left, right, left_index=True, right_index=True), dfs)
    # print(df_final)
    print(type(df_final))
    
    # 将该Dataframe_1保存至csv文件
    df_final.to_csv('.\Data_after_first_cleaning\Dataframe_1.csv', encoding='utf_8_sig')
        
    
    end = time.time() #计时的
    print("Running time: %s Seconds"%(end - start), "\n")
    
    
    
    
    
#-----读取所有excel表的收益率数据，合并为一个index为日期，col_name为行业名称，值为该行业行市值的Dataframe_2-----
def Excels_to_Dataframe_2(files_dir):
    import os
    import pandas as pd
    import time
    from functools import reduce
    
    start = time.time() #计时
    
    
    dfs = [] #用以存储读取的各表中的流通市值数据，方便后续合并
    
    # 显示进度
    print("Dataframe_2 process:")
    
    #对Raw_data文件夹进行遍历，获取其中所有文件的路径
    for cur_dir, dirs, files in os.walk(files_dir):
        for file in files:
            
            file_path = cur_dir + "\\\\" + file #合并三者为"pd.read_excel"可以读取的路径形式
            
            # 在制作该Dataframe的时候，需要读取如下数据
            # 该步骤为获取这些数据在源数据中的列index
            df_index = list(pd.read_excel(file_path, nrows=1))
            return_index_1 = df_index.index("流通市值(亿元)")
            return_index_2 = df_index.index("发布日期")
            return_index_3 = df_index.index("指数名称")
            
            # 根据获取的列index进行读取
            df = pd.read_excel(file_path, usecols=[return_index_1, return_index_2])
            col_name = pd.read_excel(file_path, nrows=1, usecols=[return_index_3]).iat[0,0] #指数名称最后是作为新的Dataframe的col_name，这里只需获取标量即可

            df.set_index("发布日期", inplace=True) #将日期作为index

            new_df = df.iloc[::-1] #源数据为时间倒序，将其转换为时间正序
            
            new_df.columns = [col_name] #修改列名为行业名称
            new_df
            
            dfs.append(new_df)
            
            # 显示进度
            print(col_name, "is finished")
            
    # print(dfs)
    
    # 拼接dfs中的dataframe
    df_final = reduce(lambda left, right: pd.merge(left, right, left_index=True, right_index=True), dfs)
    # print(df_final)
    print(type(df_final))
    
    # 将该Dataframe_2保存至csv文件
    df_final.to_csv('.\Data_after_first_cleaning\Dataframe_2.csv', encoding='utf_8_sig')
        
    
    end = time.time() #计时的
    print("Running time: %s Seconds"%(end - start), "\n")
    



#-----读取所有excel表的收益率数据，合并为一个index为日期，col_name为行业名称，值为该行业行指市净率（PB）的Dataframe_3-----
def Excels_to_Dataframe_3(files_dir):
    import os
    import pandas as pd
    import time
    from functools import reduce
    
    start = time.time() #计时
    
    
    dfs = [] #用以存储读取的各表中的行指PB数据，方便后续合并
    
    # 显示进度
    print("Dataframe_3 process:")
    
    #对Raw_data文件夹进行遍历，获取其中所有文件的路径
    for cur_dir, dirs, files in os.walk(files_dir):
        for file in files:
            
            file_path = cur_dir + "\\\\" + file #合并三者为"pd.read_excel"可以读取的路径形式
            
            # 在制作该Dataframe的时候，需要读取如下数据
            # 该步骤为获取这些数据在源数据中的列index
            df_index = list(pd.read_excel(file_path, nrows=1))
            return_index_1 = df_index.index("市净率(倍)")
            return_index_2 = df_index.index("发布日期")
            return_index_3 = df_index.index("指数名称")
            
            # 根据获取的列index进行读取
            df = pd.read_excel(file_path, usecols=[return_index_1, return_index_2])
            col_name = pd.read_excel(file_path, nrows=1, usecols=[return_index_3]).iat[0,0] #指数名称最后是作为新的Dataframe的col_name，这里只需获取标量即可

            df.set_index("发布日期", inplace=True) #将日期作为index

            new_df = df.iloc[::-1] #源数据为时间倒序，将其转换为时间正序
            
            new_df.columns = [col_name] #修改列名为行业名称
            new_df
            
            dfs.append(new_df)
            
            # 显示进度
            print(col_name, "is finished")
            
    # print(dfs)
    
    # 拼接dfs中的dataframe
    df_final = reduce(lambda left, right: pd.merge(left, right, left_index=True, right_index=True), dfs)
    # print(df_final)
    print(type(df_final))
    
    # 将该Dataframe_3保存至csv文件
    df_final.to_csv('.\Data_after_first_cleaning\Dataframe_3.csv', encoding='utf_8_sig')
        
    
    end = time.time() #计时的
    print("Running time: %s Seconds"%(end - start), "\n")





# -----运行上述函数-----
Excels_to_Dataframe_1("Raw_data")
Excels_to_Dataframe_2("Raw_data")
Excels_to_Dataframe_3("Raw_data")
    