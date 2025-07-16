#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime
import re

def test_option_flow():
    print("=== 期权数据完整流程测试 ===")
    
    # 1. 模拟setup_option过程
    today = datetime.now().strftime("%Y%m%d")
    calendar = pd.read_pickle("./data/trading_days.pkl")
    
    if isinstance(calendar, pd.DataFrame):
        days = calendar.iloc[:, 0].tolist()
    else:
        days = list(calendar)
    
    if today in days:
        idx = days.index(today)
        last_trading_day = days[idx - 1] if idx > 0 else days[0]
    else:
        last_trading_day = days[-1]
    
    file = f"./data/每日报告_{last_trading_day}.xlsx"
    print(f"使用文件: {file}")
    
    try:
        # 读取Excel文件
        df = pd.read_excel(file)
        df_copy = df.copy()
        df_copy.columns = df_copy.columns.str.strip().str.replace("\n", "")
        df_copy = df_copy.drop("日期", axis=1)
        df_copy = df_copy.dropna()
        
        print(f"原始数据行数: {len(df_copy)}")
        
        # 读取主力合约映射
        with open("./data/code.txt") as f:
            codes = [line.strip() for line in f]
        
        code_map = {}
        for code in codes:
            m = re.match(r"([a-zA-Z]{1,2})[0-9]*\..+", code)
            if m:
                short = m.group(1)
                code_map[short] = "." + code.split(".")[-1]
        
        print(f"代码映射: {code_map}")
        
        # 处理期权代码
        def add_exchange_suffix(option_code):
            m = re.match(r"([a-zA-Z]{1,2})", option_code)
            if m:
                short = m.group(1)
                suffix = code_map.get(short)
                if suffix and not option_code.endswith(suffix):
                    return option_code + suffix
            return option_code
        
        def extract_future_code(option_code):
            option_code = str(option_code).strip()
            if len(option_code) < 11:
                return pd.NaT
            if "-" in option_code:
                future_code = option_code.split("-")[0] + option_code[-3:]
                return future_code
            elif "P" in option_code[2:].upper():
                return option_code.split("P")[0] + option_code[-3:]
            elif "C" in option_code[2:].upper():
                return option_code.split("C")[0] + option_code[-3:]
            else:
                return option_code
        
        df_copy["option_code"] = df_copy["期权合约代码"].apply(add_exchange_suffix)
        df_copy["future_code"] = df_copy["option_code"].apply(extract_future_code)
        
        print("期权代码处理示例:")
        for i, row in df_copy.head().iterrows():
            print(f"  原始: {row['期权合约代码']} -> 处理后: {row['option_code']} -> 期货代码: {row['future_code']}")
        
        # 设置其他字段
        df_copy["pos_avg_price"] = df_copy["平均开仓期权价"]
        df_copy["pos"] = df_copy["手数"]
        df_copy["multiply"] = df_copy["交易单位"].fillna(1).astype(int)
        
        show_cols = ["option_code", "pos_avg_price", "pos", "future_code", "multiply"]
        result = df_copy[show_cols].copy()
        option_static_df = result.dropna()
        
        print(f"期权静态数据行数: {len(option_static_df)}")
        print("期权静态数据示例:")
        print(option_static_df.head())
        
        # 2. 模拟update_option过程
        print("\n=== 模拟update_option过程 ===")
        
        if option_static_df.empty:
            print("期权静态数据为空，无法更新")
            return
        
        df = option_static_df.copy()
        
        # 设置索引
        if "option_code" in df.columns:
            df.set_index("option_code", inplace=True)
        
        df.columns = [c.strip() for c in df.columns]
        opt_codes = [str(code) for code in df.index if isinstance(code, str) and "." in code]
        fut_code_arr = list(df["future_code"]) if hasattr(df["future_code"], '__iter__') else []
        fut_codes = [str(code) for code in fut_code_arr if isinstance(code, str) and "." in code]
        
        print(f"期权代码数量: {len(opt_codes)}")
        print(f"期货代码数量: {len(fut_codes)}")
        print("期权代码示例:", opt_codes[:5])
        print("期货代码示例:", fut_codes[:5])
        
        # 3. 模拟Greeks和市场数据
        print("\n=== 模拟数据获取 ===")
        
        # 模拟Greeks数据
        greeks = {}
        for code in opt_codes[:10]:  # 只模拟前10个
            greeks[code] = {
                "iv": 0.25 + (hash(code) % 100) / 1000,
                "delta": 0.5 + (hash(code) % 100) / 1000
            }
        
        # 模拟市场数据
        opt_prices_dict = {}
        fut_prices_dict = {}
        for code in opt_codes[:10]:
            opt_prices_dict[code] = {"close": pd.Series([100.0 + hash(code) % 50])}
        for code in fut_codes[:10]:
            fut_prices_dict[code] = {"close": pd.Series([200.0 + hash(code) % 100])}
        
        print(f"模拟Greeks数据: {len(greeks)} 个")
        print(f"模拟期权价格数据: {len(opt_prices_dict)} 个")
        print(f"模拟期货价格数据: {len(fut_prices_dict)} 个")
        
        # 4. 处理数据
        def pick_last_close(code, data_dict):
            v = data_dict.get(code, {})
            series = v.get("close", None)
            if hasattr(series, "iloc") and len(series) > 0:
                return float(series.iloc[-1])
            elif isinstance(series, (list, tuple)) and len(series) > 0:
                return float(series[-1])
            elif isinstance(series, (int, float)):
                return float(series)
            return None
        
        results = []
        for code, row in df.iterrows():
            future_code = row["future_code"]
            pos_avg_price = row["pos_avg_price"]
            pos = row["pos"]
            multiply = row["multiply"]
            
            # 行情
            current_opt_price = pick_last_close(code, opt_prices_dict)
            current_fut_price = pick_last_close(future_code, fut_prices_dict)
            
            # Greeks
            greek = greeks.get(code, {})
            iv = greek.get("iv", None)
            delta = greek.get("delta", None)
            
            # option_type
            code_str = str(code)
            option_type = "P" if "P" in code_str.upper() else ("C" if "C" in code_str.upper() else "")
            
            # 检查数据完整性
            if (current_opt_price is None or current_fut_price is None or not greek or iv is None or delta is None):
                print(f"数据不全，跳过: {code}")
                continue
            
            # 计算盈亏
            try:
                if (current_opt_price is not None and pos_avg_price is not None and
                    isinstance(pos, (int, float)) and isinstance(multiply, (int, float)) and pos != 0 and multiply != 0):
                    gain_loss = (float(pos_avg_price) - float(current_opt_price)) * float(pos) * float(multiply)
                else:
                    gain_loss = 0.0
            except Exception:
                gain_loss = 0.0
            
            try:
                valid = True
                for v in [gain_loss, pos_avg_price, pos, multiply]:
                    if isinstance(v, pd.Series):
                        valid = False
                if (valid and gain_loss != 0.0 and isinstance(pos_avg_price, (int, float)) and isinstance(pos, (int, float)) and isinstance(multiply, (int, float)) and pos_avg_price != 0 and pos != 0 and multiply != 0):
                    gain_loss_pct = gain_loss / (float(pos_avg_price) * abs(float(pos)) * float(multiply)) * 100
                else:
                    gain_loss_pct = 0.0
            except Exception:
                gain_loss_pct = 0.0
            
            # 报警价
            alarm_ratio = 0.02
            try:
                if current_fut_price is not None:
                    if option_type == "P":
                        alarm_price = float(current_fut_price) * (1 - alarm_ratio)
                    elif option_type == "C":
                        alarm_price = float(current_fut_price) * (1 + alarm_ratio)
                    else:
                        alarm_price = 0.0
                else:
                    alarm_price = 0.0
            except Exception:
                alarm_price = 0.0
            
            def safe_round(val, n):
                try:
                    return round(float(val), n)
                except Exception:
                    return "-"
            
            results.append({
                "option_code": code_str,
                "current_fut_price": safe_round(current_fut_price, 2),
                "option_type": option_type,
                "current_opt_price": safe_round(current_opt_price, 2),
                "pos_avg_price": safe_round(pos_avg_price, 2) if pos_avg_price is not None else "-",
                "pos": pos,
                "gain_loss": safe_round(gain_loss, 2),
                "gain_loss_pct": safe_round(gain_loss_pct, 2),
                "alarm_price": safe_round(alarm_price, 2) if alarm_price else "-",
                "iv": safe_round(iv, 4),
                "delta": safe_round(delta, 4),
            })
        
        show_df = pd.DataFrame(results)
        print(f"\n最终结果数据行数: {len(show_df)}")
        if len(show_df) > 0:
            print("最终结果示例:")
            print(show_df.head())
        else:
            print("没有生成任何结果数据")
            
    except Exception as e:
        print(f"测试过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_option_flow() 