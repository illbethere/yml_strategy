import datetime
import pandas as pd
from datetime import datetime, timedelta
from read_data import get_market_data


class TrendStrategy:
    def __init__(self):
        self.signal_threshold = 30

    def get_trading_date(self, dt):
        if isinstance(dt, str):
            dt = pd.to_datetime(dt)
        
        hour = dt.hour
        
        # 夜盘时间：21:00 到次日 02:30
        if hour >= 21 or hour <= 2:
            # 如果是21:00之后，交易日为第二天
            if hour >= 21:
                trading_date = dt.date() + timedelta(days=1)
            else:
                # 如果是00:00-02:30，交易日就是当天
                trading_date = dt.date()
        else:
            # 日盘时间：09:00-15:00，交易日就是当天
            trading_date = dt.date()
        
        return trading_date.strftime('%Y%m%d')

    def cook_data(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        data = raw_data.copy()
        data.columns = data.columns.str.strip()


        data = data.dropna(subset=['date', 'time']).copy()

        if 'date' in data.columns and 'time' in data.columns:
            data['date'] = pd.to_datetime(data['date'], format='%Y%m%d%H%M%S', errors='coerce')
            data['time'] = pd.to_numeric(data['time'], errors='coerce').astype('Int64')
            
            data['trading_date'] = data['date'].apply(self.get_trading_date)
            data['date_str'] = data['trading_date']  
            
        price_columns = ['open', 'high', 'low', 'close']
        for col in price_columns:
            if col in data.columns:
                data[col] = pd.to_numeric(data[col], errors='coerce')
        
        
        print(f"数据解析完成: {len(data)} 条有效数据")
        return data

    def strategy(self, code_input: list, raw_data: pd.DataFrame, start_date: str) -> pd.DataFrame:
        df = self.cook_data(raw_data)
        
        if isinstance(code_input, list):
            code = code_input[0]
            code_list = code_input
        else:
            code = code_input
            code_list = [code_input]

        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        else:
            print("数据中不包含 'date' 列，无法进行日期处理。")
            return None
        
        start_date_obj = datetime.strptime(start_date, '%Y%m%d')
        
        df['filter_date'] = pd.to_datetime(df['trading_date'], format='%Y%m%d')
        df = df[df['filter_date'] >= start_date_obj].sort_values('date').reset_index(drop=True)

        if df.empty:
            print(f"没有找到符合交易日期范围 {start_date} 的数据。")
            return None
        
        print(f"过滤后数据量: {len(df)} 条")
        
        signal_count_pos = 0
        signal_count_neg = 0
        max_signals = 30
        lookback_days = 20
        
        # 初始化列
        df['sell_put_signal'] = 0
        df['sell_call_signal'] = 0
        df['signal_type'] = 0
        df['close_min'] = 0.0
        df['close_max'] = 0.0
        
        price_dict = {}
        rows_to_drop = []

        print("开始遍历数据...")
        
        for i in range(len(df)):
            current_date = df.iloc[i]['date']
            current_close = df.iloc[i]['close']
            
            current_trading_date = df.iloc[i]['trading_date']
            
            if i % 100 == 0:
                print(f"进度: {i}/{len(df)}, 实际时间: {current_date}, 交易日期: {current_trading_date}")

            trading_date_obj = datetime.strptime(current_trading_date, '%Y%m%d')
            pre_date = (trading_date_obj - timedelta(days=lookback_days)).strftime('%Y%m%d')

            close_min = None
            close_max = None
            
            cache_key = current_trading_date
            
            if cache_key in price_dict:
                close_min = price_dict[cache_key]['close_min']
                close_max = price_dict[cache_key]['close_max']
                df.at[i, 'close_min'] = close_min
                df.at[i, 'close_max'] = close_max
            else:
                try:
                    dict_data = get_market_data(code_list, '1d', pre_date, current_trading_date, 20)
                    
                    if code in dict_data and not dict_data[code].empty:
                        close_min = dict_data[code]['close'].min()
                        close_max = dict_data[code]['close'].max()
                        df.at[i, 'close_min'] = close_min
                        df.at[i, 'close_max'] = close_max
                        price_dict[cache_key] = {'close_min': close_min, 'close_max': close_max}
                    else:
                        print(f"无法获取交易日期 {current_trading_date} 的历史数据，标记删除行 {i}")
                        rows_to_drop.append(i)
                        continue
                        
                except Exception as e:
                    print(f"获取数据错误: {e}，标记删除行 {i}")
                    rows_to_drop.append(i)
                    continue
            
            if close_min is None or close_max is None:
                print(f"行 {i} 数据无效，标记删除")
                rows_to_drop.append(i)
                continue
            
            if current_close > close_max:
                signal_count_pos += 1
                signal_count_neg = 0  
                if signal_count_pos % 5 == 0:
                    print(f"正向信号累计: {signal_count_pos}, 交易日期: {current_trading_date}")
                
            elif current_close < close_min:
                signal_count_neg += 1
                signal_count_pos = 0  
                if signal_count_neg % 5 == 0:
                    print(f"负向信号累计: {signal_count_neg}, 交易日期: {current_trading_date}")

            if signal_count_pos >= max_signals:
                df.at[i, 'sell_put_signal'] = 1
                df.at[i, 'signal_type'] = 1
                print(f"触发卖出PUT信号，交易日期: {current_trading_date}, 价格: {current_close:.2f}")
                signal_count_pos = 0
                
            if signal_count_neg >= max_signals:
                df.at[i, 'sell_call_signal'] = 1
                df.at[i, 'signal_type'] = -1
                print(f"触发卖出CALL信号，交易日期: {current_trading_date}, 价格: {current_close:.2f}")
                signal_count_neg = 0

        if rows_to_drop:
            print(f"\n删除 {len(rows_to_drop)} 行无效数据")
            df = df.drop(rows_to_drop).reset_index(drop=True)
            print(f"删除后剩余数据: {len(df)} 条")

        df = df.dropna().reset_index(drop=True)
        
        total_put_signals = df['sell_put_signal'].sum()
        total_call_signals = df['sell_call_signal'].sum()
        
        print(f"\n=== 策略执行完成 ===")
        print(f"最终数据量: {len(df)} 条")
        print(f"卖出PUT信号: {total_put_signals} 次")
        print(f"卖出CALL信号: {total_call_signals} 次")

        return df


if __name__ == "__main__":
    start_time = datetime.now()
    
    data = pd.read_csv(r'C:\Users\HP\Desktop\myProject\strategies\data\ag2507_data.csv')
    print("原始数据预览:")
    print(data.head())

    st = TrendStrategy()
    start_date = '20250508'
    code = ['ag2507.SF']
    
    result = st.strategy(code, data, start_date)
    
    if result is not None:
        print(f"\n=== 数据检查 ===")
        
        null_counts = result.isnull().sum()
        if null_counts.sum() > 0:
            print("发现空值:")
            print(null_counts[null_counts > 0])
            result = result.fillna(0)
            print("已填充空值为0")
        else:
            print("数据中没有空值")

        output_file = r'C:\Users\HP\Desktop\myProject\strategies\data\ag2507_strategy_result.csv'
        
        try:
            result = result.reset_index(drop=True)
            
            result.to_csv(output_file, index=False, encoding='utf-8', lineterminator='\n')
            print(f"\n结果已保存到: {output_file}")
            
            saved_data = pd.read_csv(output_file)
            print(f"文件验证: 保存了 {len(saved_data)} 条记录")
            
            with open(output_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            empty_lines = [i for i, line in enumerate(lines) if line.strip() == '']
            if empty_lines:
                cleaned_lines = [line for line in lines if line.strip()]
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.writelines(cleaned_lines)
            else:
                print("文件中没有空行")
                
        except Exception as e:
            print(f" 保存失败: {e}")
        
    else:
        print("策略执行失败")

    end_time = datetime.now()
    print(f"\n策略执行完成，耗时: {end_time - start_time}")






