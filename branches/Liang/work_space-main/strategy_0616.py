import datetime
import pandas as pd
from datetime import datetime, timedelta
from xtquant import xtdatacenter as xtdc
from xtquant import xtdata
from read_data import get_market_data, get_main_contract_code
from cook_data import cook_data
from pocess_order import OrderManager
from backtesting import Backtest

xtdc.set_token('4065054877ce5724155dbc5bcba200381ce5eb35')
xtdc.init()


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
    
    def filter_options(self, option_dict):
        # 按值分组
        value_groups = {}
        for key, value in option_dict.items():
            if value not in value_groups:
                value_groups[value] = []
            value_groups[value].append(key)
        
        # 对每个值组，选择最短的键
        filtered_dict = {}
        for value, keys in value_groups.items():
            # 找到最短的键（如果有多个相同长度，取第一个）
            shortest_key = min(keys, key=len)
            filtered_dict[shortest_key] = value
        
        return filtered_dict
    
    def cal_lot_size(self, code: str, basic_lot: int, lookback_days: int) -> int:
        pass

    def strategy(self, continuous_contract_code: str, start_date: str, end_date: str, max_signals: int = 30, lookback_days: int = 20, k: float = 0.08, close_n: int = 10, alarm_ratio: float = 0.02) -> pd.DataFrame:
        # code:连续合约代码！！！
        # max_signals:该日积累该次数信号开仓，lookback_days:回溯窗口期大小，k：ratio of option's K and future price, close_n:于行权日前n天平仓
        code = get_main_contract_code(continuous_contract_code, start_time=start_date, end_time=end_date)

        future_dict = get_market_data(codes=[code], period='1m', start_time=start_date, end_time=end_date, count=-1)
        future_df = cook_data(raw_data=future_dict[code])[['date', 'close', 'trading_date']].copy()
        end_trading_time = future_df.iloc[-1]['date'] # 获取最后一个交易日的最后一个时间点（15：00）
        
        signal_count_pos = 0
        signal_count_neg = 0
        
        # 初始化列
        future_df['signal_type'] = 0
        future_df['close_min'] = 0.0
        future_df['close_max'] = 0.0
        
        price_dict = {}
        rows_to_drop = []
        option_dict = {}
        option_df = []

        # 获取当前期货对应的期权列表
        option_list_PUT = xtdata.get_option_list(undl_code=code,dedate=start_date,opttype='PUT')
        option_list_CALL = xtdata.get_option_list(undl_code=code,dedate=start_date,opttype='CALL')
        
        for i in range(len(future_df)):
            #----------------------------------------获取当前数据----------------------------------------
            current_time = future_df.iloc[i]['date']
            _current_time_str = current_time.strftime('%Y%m%d%H%M%S')
            current_date = current_time.date()
            current_close = future_df.iloc[i]['close']
            current_trading_date = future_df.iloc[i]['trading_date']
            #print('获取数据完成！')

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
            #print('生成交易信号完成！')
            #-------------------------------------------------------------------------------------------


            #-----------------------------------------开仓模块-------------------------------------------
            # 开仓逻辑：若每天分钟级价格大于前lookback_days的max price次数超过max_signals（min同理），且当前持仓为空，则进行开仓
            # sell put signal
            if future_df.at[i, 'signal_type'] == 1 and self.order_manager.open_orders == {}:
                
                # 筛选出合适的期权
                strike_obj = current_close * (1 - k)
                option_info_dict = {}
                for option in option_list_PUT:
                    strike = self.parse_option_code(option)['strike']
                    # 取远端期权
                    if strike >= strike_obj:
                        option_info_dict[option] = strike

                # 对于一些期权，可能会有多个代码，这里进行筛选，例如SH2509.ZF和SH509.ZF
                option_info_dict = self.filter_options(option_info_dict)
                # 按照行权价从小到大排序，找出距离最近的远端期权
                option_info_dict = dict(sorted(option_info_dict.items(), key=lambda x: x[1], reverse=False))

                if option_info_dict:
                    selected_option = list(option_info_dict.keys())[0]
                    selected_strike = option_info_dict[selected_option]

                    # 获取当前期权的信息
                    selected_option_info = xtdata.get_option_detail_data(selected_option)
                    expire_date = selected_option_info['ExpireDate']
                    expire_date = datetime.strptime(expire_date, '%Y%m%d').date()
                    
                    # 更新当前期权的分钟级数据
                    if option_dict == {} or selected_option != list(option_dict.keys())[0]:
                        # 如果option_dict为空，或者当前选择的期权代码与已有数据不一致，则重新获取数据
                        option_dict = get_market_data(codes=[selected_option], period='1m', start_time=start_date, end_time=end_date, count=-1)
                        option_df = option_dict[selected_option]

                    #option_df.to_csv(r'C:\Users\HP\Desktop\project\branches\Liang\work_space-main\123.csv')

                    print(f"选择的期权: {selected_option}, 类型: PUT, 行权价: {selected_strike}, OpenDate: {current_date}, EndDelivDate: {expire_date}")
                    print(option_df.iloc[i])

                    # 获取当前期权的最新价格
                    current_option_price = option_df.iloc[i]['close']

                    # Sell Put
                    short_order = self.order_manager.open_order(
                        code=selected_option,  # 使用选择的期权代码
                        position=-1,
                        price=current_option_price,
                        open_future_price = current_close,
                        open_time=current_time,
                        lot=1,
                        slip=0.0
                    )
                    print(f"开仓: {short_order}, 时间: {current_time}")
                else:
                    print(f"在{current_time}没有找到满足条件的期权")

            # sell call signal
            if future_df.at[i, 'signal_type'] == -1 and self.order_manager.open_orders == {}:
                # 筛选出合适的期权
                strike_obj = current_close * (1 + k)
                option_info_dict = {}
                for option in option_list_CALL:
                    strike = self.parse_option_code(option)['strike']
                    # 取远端期权
                    if strike <= strike_obj:
                        option_info_dict[option] = strike

                # 对于一些期权，可能会有多个代码，这里进行筛选，例如SH2509.ZF和SH509.ZF
                option_info_dict = self.filter_options(option_info_dict)
                # 按照行权价从大到小排序，找出距离最近的远端期权
                option_info_dict = dict(sorted(option_info_dict.items(), key=lambda x: x[1], reverse=True))
                #print(f"筛选出的期权: {option_info_dict}")
                if option_info_dict:
                    selected_option = list(option_info_dict.keys())[0]
                    selected_strike = option_info_dict[selected_option]

                    # 获取当前期权的信息
                    selected_option_info = xtdata.get_option_detail_data(selected_option)
                    expire_date = selected_option_info['ExpireDate']
                    expire_date = datetime.strptime(expire_date, '%Y%m%d').date()

                    # 更新当前期权的分钟级数据
                    if option_dict == {} or selected_option != list(option_dict.keys())[0]:
                        option_dict = get_market_data(codes=[selected_option], period='1m', start_time=start_date, end_time=end_date, count=-1)
                        option_df = option_dict[selected_option]
                        print(f"更新期权数据: {option_df}")

                    
                    print(f"选择的期权: {selected_option}, 类型: CALL, 行权价: {selected_strike}, OpenDate: {current_date}, EndDelivDate: {expire_date}")
                    
                    # 获取当前期权的最新价格
                    current_option_price = option_df.iloc[i]['close']

                    # Sell Call
                    short_order = self.order_manager.open_order(
                        code=selected_option,  # 使用选择的期权代码
                        position=-1,
                        price=current_option_price,
                        open_future_price = current_close,
                        open_time=current_time,
                        lot=1,
                        slip=0.0
                    )
                    print(f"开仓: {short_order}, 时间: {current_time},价格: {current_option_price:.2f}")
                else:
                    print(f"在{current_time}没有找到满足条件的期权")
            #-------------------------------------------------------------------------------------------


            #-----------------------------------------平仓模块-------------------------------------------
            # 平仓逻辑：如果价格达到预警价格，或者日期达到在行权日前close_n天，进行平仓
            if self.order_manager.open_orders != {}:
                for order_id, order_info in list(self.order_manager.open_orders.items()):
                    #print(order_info)
                    open_date = order_info['open_time'].date()
                    open_future_price = order_info['open_future_price']

                    # 获取当前期权的最新价格
                    current_option_price = option_df.iloc[i]['close']
                        
                    day_to_open = (current_date - open_date).days # 目前距离开仓日的天数
                    expire_to_open = (expire_date - open_date).days # 过期日距离开仓日的天数
                    dynamic_alarm_ratio = alarm_ratio + (day_to_open / expire_to_open) * 0.08  # 动态调整预警比例,time越长，预警比例越高

                    if self.parse_option_code(order_info['code'])['option_type'] == 'call':
                        alarm_price = open_future_price * (1 + dynamic_alarm_ratio)

                        if current_close >= alarm_price or day_to_open >= (expire_to_open - close_n) or current_time == end_trading_time:
                            print(f"预警价格: {alarm_price:.2f} (CALL), open_future_price: {open_future_price:.2f}, day_to_open: {day_to_open}, deliv_to_open: {delivexpire_to_open_to_open}, dynamic_alarm_ratio: {dynamic_alarm_ratio:.2f}")
                            print(f"当前价格: {current_close:.2f} (CALL)")
                            print(f"day_to_open: {day_to_open} ,expire_to_open - close_n: {expire_to_open-close_n}")
                            #print(f"当前时间: {current_time}, 结束时间: {end_trading_time}")
                            #print(f"平仓条件满足: {current_close:.2f} >= {alarm_price:.2f} (CALL) or day_to_open >= {expire_to_open - close_n} or current_time == {end_trading_time}")
                            print('-----------------------------------------------------------------------')
                            self.order_manager.close_order(
                                order_id=order_id,
                                price=current_option_price,
                                close_time=current_time
                            )
                            print(f"平仓: {order_id}, 时间: {current_time}, 价格: {current_option_price:.2f}")
                            

                    elif self.parse_option_code(order_info['code'])['option_type'] == 'put':
                        alarm_price = open_future_price * (1 - dynamic_alarm_ratio)

                        if current_close <= alarm_price or day_to_open >= (expire_to_open - close_n) or current_time == end_trading_time:
                            self.order_manager.close_order(
                                order_id=order_id,
                                price=current_option_price,
                                close_time=current_time
                            )
                            print(f"平仓: {order_id}, 时间: {current_time}, 价格: {current_option_price:.2f}")
                            
            #-------------------------------------------------------------------------------------------



if __name__ == '__main__':
    # 示例用法
    order_manager = OrderManager(
                    initial_capital=100000,
                    contract_size=20,
                    margin_rate=0.0,
                    max_position_ratio=1,
                    fee_per_lot=8,
                    slip_rate=0.0
                )
    strategy_manager = StrategyManager(order_manager)
    
    continuous_contract_code = 'TA00.ZF'  # 示例期货代码
    start_date = '20250604'
    end_date = '20250613'
    
    
    df = strategy_manager.strategy(continuous_contract_code=continuous_contract_code, start_date=start_date, end_date=end_date, max_signals=30, lookback_days=20, k=0.08, close_n=15, alarm_ratio=0.02)
    backtest = Backtest(initial_capital=strategy_manager.order_manager.money, risk_free_rate=0.02)
    analysis = backtest.get_detail_analyze(pd.DataFrame(order_manager.closed_orders))
    print("策略执行完成！")
    #print("当前持仓信息：", order_manager.open_orders)
    print("所有已平仓订单：", order_manager.closed_orders)
    print("详细分析结果：", analysis)


