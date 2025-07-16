import datetime
import pandas as pd
from datetime import datetime, timedelta
from xtquant import xtdatacenter as xtdc
from xtquant import xtdata
from read_data import get_market_data
from cook_data import cook_data
from pocess_order import OrderManager


class StrategyManager:
    def __init__(self, order_manager):
        self.order_manager = order_manager

    def parse_option_code(self,option_code):
    
        code  = option_code.split('.')[0]
        if '-' in code:
            parts = code.split('-')
            if len(parts) == 3:
                underlying = parts[0]
                option_type = 'call' if parts[1].upper() == 'C' else 'put'
                strike = int(parts[2])
            else:
                import traceback
                traceback.print_exc()

        else:

            call_pos = code.find('C') # 找不到指定字符串的时候返回 -1
            put_pos = code.find('P')

            if call_pos != -1:
                option_type = 'call'
                underlying = code[:call_pos]
                strike = int(code[call_pos + 1:])
            elif put_pos != -1:
                option_type = 'put'
                underlying = code[:put_pos]
                strike = int(code[put_pos + 1:])
            else:
                import traceback
                traceback.print_exc()

        return {
            'option_type': option_type,
            'underlying': underlying,
            'strike': strike,
            'exchange': option_code.split('.')[-1] if '.' in option_code else None
        }


    def strategy(self, code: str, start_date: str, end_date: str, max_signals: int = None, lookback_days: int = 20, k: float = 0.08, close_n: int = 10, alarm_ratio: float = 0.02) -> pd.DataFrame:
        if max_signals is None:
            max_signals = 30

        #max_signals:该日积累该次数信号开仓，lookback_days:回溯窗口期大小，k：ratio of option's K and future price, close_n:于行权日前n天平仓
        future_dict = get_market_data(codes=[code], period='1m', start_time=start_date, end_time=end_date, count=-1)
        future_df = cook_data(raw_data=future_dict[code])[['date', 'close', 'trading_date']].copy()
        
        signal_count_pos = 0
        signal_count_neg = 0
        
        # 初始化列
        future_df['signal_type'] = 0
        future_df['close_min'] = 0.0
        future_df['close_max'] = 0.0
        
        price_dict = {}
        rows_to_drop = []
        
        for i in range(len(future_df)):
            #----------------------------------------获取当前数据----------------------------------------
            current_time = future_df.iloc[i]['date']
            current_time_str = current_time.strftime('%Y%m%d%H%M%S')
            current_date = current_time.date()
            current_date_str = current_date.strftime('%Y%m%d')
            current_close = future_df.iloc[i]['close']
            current_trading_date = future_df.iloc[i]['trading_date']

            #----------------------------------------生成交易信号----------------------------------------
            count = 0
            
            if count == 0:
                yesterday = current_date
                count += 1

            close_min = None
            close_max = None
            
            cache_key = current_trading_date
            
            if cache_key in price_dict:
                close_min = price_dict[cache_key]['close_min']
                close_max = price_dict[cache_key]['close_max']
                future_df.at[i, 'close_min'] = close_min
                future_df.at[i, 'close_max'] = close_max
            else:
                try:
                    dict_data = get_market_data([code], '1d', '', current_trading_date, lookback_days)
                    
                    if code in dict_data and not dict_data[code].empty:
                        close_min = dict_data[code]['close'].min()
                        close_max = dict_data[code]['close'].max()
                        future_df.at[i, 'close_min'] = close_min
                        future_df.at[i, 'close_max'] = close_max
                        price_dict[cache_key] = {'close_min': close_min, 'close_max': close_max}
                    else:
                        print(f"无法获取交易时间 {current_time} 的历史数据，标记删除行 {i}")
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
                
            elif current_close < close_min:
                signal_count_neg += 1
                signal_count_pos = 0  

            if signal_count_pos >= max_signals:
                future_df.at[i, 'signal_type'] = 1
                # print(f"触发卖出PUT信号，交易时间: {current_date}, 价格: {current_close:.2f}")
                signal_count_pos = 0
                
            if signal_count_neg >= max_signals:
                future_df.at[i, 'signal_type'] = -1
                # print(f"触发卖出CALL信号，交易时间: {current_date}, 价格: {current_close:.2f}")
                signal_count_neg = 0

            if yesterday != current_date:
                signal_count_pos = 0
                signal_count_neg = 0

            yesterday = current_date
            #-------------------------------------------------------------------------------------------


            #-----------------------------------------开仓模块-------------------------------------------
            # 开仓逻辑：若每天分钟级价格大于前lookback_days的max price次数超过max_signals（min同理），且当前持仓为空，则进行开仓
            # sell put signal
            if future_df.at[i, 'signal_type'] == 1 and self.open_orders == {}:
                # 获取当前期货对应的期权列表
                option_list = xtdata.get_option_list(undl_code=code,dedate=current_date_str,opt_type='PUT')
                
                # 筛选出合适的期权
                strike_obj = current_close * (1 - k)
                option_info_dict = {}
                for option in option_list:
                    strike = self.parse_option_code(option)['strike']
                    # 取远端期权
                    if strike >= strike_obj:
                        option_info_dict[option] = strike

                # 按照行权价从小到大排序
                option_info_dict = dict(sorted(option_info_dict.items(), key=lambda x: x[1], reverse=False))

                if option_info_dict:
                    selected_option = list(option_info_dict.keys())[0]
                    selected_strike = option_info_dict[selected_option]

                    # 获取当前期权的信息
                    selected_option_info = xtdata.get_option_detail_data(selected_option)
                    EndDelivDate = selected_option_info['EndDelivDate']
                    
                    print(f"选择的期权: {selected_option}, 类型: PUT, 行权价: {selected_strike}, OpenDate: {current_date}, EndDelivDate: {EndDelivDate}")
                    
                    # 获取当前期权的最新价格
                    current_option_dict = xtdata.get_market_data(option_code=selected_option, period='1m', start_time=current_time_str, end_time=current_time_str, count=1)
                    current_option_price = current_option_dict[selected_option]['close'].iloc[0]
                    # Sell Put
                    long_order = self.order_manager.open_order(
                        code=selected_option,  # 使用选择的期权代码
                        position=-1,
                        price=current_option_price,
                        open_time=current_time,
                        lot=1,
                        slip=0.0
                    )
                    print(f"开仓: {long_order}, 时间: {current_time}")

                    #open_price = current_option_price # 记录开仓价格
                    #open_date = current_date # 记录开仓日期
                else:
                    print(f"在{current_time}没有找到满足条件的期权")

            # sell call signal
            if future_df.at[i, 'signal_type'] == -1 and self.order_manager.open_orders == {}:
                # 获取当前期货对应的期权列表
                option_list = xtdata.get_option_list(undl_code=code,dedate=current_date_str,opttype='CALL')
                
                # 筛选出合适的期权
                strike_obj = current_close * (1 + k)
                option_info_dict = {}
                for option in option_list:
                    strike = self.parse_option_code(option)['strike']
                    # 取远端期权
                    if strike <= strike_obj:
                        option_info_dict[option] = strike

                # 按照行权价从大到小排序
                option_info_dict = dict(sorted(option_info_dict.items(), key=lambda x: x[1], reverse=True))

                if option_info_dict:
                    selected_option = list(option_info_dict.keys())[0]
                    selected_strike = option_info_dict[selected_option]

                    # 获取当前期权的信息
                    selected_option_info = xtdata.get_option_detail_data(selected_option)
                    EndDelivDate = selected_option_info['EndDelivDate']
                    
                    print(f"选择的期权: {selected_option}, 类型: CALL, 行权价: {selected_strike}, OpenDate: {current_date}, EndDelivDate: {EndDelivDate}")
                    
                    # 获取当前期权的最新价格
                    current_option_dict = xtdata.get_market_data(option_code=selected_option, period='1m', start_time=current_time_str, end_time=current_time_str, count=1)
                    current_option_price = current_option_dict[selected_option]['close'].iloc[0]
                    # Sell Call
                    long_order = self.order_manager.open_order(
                        code=selected_option,  # 使用选择的期权代码
                        position=-1,
                        price=current_option_price,
                        open_time=current_time,
                        lot=1,
                        slip=0.0
                    )
                    print(f"开仓: {long_order}, 时间: {current_time}")

                    #open_price = current_option_price # 记录开仓价格
                    #open_date = current_date # 记录开仓日期
                else:
                    print(f"在{current_time}没有找到满足条件的期权")
            #-------------------------------------------------------------------------------------------


            #-----------------------------------------平仓模块-------------------------------------------
            # 平仓逻辑：如果价格达到预警价格，或者日期达到在行权日前close_n天，进行平仓
            if self.open_orders != {}:
                open_date = self.order_manager.open_orders['open_time'].date()
                open_price = self.order_manager.open_orders['price']
                delta_t = (current_date - open_date).days # 目前距离开仓日的天数
                delta_T = (EndDelivDate - open_date).days # 开仓日到交割日的天数
                alarm_ratio += (delta_t / delta_T) * 0.08  # 动态调整预警比例,time越长，预警比例越高

                if self.parse_option_code(self.order_manager.open_orders['code'])['type'] == 'call':
                    alarm_price = open_price * (1 + alarm_ratio)
                    if current_close >= alarm_price or delta_t >= (delta_T - close_n):
                        self.order_manager.close_order(
                            order_id=self.order_manager.open_orders['id'],
                            price=current_close,
                            close_time=current_time
                        )
                        print(f"平仓: {self.order_manager.open_orders['id']}, 时间: {current_time}, 价格: {current_close:.2f}")

                elif self.parse_option_code(self.order_manager.open_orders['code'])['type'] == 'put':
                    alarm_price = open_price * (1 - alarm_ratio)
                    if current_close <= alarm_price or delta_t >= (delta_T - close_n):
                        self.order_manager.close_order(
                            order_id=self.order_manager.open_orders['id'],
                            price=current_close,
                            close_time=current_time
                        )
                        print(f"平仓: {self.order_manager.open_orders['id']}, 时间: {current_time}, 价格: {current_close:.2f}")
            #-------------------------------------------------------------------------------------------


if __name__ == "__main__":
    # 示例用法
    # order_manager = xtdata.OrderManager()
    order_manager = OrderManager()
    strategy_manager = StrategyManager(order_manager)
    
    code = 'ag2508.ag'
    start_date = '20230101'
    end_date = '20250601'
    
    strategy_manager.strategy(code=code, start_date=start_date, end_date=end_date)
    
    # 打印最终的DataFrame
    print(order_manager.open_orders)





