# -*- coding: utf-8 -*-
import numpy as py
import pandas as pd
import akshare as ak
import time
import urllib as ur
import re

# -----获取申万一级行业指数包含的27个行业的行业代码的list-----
# 计时
start = time.time() 

"""
主体
"""
sw_index_first_industry_df = ak.sw_index_first_info() #直接从akshare中调包，获得31个申万一级行指的information
# print("The raw data is like:\n", sw_index_first_industry_df, "\n")
sw_index_first_industry_df = sw_index_first_industry_df[~sw_index_first_industry_df['行业名称'].isin(['环保', '美容护理','石油石化','煤炭'])] # 按照要求，不要环保、美容护理、石油石化、煤炭四个行指
# print("After delete 4 indexes\n", sw_index_first_industry_df, "\n")
industry_list = sw_index_first_industry_df['行业代码'] #提取“行业代码”一栏数据
# print("Get the industry code\n", industry_list, "\n")
# 提取“行业代码”中的数字
industry_code = []
for name in industry_list:
    industry_code.append(re.findall('(\d+).SI', name)[0])
# print("Industry code 删去 .SI\n", industry_code, "\n")


end = time.time() #计时的
print("Running time: %s Seconds"%(end - start), "\n")





# -----爬取符合要求的申万一级行指历史数据文件（这边写了个函数，适用于以后方便使用）-----
def grab_files(url1, para_list, file_path, headers, url2=''):
    import requests
    import urllib as ur
    import time
    
    #计时
    start = time.time()
    
    #只需抓取一个文件时，输入字符串也可
    # para_list = list(para_list)
    # print(para_list)
    
    """
    主体
    """
    
    #方便为文件编号
    i=1
    print("实时下载情况:")
    for code in para_list:
        
            #拼成完整url
            url = url1 + code + url2
            #伪装成正常情况，完成文件下载
            r = requests.get(url, headers = headers)
            # print(r.content)
            
            with open (file_path + '/'+  str(i) + '-' + code + '.xlsx', "wb") as excel_: #这里也比较特殊，文件后缀可改
                excel_.write(r.content)
            #随时反馈下载情况
            print('{}--{} completed'.format(i, code))
            i += 1
            
            #停时
            time.sleep(2)
            
    end = time.time()
    print("Running time: %s Seconds"%(end - start), "\n")
    
    
    


# -----调用函数，批量抓取excel文件至Raw data文件夹-----
grab_files('https://www.swsresearch.com/institute-sw/api/index_analysis/index_analysis_report/?start_date=2014-02-21&end_date=2021-02-21&index_type=%E4%B8%80%E7%BA%A7%E8%A1%8C%E4%B8%9A&swindexcode=',
            industry_code,
            './Raw_data',
            {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54'},
            url2='&export=true')

                
            
            




