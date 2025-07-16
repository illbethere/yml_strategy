import datetime
import pandas as pd
from datetime import datetime, timedelta
from read_data import get_market_data


class TrendStrategy:
    def __init__(self):
        self.signal_threshold = 30

    def cook_data(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        data = raw_data.copy()

        data = data.dropna(subset=['date', 'time']).copy()

        if 'date' in data.columns and 'time' in data.columns:
            data['date'] = pd.to_datetime(data['date'], format='%Y%m%d%H%M%S', errors='coerce')
            data['time'] = pd.to_numeric(data['time'], errors='coerce').astype('Int64')
            data['date_str'] = data['date'].dt.strftime('%Y%m%d')

            # data['date'] = pd.to_numeric(data['date'], errors='coerce').astype('Int64')
            # data['time'] = pd.to_numeric(data['time'], errors='coerce').astype('Int64')
            
            # # 将时间戳转换为datetime
            # data['datetime'] = pd.to_datetime(data['time'], unit='ms', errors='coerce')
            
            # # 提取日期字符串用于过滤
            # data['date_str'] = data['datetime'].dt.strftime('%Y%m%d')
            
        # 确保价格列为数值类型
        price_columns = ['open', 'high', 'low', 'close']
        for col in price_columns:
            if col in data.columns:
                data[col] = pd.to_numeric(data[col], errors='coerce')
        
        # 删除无效数据
        data = data.dropna(subset=['close']).copy()
        
        print(f"数据解析完成: {len(data)} 条有效数据")
        return data

    def strategy(self, code_input: str, raw_data: pd.DataFrame, start_date: str):
        # df = raw_data.copy()
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
            return
        
        start_date = datetime.strptime(start_date, '%Y%m%d')
        # start_time = datetime.strptime('000900', '%H%M%S')
        # start_date = datetime.combine(start_day, start_time.time())

        df = df[df['date'] >= start_date].sort_values('date').reset_index(drop=True)

        if df.empty:
            print(f"没有找到符合日期范围 {start_date} 的数据。")
            return 
        
        signal_count_pos = 0
        signal_count_neg = 0
        max_signals = 30
        lookback_days = 20
        df['sell_put_signal'] = 0
        df['sell_call_signal'] = 0
        df['signal_type'] = 0
        # df['close_min'] = 0.0
        # df['close_max'] = 0.0
        # code_01 = code
        # code = code[0]
        price_dict = {}


        for i in range(len(df)):
            current_date = df.iloc[i]['date']
            current_close = df.iloc[i]['close']
            # print(f"Processing date: {current_date}, close: {current_close}")

            current_date_str = current_date.strftime('%Y%m%d')
            pre_date = (current_date - timedelta(days=lookback_days)).strftime('%Y%m%d')

            close_min = None
            close_max = None
            cache_key = current_date_str
            # if cache_key in price_dict:
            #     close_min = price_dict[cache_key]['close_min']
            #     close_max = price_dict[cache_key]['close_max']
            if current_date_str in price_dict:
                close_min = price_dict[current_date_str]['close_min']
                close_max = price_dict[current_date_str]['close_max']
                df.at[i, 'close_min'] = close_min
                df.at[i, 'close_max'] = close_max
            else:
                dict_data = get_market_data(code_list, '1d', pre_date, current_date_str, 20)
                try:
                    if code in dict_data and not dict_data[code].empty:
                        close_min = dict_data[code]['close'].min()
                        close_max = dict_data[code]['close'].max()
                        df.at[i, 'close_min'] = close_min
                        df.at[i, 'close_max'] = close_max
                    else:
                        continue
                    price_dict[cache_key] = {'close_min': close_min, 'close_max': close_max}
                except Exception as e:
                    continue
            
            if close_min is None or close_max is None:
                continue
            
            if current_close > close_max:
                signal_count_pos += 1
                print(f"Signal count positive: {signal_count_pos} for date {current_date_str}")
            elif current_close < close_min:
                signal_count_neg += 1
                print(f"Signal count negative: {signal_count_neg} for date {current_date_str}")

            if signal_count_pos >= max_signals:
                df.at[i, 'sell_put_signal'] = 1
                df.at[i, 'signal_type'] = 1
                signal_count_pos = 0
                # print("/////////////////////////////////////////////////////////////////////////////////////////////////////////")
            if signal_count_neg >= max_signals:
                df.at[i, 'sell_call_signal'] = 1
                df.at[i, 'signal_type'] = -1
                signal_count_neg = 0
                
                # ("/////////////////////////////////////////////////////////////////////////////////////////////////////////")

        # if rows_to_drop:
        #     print(f"标记删除行: {rows_to_drop}")
        #     df = df.drop(index=rows_to_drop).reset_index(drop=True)
        #     print(f"删除后数据行数: {len(df)}")

        return df

        

if __name__ == "__main__":
    start_time = datetime.now()
    data = pd.read_csv(r'C:\Users\HP\Desktop\myProject\strategies\data\ag2507_data.csv')
    print(data.head())

    st = TrendStrategy()
    start_date = '20250508'
    code = ['ag2507.SF']
    # raw_data = st.cook_data(data)
    result = st.strategy(code, data, start_date)
    print(result)

    with open(r'C:\Users\HP\Desktop\myProject\strategies\data\ag2507_strategy_result.csv', 'w', encoding='utf-8') as f:
        result.to_csv(f, index=False, encoding='utf-8', lineterminator='\n')

    end_time = datetime.now()
    print(f"策略执行完成，耗时: {end_time - start_time}")


            



        