import datetime
import pandas as pd
from datetime import datetime, time
from read_data import get_market_data
from functools import wraps

def filter_trading_hours(night_end_time='23:00:00'):
     
     def decorator(func):
        @wraps(func)
        def wrapper(self, code: str, raw_data: pd.DataFrame, *args, **kwargs):
            morning_start = datetime.strptime('09:00:00', '%H:%M:%S').time()
            morning_end = datetime.strptime('11:30:00', '%H:%M:%S').time()
            afternoon_start = datetime.strptime('13:30:00', '%H:%M:%S').time()
            afternoon_end = datetime.strptime('15:00:00', '%H:%M:%S').time()
            night_start = datetime.strptime('21:00:00', '%H:%M:%S').time()
            night_end = datetime.strptime(night_end_time, '%H:%M:%S').time()

            def is_trade_time(time_str: str) -> bool:
                 try:
                      current_time = datetime.strptime(time_str, '%H:%M:%S').time()
                      return (
                           (morning_start < current_time < morning_end) or
                           (afternoon_start < current_time < afternoon_end) or
                            (night_start < current_time < night_end)
                      )
                 except:
                      return False
            
            if 'timetag' in raw_data.columns:
                 raw_data['time_str'] = raw_data['timetag'].apply(self.extract_time)
                 filtered_data = raw_data[raw_data['time_str'].apply(is_trade_time)].copy()
                 filtered_data = filtered_data.drop('time_str', axis=1)
                 return func(self, code, filtered_data, *args, **kwargs)
            else:
                 print("Error: 'timetag' column not found in raw_data.")
                 return func(self, code, raw_data, *args, **kwargs)
            
        return wrapper
     return decorator


class OptionTrendStrategy:
    def __init__(self):
        pass

    def extract_time(self, datetime_str: str) -> str:
          
        dt = datetime.strptime(datetime_str, '%Y%m%d%H%M%S')

        time_str = dt.strftime('%H:%M:%S')

        return time_str
    
    def extract_date(self, date_str: str) -> str:
        try:
            return date_str[:8]
        except Exception as e:
            print(f"Error extracting date from {date_str}: {e}")
            return None
        
    def filter_date(self, raw_data: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
        raw_data_copy = raw_data.copy()
        raw_data_copy['date_str'] = raw_data_copy.index.to_series().apply(self.extract_date)

        filtered_data = raw_data_copy[
            (raw_data_copy['date_str'] >= start_date) &
            (raw_data_copy['date_str'] <= end_date)
        ].copy()

        filtered_data = filtered_data.drop('date_str', axis=1)

        return filtered_data


    # @filter_trading_hours(night_end_time='23:00:00')
    def trend_strategy(self, code: str, raw_data: pd.DataFrame,start_date: str, end_date: str) -> pd.DataFrame:
        # strat_time = datetime.strptime(strat_time, '%Y%m%d')
        # end_time = datetime.strptime(end_time, '%Y%m%d')
        # today = datetime.now().date().strftime('%Y%m%d')

        filtered_data = self.filter_date(raw_data, start_date, end_date)

        if len(filtered_data) == 0:
            print(f"没有找到符合日期范围 {start_date} 到 {end_date} 的数据。")
            return raw_data
        
        try:
            #  dict_data = get_market_data([code], '1d', start_date, end_date, 20)
        


        



        dict_data = get_market_data(code, '1d', '20250407', today, 20)
        

        if code in dict_data and not dict_data[code].empty:
                    close_min = dict_data[code]['close'].min()
                    close_max = dict_data[code]['close'].max()
                    # self.log_message(f"✓ {contract} 历史数据初始化成功: min={close_min:.2f}, max={close_max:.2f}")
        else:
            print(f"数据 {code} 获取失败！")


        raw_data['can_trade'] = 0
        raw_data['direction'] = 0


        for index, row in raw_data.iterrows():
            try:
                if row['close'] > close_max:
                    row['can_trade'] = 1
                    # 设定为sell put
                    row['direction'] = 1
                elif row['close'] < close_min:
                    row['can_trade'] = 1
                    # 设定为buy call
                    row['direction'] = -1
            except Exception as e:
                print(f"Error processing row {index}: {e}")
                continue

        return raw_data
                     
                    





        


        


