# -*- coding: utf-8 -*-
"""
Created on Fri Jul  4 09:40:06 2025

@author: Astra
"""

#%% 地址和库
# import os
# path = r'C:\Users\Astra\Desktop\Data';
# os.chdir(path)

import numpy as np
# import pandas as pd
from scipy.stats import norm
# from datetime import datetime
from scipy.optimize import brentq


#%% 定价模型
def black76_price(F, K, T, r, sigma, option_type):
    d1 = (np.log(F / K) + 0.5 * sigma**2 * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == 'C':
        return np.exp(-r * T) * (F * norm.cdf(d1) - K * norm.cdf(d2))
    elif option_type == 'P':
        return np.exp(-r * T) * (K * norm.cdf(-d2) - F * norm.cdf(-d1))
    else:
        raise ValueError("option_type must be 'C' or 'P'")
        
def black76_iv(F, K, T, r, price, option_type):
    """使用Brent法计算隐含波动率"""
    # 第一步：校验option_type
    if option_type not in ['C', 'P']:
        raise ValueError("option_type必须是'C'或'P'")
    
    # 定义方程：模型价格 - 市场价格 = 0
    def equation(sigma):
        return black76_price(F, K, T, r, sigma, option_type) - price
    
    # 检查市场价格的合理性
    intrinsic_value = max(F - K, 0) if option_type == 'C' else max(K - F, 0)
    if price < intrinsic_value:
        raise ValueError(f"{F},{K},{T},{price},{option_type}: 价格低于内在价值（无套利条件不成立）")
    
    # 设置波动率搜索范围（0.1%到500%）
    sigma_min, sigma_max = 0.001, 5.0
    
    # 调用Brent法求解
    try:
        iv = brentq(equation, a=sigma_min, b=sigma_max, rtol=1e-6)
        return iv
    except ValueError:
        raise ValueError(f"{F},{K},{T},{price},{option_type}: 未找到解，请检查输入参数或扩大搜索区间")


#%% 希腊字母
def calc_delta(S, K, T, r, sigma, d1, option_type):
    if option_type == 'C':
        delta = np.exp(-r * T) * norm.cdf(d1)
        # delta = norm.cdf(d1)
    else:
        delta = - np.exp(-r * T) * norm.cdf(-d1)
        # delta = norm.cdf(d1) - 1
        
    return delta

def calc_gamma(S, K, T, r, sigma, d1):
    gamma = np.exp(-r * T) * norm.pdf(d1) / (S * sigma * np.sqrt(T))
    # gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))

    return gamma

def calc_vega(S, K, T, r, sigma, d1):
    vega = np.exp(-r * T) * S * norm.pdf(d1) * np.sqrt(T)
    # vega = S * norm.pdf(d1) * np.sqrt(T)

    return vega / 100

def clac_theta(S, K, T, r, sigma, d1, d2, option_type):
    if option_type == 'C':
        theta = - np.exp(-r * T) * (S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) \
                                    + r * K * norm.cdf(d2) - r * S * norm.cdf(d1))
        # theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) \
        #          - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
    else:
        theta = - np.exp(-r * T) * (S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) \
                                    - r * K * norm.cdf(-d2) + r * S * norm.cdf(-d1))
        # theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) \
        #          + r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365
            
    return theta / 365

def calc_rho(S, K, T, r, sigma, d1, d2, option_type):
    if option_type == 'C':
        rho = - T * np.exp(-r * T) * (S * norm.cdf(d1) - K * norm.cdf(d2))
        # rho = K * T * np.exp(-r * T) * norm.cdf(d2)
    else:
        rho = - T * np.exp(-r * T) * (K * norm.cdf(-d2) - S * norm.cdf(-d1))
        # rho = -K * T * np.exp(-r * T) * norm.cdf(-d2)

    return rho / 100

def calc_greeks_letter(F, K, T, price, option_type, r = None):
    if r is None:
        r = 0.02
        
    sigma = black76_iv(F, K, T, r, price, option_type)
    
    if sigma is not None:
        S = F
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        delta = calc_delta(S, K, T, r, sigma, d1, option_type)
        gamma = calc_gamma(S, K, T, r, sigma, d1)
        vega = calc_vega(S, K, T, r, sigma, d1)
        theta = clac_theta(S, K, T, r, sigma, d1, d2, option_type)
        rho = calc_rho(S, K, T, r, sigma, d1, d2, option_type)
        
        # result = pd.Series([sigma, delta, gamma, vega, theta, rho])
        
        return sigma, delta, gamma, vega, theta, rho
    
    else:
        raise ValueError("Fail to calculate the IV.")
    
    
#%% 计算风险
def calc_single_greeks(current_row):
    '''计算单位资产希腊字母、持仓希腊字母、持仓希腊字母现金风险敞口'''
    # 计算希腊字母
    current_type = current_row['type']
    F = current_row['F']
    
    if current_type == 'option':
        K = current_row['K']
        T = current_row['T'] / 365
        price = current_row['price']
        option_type = current_row['option_type']
        
        sigma, delta, gamma, vega, theta, rho = calc_greeks_letter(F, K, T, price, option_type)

    elif current_type == 'future':
        sigma, delta, gamma, vega, theta, rho = None, 1, 0, 0, 0, 0
    
    row = current_row.copy()
    
    row['sigma'] = sigma
    row['delta'] = delta
    row['gamma'] = gamma
    row['vega'] = vega
    row['theta'] = theta
    row['rho'] = rho
    
    # 计算整体希腊字母
    n = current_row['num']
    m = current_row['multiplier']
    
    row['∑delta'] = m * n * delta
    row['∑gamma'] = m * n * gamma
    row['∑vega'] = m * n * vega
    row['∑theta'] = m * n * theta
    row['∑rho'] = m * n * rho
    
    # 计算现金风险敞口
    
    row['delta_cash'] = delta * F * m * n * 0.01
    row['gamma_cash'] = gamma * F**2 * m * n * 0.01**2 / 2
    row['vega_cash'] = vega * m * n
    row['theta_cash'] = theta * m * n
       
    return row
    
def calc_all_greeks(current_class, sort_col, is_total=1):
    '''
    输入：df, columns包含'option_type', 'K', 'type', 'num', 'multiplier', 'price', 'T', 'F'
    参数: sort_col:结果按照哪列排序，is_total:是否计算加总
    输出: df
    '''
    current_greeks = current_class.apply(calc_single_greeks, axis=1)

    current_greeks = current_greeks.sort_values(by=sort_col)
    
    current_greeks = current_greeks[['code_full', 'num', 'multiplier', 'price',
           'T', 'F', 'sigma', 'delta', 'gamma', 'vega', 'theta', 'rho', '∑delta',
           '∑gamma', '∑vega', '∑theta', '∑rho', 'delta_cash', 'gamma_cash',
           'vega_cash', 'theta_cash']]
    
    if is_total:
        current_greeks.loc['total'] = ['']*(len(current_greeks.columns)-9) + current_greeks.iloc[:, -9:].sum().tolist()
    
    return current_greeks






