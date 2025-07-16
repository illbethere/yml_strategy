# -*- coding: utf-8 -*-
"""
Spyder 编辑器

这是一个临时脚本文件。
"""

#%% 库
import os
path = r'C:\Users\Astra\Desktop\Local';
os.chdir(path)

import numpy as np
import pandas as pd
# import prettytable as pt
# import scipy.stats as st
# import statsmodels.api as sm

# import calendar  # 日历
import datetime as dt
# from tqdm import *
# from dateutil.parser import parse
# from dateutil.relativedelta import relativedelta
# from IPython.core.display import HTML

from sklearn.model_selection import train_test_split
from tqdm import tqdm  # 进度条
from scipy.spatial.distance import cdist
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error

# 画图
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as mg # 不规则子图
import matplotlib.dates as mdate
# import seaborn as sns

# 设置字体 用来正常显示中文标签
mpl.rcParams['font.sans-serif'] = ['SimHei']

# 用来正常显示负号
mpl.rcParams['axes.unicode_minus'] = False


#%% 数据
def read_data(file):
    df_m = pd.read_csv(file)
    
    # 重命名并转换时间列
    df_m = df_m.rename(columns={'Unnamed: 0': 't'})
    df_m['t'] = pd.to_datetime(df_m['t'], format='%Y%m%d%H%M%S')
    
    # 提取7-8月数据
    df_m = df_m[df_m['t'].dt.month.isin([7, 8])].copy()
    
    # 提取日期和时分秒作为两列
    df_m['date'] = df_m['t'].dt.date
    df_m['time'] = df_m['t'].dt.time
    
    # 创建透视表（日期为行，时间为列，值为收盘价）
    df_pivot = df_m.pivot_table(
        index='date',
        columns='time',
        values='close',
        aggfunc='last'  # 如果同一时间有多个数据，取最后一个
    )
    
    # 划分
    # 按顺序划分80%训练集，20%测试集
    split_idx = int(len(df_pivot) * 0.8)
    train = df_pivot.iloc[:split_idx]  # 前80%作为训练集
    test = df_pivot.iloc[split_idx:]   # 后20%作为测试集

    # 预处理：确保列是时间排序的
    train = train.sort_index(axis=1)
    test = test.sort_index(axis=1)
    
    train.index = pd.to_datetime(train.index)
    test.index = pd.to_datetime(test.index)
    
    return train, test

#%% 相似度模型

def get_first_30min(row):
    """提取每行前30分钟数据（假设时间列已排序）"""
    time_cols = [col for col in row.index if col <= pd.to_datetime('1900-01-01 09:30:00').time()]
    row_30 = row[time_cols] / row.iloc[0]
    return row_30

def cal_similarity(train_30, test_row_30, top_k):
    """基于MSE计算相似度，仅保留Top 10权重"""
    # test_row_30: 每日前30min数据/开盘数据
    mse_scores = []
    
    # 计算与训练集每条记录的MSE
    for _, train_row in train_30.iterrows():
        # 对齐长度（取最小公共长度）
        min_len = min(len(test_row_30), len(train_row))
        if min_len == 0:
            mse_scores.append(np.inf)  # 无效值设为无穷大
            continue
            
        # 计算MSE（越小越相似）
        mse = mean_squared_error(
            test_row_30.values[:min_len],
            train_row.values[:min_len]
        )
        mse_scores.append(mse)
    
    # 转换为相似度（MSE越小，相似度越高）
    mse_scores = np.array(mse_scores)
    similarities = 1 / (1 + mse_scores)  # 将MSE映射到(0,1]区间
    
    # 仅保留Top 10的权重，其余为0
    top_indices = np.argsort(similarities)[-top_k:]  # 取相似度最高的10个索引
    weights = np.zeros(len(similarities))
    weights[top_indices] = similarities[top_indices] / np.sum(similarities[top_indices])  # 归一化
    
    return weights

def cheat(test_row_30, train, train_30, top_k):
    
    weights = cal_similarity(train_30, test_row_30, top_k)
    
    train_values = train.values
    weighted_sequence = weights.reshape(1, -1) @ train_values
    weighted_seq = pd.Series(weighted_sequence.flatten(), index=train.columns)
    
    return weighted_seq

def compare(test, train, top_k, is_same, is_buy):
    '''
    is_same:是否只取同月份数据
    is_buy:是否做空
    '''
    # 预先提取所有30分钟片段
    train_30 = train.apply(get_first_30min, axis=1)
    
    # 存储结果
    # 初始化结果表格
    result = pd.DataFrame(columns=[
        '实际第30项', '实际收盘', 
        '预测第30项', '预测收盘',
        '实际方向', '预测方向', 
        '方向一致', '收益率'
    ])
    
    for date, test_row in test.iterrows():
        
        # 导入前30分钟数据
        test_row_30 = get_first_30min(test_row)
        
        if is_same:
            # 用历史同月份的作为训练集
            index = train.index.month == test_row.name.month
            train_m = train[index]
            train_30_m = train_30[index]
            
            # 计算相似序列
            test_seq = cheat(test_row_30, train_m, train_30_m, top_k)
        
        else:
            # 用7/8月份
            test_seq = cheat(test_row_30, train, train_30, top_k)
        
        # 获取关键值
        actual_30 = test_row.iloc[29]    # 实际第30项
        actual_last = test_row.iloc[-1]  # 实际收盘
        pred_30 = test_seq.iloc[29]      # 预测第30项
        pred_last = test_seq.iloc[-1]    # 预测收盘
        
        # 计算方向和收益率
        actual_dir = 1 if actual_last > actual_30 else 0
        pred_dir = 1 if pred_last > pred_30 else 0
        direction_match = actual_dir == pred_dir
        
        if pred_last < pred_30:
            earn = (actual_30 - actual_last) / actual_30  # 做空收益率
        elif is_buy:
            earn = -(actual_30 - actual_last) / actual_30  # 做多收益率
        else:
            earn = 0 # 不做多
        
        # 添加到结果表
        result.loc[date] = [
            actual_30, actual_last,
            pred_30, pred_last,
            actual_dir, pred_dir,
            direction_match,
            earn
        ]
    
    # 计算累计收益率
    result['累计收益'] = (1 + result['收益率']).cumprod() - 1
    
    accuracy = result['方向一致'].mean()
    print(f"方向预测准确率: {accuracy:.2%}")
    
    return result

def print_results(seq):
    # 3. 绘制损益曲线
    plt.figure(figsize=(12, 6))
    seq.plot(title='损益曲线', color='b', lw=2)
    plt.xlabel('日期')
    plt.ylabel('累计收益')
    plt.grid(True)
    
    # 标记正负收益区域
    plt.fill_between(seq.index, seq, where=(seq >= 0), 
                    facecolor='red', alpha=0.2)
    plt.fill_between(seq.index, seq, where=(seq < 0), 
                    facecolor='green', alpha=0.2)
    
    plt.show()
    
#%% 运行
if __name__ == "__main__":
    file = 'jd00.DF_1m.csv'
    top_k = 20

    train, test = read_data(file)
    result1 = compare(test, train, top_k, is_same=1, is_buy=1)
    # result2 = compare(test, train, top_k, is_same=1, is_buy=0)
    result3 = compare(test, train, top_k, is_same=0, is_buy=1)
    # result4 = compare(test, train, top_k, is_same=0, is_buy=0)
    
    print_results(result1['累计收益'])
    print_results(result1['收益率'])

    # print_results(result2['累计收益'])
    # print_results(result2['收益率'])

    








