#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime
import os
from xtquant import xtdata
from calc_HV_IV import calc_greeks_letter

def debug_option_data():
    print("=== 期权数据调试 ===")
    
    # 1. 检查交易日历
    try:
        calendar = pd.read_pickle("./data/trading_days.pkl")
        print(f"交易日历类型: {type(calendar)}")
        print(f"交易日历形状: {calendar.shape}")
        
        if isinstance(calendar, pd.DataFrame):
            days = calendar.iloc[:, 0].tolist()
        elif isinstance(calendar, pd.Series):
            days = calendar.tolist()
        else:
            days = list(calendar)
        
        print(f"交易日数量: {len(days)}")
        print(f"前5个交易日: {days[:5]}")
        
        today = datetime.now().strftime("%Y%m%d")
        print(f"今天: {today}")
        
        if today in days:
            idx = days.index(today)
            last_trading_day = days[idx - 1] if idx > 0 else days[0]
        else:
            last_trading_day = days[-1]
        
        print(f"使用的交易日: {last_trading_day}")
        
        # 2. 检查Excel文件
        file = f"./data/每日报告_{last_trading_day}.xlsx"
        print(f"尝试读取文件: {file}")
        
        try:
            df = pd.read_excel(file)
            print(f"Excel文件读取成功，形状: {df.shape}")
            print(f"列名: {list(df.columns)}")
            
            # 检查是否有期权数据
            if "期权合约代码" in df.columns:
                option_count = df["期权合约代码"].notna().sum()
                print(f"期权合约数量: {option_count}")
                
                if option_count > 0:
                    print("前5个期权合约:")
                    print(df["期权合约代码"].head())
                else:
                    print("没有找到期权合约数据")
            else:
                print("Excel文件中没有'期权合约代码'列")
                
        except Exception as e:
            print(f"读取Excel文件失败: {e}")
            
    except Exception as e:
        print(f"调试过程中出错: {e}")

if __name__ == "__main__":
    debug_option_data() 