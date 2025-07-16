# -*- coding: utf-8 -*-
"""
Created on Tue Jul  8 11:04:07 2025

@author: Astra
"""

#%% 地址和库
import os
path = r'C:\Users\Astra\Desktop\Hedging_greeks';
# os.chdir(path)

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import time
import re

import warnings
warnings.filterwarnings("ignore")

import calc_greeks
from account_search import SimplePositionQuery
from account_search import get_option_code, get_expire_time, get_latest_price


#%% 读取数据
def split_code(code):
    '''拆分期权代码
    输入：'lc2509-P-60000.GF'
    返回：['P', 2750, 'option']'''
    # 删去大商所代码横杠和后缀
    code2 = code[:-3].replace('-','')
    
    # 拆分
    result = re.findall(r'[a-zA-Z]+|[^a-zA-Z]+', code2)
    if len(result) == 4:
        return pd.Series([result[2], int(result[3]), 'option'])
    else:
        return pd.Series([None, None, 'future'])
    
def calc_current(df, sort_col='delta_cash'):
    '''计算单个账户的持仓风险和对冲池'''
    grouped = df.groupby('underlying')
    
    # 单个品种
    current_risk = {key: calc_greeks.calc_all_greeks(group, sort_col) for key, group in grouped}
    
    # 全部品种
    current_risk_all = pd.concat({class_key: df.loc['total', ['∑delta', '∑gamma', '∑vega', '∑theta', '∑rho',
           'delta_cash', 'gamma_cash', 'vega_cash', 'theta_cash']] for class_key, df in current_risk.items()}, axis=1).T
    current_risk_all = current_risk_all.sort_values(by=sort_col)
    
    current_risk['_ALL'] = current_risk_all

    return current_risk


#%% 对冲
def get_K_and_type(code):
    match = re.search(r'([A-Za-z])-?(\d+)\.', code)
    K = int(match.group(2))
    option_type = match.group(1)
    
    result = pd.Series([option_type, K])
    
    return result

def hedging_pool(underlying, current, option_num):
    '''默认单位资产的对冲池子，虚值最大档位为option_num'''
    # 标的期货信息
    info = current.dropna(how='any').iloc[0, :]
    if info.empty:
        raise ValueError(f"{underlying}: 组合中没有期权")
    
    multiplier = info['multiplier']
    F = info['F']
    T = info['T']
    
    # 期权代码
    option_code = get_option_code(underlying)
    pool = option_code.apply(get_K_and_type)
    
    pool = pd.concat([option_code, pool], axis=1)
    pool.columns = ['code_full', 'option_type', 'K']
    pool['F'] = F
    
    # 取前5的虚值期权
    call = pool[(pool['option_type']=='C') & (pool['K']>pool['F'])].sort_values('K', ascending=True)
    put = pool[(pool['option_type']=='P') & (pool['K']<pool['F'])].sort_values('K', ascending=False)
    
    pool = pd.concat([call.head(option_num), put.head(option_num)], axis=0)
    
    # 取一单位买入
    pool['num'] = 1
    
    pool['multiplier'] = multiplier
    pool['T'] = T
    
    # 计算price
    pool['price'] = pool['code_full'].apply(get_latest_price)
    
    # 添加标的期货
    pool['type'] = 'option'
    future = pd.DataFrame([underlying, None, None, F, 1, multiplier, None, None, 'future'], index=pool.columns)
    pool = pd.concat([pool, future.T], axis=0)
    
    return pool

def hedging(current_risk, option_num):
    '''生成对冲池子，最大虚值档位为option_num'''
    hedging = {}
    for underlying, current in current_risk.items():
        if underlying != '_ALL':
            pool = hedging_pool(underlying, current, option_num)
            pool_risk = calc_greeks.calc_all_greeks(pool, sort_col='code_full', is_total=0)
            
            hedging[underlying] = pd.concat([current, pool_risk], axis=0)
    
    hedging['_ALL'] = current_risk['_ALL']
    
    return hedging
    

#%% 运行
def run(sort_col='delta_cash', option_num=10, is_hedging=1):
    '''参数分别为: 排序变量；对冲池最大虚值档位；是否生成对冲池；是否导出'''
    start = time.time()
    
    # 当前持仓
    df_pos = pos_query.reqPositionStaticsSync(accountIDs)
    
    # 清洗数据
    current = df_pos[['账号', '期货代码', '合约代码', '期权现价', '期货现价', '到期时间', '合约乘数']]
    current.columns = ['account', 'underlying', 'code_full', 'price', 'F', 'T', 'multiplier']
    current['num'] = df_pos['总持仓'] * df_pos['方向']
    current[['option_type', 'K', 'type']] = current['code_full'].apply(split_code)
    
    dct_pos = {name: df for name, df in current.groupby('account')}
    
    print('读取仓位用时（累计）：', time.time() - start)
    
    # 计算风险
    risk = {}
    for name, df in dct_pos.items():
        risk[name] = calc_current(df, sort_col)
    
    print('计算风险用时（累计）：', time.time() - start)
    
    # 对冲
    if is_hedging:
        for name, df in risk.items():
            risk[name] = hedging(df, option_num)
    
        print('生成对冲池用时（累计）：', time.time() - start)
            
    return risk

def output(risk):
    today = datetime.now().strftime('%m%d_%H%M')
    for name, dct in risk.items():
        with pd.ExcelWriter(f"RESULTS/{today}_risk_{name}.xlsx") as writer:
            dct['_ALL'].to_excel(writer, sheet_name="All", float_format="%.4f")
            
            for class_key, df in dct.items():
                if class_key != '_ALL':
                    df = df[['code_full', 'num', 'multiplier', 'price', 'T', 'F', 'sigma',
                             'delta_cash', 'gamma_cash', 'vega_cash', 'theta_cash', '∑rho']]
                    df.to_excel(writer, sheet_name=str(class_key), float_format="%.4f")


if __name__ == "__main__":
    # 登录
    server_addr = "192.168.10.100:65300"
    username = "唐斌"
    password = "yml666888"
    accountIDs = ["8000138", "709981"]
    
    pos_query = SimplePositionQuery(server_addr, username, password, accountIDs[0])
    pos_query.init()
    pos_query.join()
    
    while not pos_query.connected:
        time.sleep(0.1)
    pos_query.doLogin()
    while not all(aid in pos_query.accountKeyDict for aid in accountIDs):
        time.sleep(0.1)
    
    # 运行
    sort_col = 'delta_cash' # 排序变量
    option_num = 5 # 对冲池最大虚值档位
    is_hedging = 1 # 是否生成对冲池
    
    risk = run(sort_col, option_num, is_hedging)
    '''参数分别为: 排序变量；对冲池最大虚值档位；是否生成对冲池'''
    
    # output(risk)
    





