#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime
import os

def test_option_setup():
    """测试期权数据设置"""
    print("=== 测试期权数据设置 ===")
    
    # 1. 检查交易日历
    try:
        calendar = pd.read_pickle("./data/trading_days.pkl")
        print(f"交易日历加载成功，类型: {type(calendar)}")
        if isinstance(calendar, pd.DataFrame):
            print(f"交易日历行数: {len(calendar)}")
        elif isinstance(calendar, pd.Series):
            print(f"交易日历长度: {len(calendar)}")
        else:
            print(f"交易日历长度: {len(calendar)}")
    except Exception as e:
        print(f"交易日历加载失败: {e}")
        return
    
    # 2. 确定最新交易日
    today = datetime.now().strftime("%Y%m%d")
    if isinstance(calendar, pd.DataFrame):
        days = calendar.iloc[:, 0].tolist()
    elif isinstance(calendar, pd.Series):
        days = calendar.tolist()
    else:
        days = list(calendar)
    
    if today in days:
        idx = days.index(today)
        last_trading_day = days[idx - 1] if idx > 0 else days[0]
    else:
        last_trading_day = days[-1]
    
    print(f"今天: {today}")
    print(f"最新交易日: {last_trading_day}")
    
    # 3. 检查每日报告文件
    file = f"./data/每日报告_{last_trading_day}.xlsx"
    print(f"检查文件: {file}")
    print(f"文件存在: {os.path.exists(file)}")
    
    if not os.path.exists(file):
        print("文件不存在，尝试其他日期...")
        # 尝试其他最近的日期
        for i in range(1, 10):
            test_date = days[-i] if i <= len(days) else days[0]
            test_file = f"./data/每日报告_{test_date}.xlsx"
            if os.path.exists(test_file):
                file = test_file
                last_trading_day = test_date
                print(f"找到可用文件: {file}")
                break
    
    # 4. 读取Excel文件
    try:
        df = pd.read_excel(file)
        print(f"Excel文件读取成功，列名: {df.columns.tolist()}")
        print(f"数据行数: {len(df)}")
        print("前3行数据:")
        print(df.head(3))
        
        # 5. 检查必要列是否存在
        required_cols = ['期权合约代码', '手数', '平均开仓期权价', '交易单位']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            print(f"缺少必要列: {missing_cols}")
        else:
            print("所有必要列都存在")
            
    except Exception as e:
        print(f"Excel文件读取失败: {e}")
        return
    
    # 6. 测试数据处理
    try:
        df_copy = df.copy()
        df_copy.columns = df_copy.columns.str.strip().str.replace("\n", "")
        df_copy = df_copy.drop("日期", axis=1)
        df_copy = df_copy.dropna()
        
        print(f"处理后数据行数: {len(df_copy)}")
        print("处理后列名:", df_copy.columns.tolist())
        
        # 检查期权合约代码
        if '期权合约代码' in df_copy.columns:
            option_codes = df_copy['期权合约代码'].dropna()
            print(f"期权合约代码数量: {len(option_codes)}")
            print("前5个期权代码:", option_codes.head().tolist())
        
    except Exception as e:
        print(f"数据处理失败: {e}")

if __name__ == "__main__":
    test_option_setup() 