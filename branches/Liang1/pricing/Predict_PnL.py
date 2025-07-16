import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq
from datetime import datetime, date
import pandas as pd
import matplotlib.pyplot as plt

def calc_natural_days(start_date, end_date):
    
    # 将字符串转换为datetime对象
    start_dt = datetime.strptime(start_date, '%Y%m%d')
    end_dt = datetime.strptime(end_date, '%Y%m%d')
    
    # 计算日期差值
    days_diff = (end_dt - start_dt).days
    
    return days_diff

def black76_price(F, K, T, r, sigma, option_type='call'):
    d1 = (np.log(F / K) + 0.5 * sigma**2 * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == 'call':
        return np.exp(-r * T) * (F * norm.cdf(d1) - K * norm.cdf(d2))
    elif option_type == 'put':
        return np.exp(-r * T) * (K * norm.cdf(-d2) - F * norm.cdf(-d1))
    else:
        raise ValueError("option_type must be 'call' or 'put'")
    
def black76_iv(F, K, T, r, market_price, option_type='call'):
    """使用Brent法计算隐含波动率"""
    # 第一步：校验option_type
    if option_type not in ['call', 'put']:
        raise ValueError("option_type必须是'call'或'put'")
    
    # 定义方程：模型价格 - 市场价格 = 0
    def equation(sigma):
        return black76_price(F, K, T, r, sigma, option_type) - market_price
    
    # 检查市场价格的合理性
    intrinsic_value = max(F - K, 0) if option_type == 'call' else max(K - F, 0)
    if market_price < intrinsic_value:
        raise ValueError(f"{option_type}价格低于内在价值（无套利条件不成立）")
    
    # 设置波动率搜索范围（0.1%到500%）
    sigma_min, sigma_max = 0.001, 5.0
    
    # 调用Brent法求解
    try:
        iv = brentq(equation, a=sigma_min, b=sigma_max, rtol=1e-6)
        return iv
    except ValueError:
        raise ValueError(f"未找到解，请检查输入参数或扩大搜索区间")
    
def predict_PnL(F, K, T, r, market_price, option_type):
    """预测期权的PnL"""
    iv = black76_iv(F, K, T, r, market_price, option_type)

    price_changes = np.linspace(-0.1, 0.1, 100)  # 价格变化范围
    pnls = []
    
    for change in price_changes:
        # 计算新的期货价格
        new_F = F * (1 + change)
        
        # 计算新价格下的期权理论价格（使用当前IV）
        predicted_price = black76_price(new_F, K, T, r, iv, option_type)
        
        # 计算PnL
        pnl = (predicted_price - market_price) / market_price * 100 
        pnls.append(pnl)
    
    return price_changes, np.array(pnls)

def plot_pnl_analysis(F, K, T, r, market_price, option_type):
    """
    绘制期权PnL分析图
    """
    # 计算PnL数据
    price_changes, pnls = predict_PnL(F, K, T, r, market_price, option_type)
    
    # 创建图表
    plt.figure(figsize=(10, 6))
    plt.plot(price_changes * 100, pnls, 'b-', linewidth=2, label=f'{option_type.upper()} Option PnL')
    
    # 添加零线
    plt.axhline(y=0, color='r', linestyle='--', alpha=0.7, label='Break-even')
    plt.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
    
    # 指定要显示的横坐标点
    target_x_values = [-10, -7.5, -5, -2.5, 2.5, 5, 7.5, 10]
    
    # 计算对应的纵坐标值并添加标记点
    for x_val in target_x_values:
        # 找到最接近的价格变化点
        closest_idx = np.argmin(np.abs(price_changes * 100 - x_val))
        y_val = pnls[closest_idx]
        actual_x = price_changes[closest_idx] * 100
        
        # 添加标记点
        plt.plot(actual_x, y_val, 'ro', markersize=6)
        
        # 添加数值标签
        plt.annotate(f'({actual_x:.1f}%, {y_val:.1f}%)', 
                    xy=(actual_x, y_val), 
                    xytext=(5, 5), 
                    textcoords='offset points',
                    fontsize=9,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    
    # 设置标签和标题
    plt.xlabel('Change of underlying asset (%)', fontsize=12)
    plt.ylabel('PnL (%)', fontsize=12)
    plt.title(f'PnL\nPrice: {F}, Strike: {K}, Time to Expiry: {T:.4f}years', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # 添加关键信息
    current_iv = black76_iv(F, K, T, r, market_price, option_type)
    plt.text(0.02, 0.98, f'IV: {current_iv*100:.2f}%\nPrice: {market_price}', 
             transform=plt.gca().transAxes, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # 打印特定点的数值
    print("特定横坐标对应的纵坐标值:")
    for x_val in target_x_values:
        closest_idx = np.argmin(np.abs(price_changes * 100 - x_val))
        y_val = pnls[closest_idx]
        actual_x = price_changes[closest_idx] * 100
        print(f"x = {actual_x:.1f}% -> PnL = {y_val:.2f}%")
    
    plt.tight_layout()
    plt.show()
    
    return price_changes, pnls

start_date = '20250703'
end_date = '20250716'
F = 3559
K = 3450
r = 0.02
T = calc_natural_days(start_date, end_date) / 365
market_price = 19
option_type = 'put'   # 期权类型

price_changes, pnls = plot_pnl_analysis(F, K, T, r, market_price, option_type)