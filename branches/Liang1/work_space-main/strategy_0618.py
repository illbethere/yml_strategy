import datetime
import pandas as pd
from datetime import datetime, timedelta
from xtquant import xtdatacenter as xtdc
from xtquant import xtdata
from read_data import get_market_data, get_main_contract_code
from cook_data import cook_data
from pocess_order import OrderManager
from backtesting import Backtest
import numpy as np

xtdc.set_token('4065054877ce5724155dbc5bcba200381ce5eb35')
xtdc.init()


class DataManager:
    """数据管理模块，负责获取和缓存价格数据"""
    
    def __init__(self):
        self.price_dict = {}
        self.current_price_cache = {}  # 新增当前价格缓存
        self.option_detail = {} # 保存交易期权详情方便读取
    
    def get_cached_price_data(self, code, current_trading_date, lookback_days, signal_levels):
        """获取缓存的价格数据 - 扩展版本，支持多个时间窗口"""
        cache_key = f"{code}_{current_trading_date}_{signal_levels}"  # 加入code到缓存键
        
        if cache_key in self.price_dict:
            return self.price_dict[cache_key]
        
        try:
            # 计算窗口范围，signal_levels为奇数时对称，为偶数时向前偏移
            if signal_levels % 2 == 1:
                # 奇数级别：例如5级时范围为 [lbd-2, lbd-1, lbd, lbd+1, lbd+2]
                half_range = signal_levels // 2
                start_window = lookback_days - half_range
                end_window = lookback_days + half_range + 1
            else:
                # 偶数级别：例如4级时范围为 [lbd-2, lbd-1, lbd, lbd+1]
                half_range = signal_levels // 2
                start_window = lookback_days - half_range + 1
                end_window = lookback_days + half_range + 1
            
            max_lookback = end_window - 1  # 最大回溯天数
            dict_data = get_market_data([code], '1d', '', current_trading_date, max_lookback)
            
            if code in dict_data and not dict_data[code].empty:
                data = dict_data[code]['close']
                
                # 计算不同时间窗口的最高价和最低价
                price_data = {}
                for window in range(start_window, end_window):
                    if window > 0 and len(data) >= window:
                        price_data[window] = {
                            'max': data.tail(window).max(),
                            'min': data.tail(window).min()
                        }
                
                self.price_dict[cache_key] = price_data
                return price_data
            else:
                return {}
                
        except Exception as e:
            print(f"获取数据错误: {e}")
            return {}
    
    def get_current_price(self, code, current_time, current_trading_date):
        """获取指定合约的当前价格"""
        cache_key = f"{code}_{current_trading_date}"
        
        if cache_key in self.current_price_cache:
            price_data = self.current_price_cache[cache_key]
        else:
            try:
                # 获取当天的分钟数据
                dict_data = get_market_data([code], '1m', current_trading_date, current_trading_date, -1)
                if code in dict_data and not dict_data[code].empty:
                    price_data = dict_data[code]
                    self.current_price_cache[cache_key] = price_data
                else:
                    print(f"无法获取 {code} 在 {current_trading_date} 的价格数据")
                    return None
            except Exception as e:
                print(f"获取当前价格错误: {e}")
                return None
        
        # 查找最接近当前时间的价格
        try:
            # 找到小于等于当前时间的最新价格
            available_data = price_data[price_data.index <= current_time]
            if not available_data.empty:
                return available_data.iloc[-1]['close']
            else:
                # 如果没有找到，使用第一个可用价格
                return price_data.iloc[0]['close'] if not price_data.empty else None
        except Exception as e:
            print(f"查找当前价格错误: {e}")
            return None

    def get_option_detail(self, code) -> dict:
        # 检查是否有缓存对应期权
        if code in self.option_detail:
            return self.option_detail[code]
        
        else:
            self.option_detail[code] = xtdata.get_option_detail_data(code)
            if self.option_detail[code] is None:
                print(f"无法获取期权详情: {code}")
                return {}
        return self.option_detail[code]

class SignalGenerator:
    """信号生成模块，负责生成交易信号"""
    
    def __init__(self):
        self.signal_count_pos = 0
        self.signal_count_neg = 0
        self.yesterday = None
        self.count = 0
    
    def generate_signal(self, current_close, price_data, current_date, max_signals, lookback_days, signal_levels):
        """生成交易信号 - 可配置级别版本"""

        """参数:
        current_close: 当前收盘价
        price_data: 历史价格数据，格式为 {窗口大小: {'max': 最高价, 'min': 最低价}}
        current_date: 当前日期
        max_signals: 生成信号所需的最小连续同向信号数
        lookback_days: 基准回溯天数
        signal_levels: 信号级别数（奇数或偶数）

        返回:
            tuple: (最终信号, 信号强度)
                最终信号: 1表示卖出PUT, -1表示卖出CALL, 0表示无信号
                信号强度: 信号的强度值
        """


        # 初始化yesterday
        if self.count == 0:
            self.yesterday = current_date
            self.count += 1
        
        # 重置计数器（新的一天）
        if self.yesterday != current_date:
            self.signal_count_pos = 0
            self.signal_count_neg = 0
        
        # 计算窗口范围
        if signal_levels % 2 == 1:
            # 奇数级别：例如5级时范围为 [lbd-2, lbd-1, lbd, lbd+1, lbd+2]
            half_range = signal_levels // 2
            start_window = lookback_days - half_range
            end_window = lookback_days + half_range + 1
        else:
            # 偶数级别：例如4级时范围为 [lbd-2, lbd-1, lbd, lbd+1]
            half_range = signal_levels // 2
            start_window = lookback_days - half_range + 1
            end_window = lookback_days + half_range + 1
        
        # 计算信号强度
        signal_strength = 0
        
        # 检查双向信号（价格高于历史最高价,或者低于最低价）
        for i, window in enumerate(range(start_window, end_window)):
            if window in price_data:
                # 正向信号
                if current_close > price_data[window]['max']:
                    signal_strength = max(signal_strength, i + 1)  # 信号强度1到signal_levels
                # 反向信号
                elif current_close < price_data[window]['min']:
                    signal_strength = min(signal_strength, -(i + 1))  # 信号强度-1到-signal_levels
                
        
        # 更新信号计数
        if signal_strength > 0:
            self.signal_count_pos += 1
            self.signal_count_neg = 0  
        elif signal_strength < 0:
            self.signal_count_neg += 1
            self.signal_count_pos = 0
        else:
            # 如果没有信号，保持当前计数不变
            pass
        
        # 生成最终信号
        final_signal = 0
        final_strength = 0
        
        if self.signal_count_pos >= max_signals and signal_strength > 0:
            final_signal = 1  # 卖出PUT信号
            final_strength = signal_strength
            self.signal_count_pos = 0
        elif self.signal_count_neg >= max_signals and signal_strength < 0:
            final_signal = -1  # 卖出CALL信号
            final_strength = abs(signal_strength)
            self.signal_count_neg = 0
        
        self.yesterday = current_date
        return final_signal, final_strength


class OptionSelector:
    """期权选择模块，负责选择合适的期权合约"""
    
    @staticmethod
    def parse_option_code(option_code):
        """解析期权代码"""
        code = option_code.split('.')[0]
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
            call_pos = code.find('C')
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
    
    @staticmethod
    def get_shorter_options(option_dict):
        """过滤重复期权，选择最短的键"""
        value_groups = {}
        for key, value in option_dict.items():
            if value not in value_groups:
                value_groups[value] = []
            value_groups[value].append(key)
        
        filtered_dict = {}
        for value, keys in value_groups.items():
            shortest_key = min(keys, key=len)
            filtered_dict[shortest_key] = value
        
        return filtered_dict
    
    def select_put_option(self, option_list_PUT, current_close, k):
        """选择PUT期权"""
        strike_obj = current_close * (1 - k)
        option_info_dict = {}
        
        for option in option_list_PUT:
            strike = self.parse_option_code(option)['strike']
            if strike >= strike_obj:
                option_info_dict[option] = strike
        
        option_info_dict = self.get_shorter_options(option_info_dict)
        option_info_dict = dict(sorted(option_info_dict.items(), key=lambda x: x[1], reverse=False))
        
        if option_info_dict:
            return list(option_info_dict.keys())[0], option_info_dict[list(option_info_dict.keys())[0]]
        return None, None
    
    def select_call_option(self, option_list_CALL, current_close, k):
        """选择CALL期权"""
        strike_obj = current_close * (1 + k)
        option_info_dict = {}
        
        for option in option_list_CALL:
            strike = self.parse_option_code(option)['strike']
            if strike <= strike_obj:
                option_info_dict[option] = strike
        
        option_info_dict = self.get_shorter_options(option_info_dict)
        option_info_dict = dict(sorted(option_info_dict.items(), key=lambda x: x[1], reverse=True))
        
        if option_info_dict:
            return list(option_info_dict.keys())[0], option_info_dict[list(option_info_dict.keys())[0]]
        return None, None


class TradingEngine:
    """交易执行模块，负责开仓和平仓操作"""
    
    def __init__(self, order_manager, option_selector):
        self.order_manager = order_manager
        self.option_selector = option_selector
        self.option_dict = {}
        self.option_df = []
        self.current_position = 0  # 当前持仓手数
        self.position_type = 0  # 持仓类型：1为PUT，-1为CALL，0为空仓
        self.current_option_code = None  # 当前持有的期权代码
    
    def can_open_position(self, current_date, open_date, expire_date, close_n):
        """检查是否可以开仓"""
        day_to_open = (current_date - open_date).days
        expire_to_open = (expire_date - open_date).days
        return day_to_open < (expire_to_open - close_n)
    
    def update_option_data(self, selected_option, start_date, end_date):
        """更新期权数据"""
        if self.option_dict == {} or selected_option != list(self.option_dict.keys())[0]:
            self.option_dict = get_market_data(codes=[selected_option], period='1m', start_time=start_date, end_time=end_date, count=-1)
            self.option_df = self.option_dict[selected_option]
            print(f"更新期权数据: {selected_option}")
    
    def get_current_total_position(self):
        """获取当前总持仓手数"""
        total_lots = 0
        for order_info in self.order_manager.open_orders.values():
            total_lots += abs(order_info['lot'])
        return total_lots
    
    def open_put_position(self, option_list_PUT, current_close, current_time, current_date, k, close_n, start_date, end_date, i, signal_strength, signal_levels):
        """开PUT仓位 - 支持增量开仓"""
        # 检查是否已有CALL持仓，如果有则不能开PUT
        if self.position_type == -1:
            return
        
        # 获取当前总持仓
        current_total = self.get_current_total_position()
        
        # 如果当前信号强度小于等于已持仓数，不开仓
        if signal_strength <= current_total:
            return
        
        # 计算需要新开的手数
        new_lots = min(signal_strength - current_total, signal_levels - current_total)
        
        if new_lots <= 0:
            return
        
        selected_option, selected_strike = self.option_selector.select_put_option(option_list_PUT, current_close, k)
        
        if selected_option:
            # 如果已有持仓但期权代码不同，则不开仓（避免持仓分散）
            if self.current_option_code and self.current_option_code != selected_option:
                print(f"期权代码变化，不开新仓: 当前持有{self.current_option_code}, 新选择{selected_option}")
                return
            
            selected_option_info = xtdata.get_option_detail_data(selected_option)
            expire_date = datetime.strptime(selected_option_info['ExpireDate'], '%Y%m%d').date()
            open_date = datetime.strptime(selected_option_info['OpenDate'], '%Y%m%d').date()
            
            self.update_option_data(selected_option, start_date, end_date)
            print(f"选择的期权: {selected_option}, 类型: PUT, 行权价: {selected_strike}, 信号强度: {signal_strength}, 当前持仓: {current_total}, 新开手数: {new_lots}")
            
            if i < len(self.option_df):
                current_option_price = self.option_df.iloc[i]['close']
                
                if self.can_open_position(current_date, open_date, expire_date, close_n):
                    short_order = self.order_manager.open_order(
                        code=selected_option,
                        position=-1,
                        price=current_option_price,
                        open_future_price=current_close,
                        open_time=current_time,
                        lot=new_lots,  # 新开手数
                        slip=0.0
                    )
                    
                    # 更新持仓状态
                    self.position_type = 1  # PUT持仓
                    self.current_option_code = selected_option
                    
                    print(f"开仓: {short_order}, 时间: {current_time}, 新开手数: {new_lots}, 总持仓: {current_total + new_lots}")
                else:
                    print(f"在{current_time}没有足够的时间开仓，距离行权日不足 {close_n} 天")
        else:
            print(f"在{current_time}没有找到满足条件的期权")
    
    def open_call_position(self, option_list_CALL, current_close, current_time, current_date, k, close_n, start_date, end_date, i, signal_strength, signal_levels):
        """开CALL仓位 - 支持增量开仓"""
        # 检查是否已有PUT持仓，如果有则不能开CALL
        if self.position_type == 1:
            return
        
        # 获取当前总持仓
        current_total = self.get_current_total_position()
        
        # 如果当前信号强度小于等于已持仓数，不开仓
        if signal_strength <= current_total:
            return
        
        # 计算需要新开的手数
        new_lots = min(signal_strength - current_total, signal_levels - current_total)
        
        if new_lots <= 0:
            return
        
        selected_option, selected_strike = self.option_selector.select_call_option(option_list_CALL, current_close, k)
        
        if selected_option:
            # 如果已有持仓但期权代码不同，则不开仓（避免持仓分散）
            if self.current_option_code and self.current_option_code != selected_option:
                print(f"期权代码变化，不开新仓: 当前持有{self.current_option_code}, 新选择{selected_option}")
                return
            
            selected_option_info = xtdata.get_option_detail_data(selected_option)
            expire_date = datetime.strptime(selected_option_info['ExpireDate'], '%Y%m%d').date()
            open_date = datetime.strptime(selected_option_info['OpenDate'], '%Y%m%d').date()
            
            self.update_option_data(selected_option, start_date, end_date)
            print(f"选择的期权: {selected_option}, 类型: CALL, 行权价: {selected_strike}, 信号强度: {signal_strength}, 当前持仓: {current_total}, 新开手数: {new_lots}")
            
            if i < len(self.option_df):
                current_option_price = self.option_df.iloc[i]['close']
                
                if self.can_open_position(current_date, open_date, expire_date, close_n):
                    short_order = self.order_manager.open_order(
                        code=selected_option,
                        position=-1,
                        price=current_option_price,
                        open_future_price=current_close,
                        open_time=current_time,
                        lot=new_lots,  # 新开手数
                        slip=0.0
                    )
                    
                    # 更新持仓状态
                    self.position_type = -1  # CALL持仓
                    self.current_option_code = selected_option
                    
                    print(f"开仓: {short_order}, 时间: {current_time}, 新开手数: {new_lots}, 总持仓: {current_total + new_lots}, 价格: {current_option_price:.2f}")
                else:
                    print(f"在{current_time}没有足够的时间开仓，距离行权日不足 {close_n} 天")
        else:
            print(f"在{current_time}没有找到满足条件的期权")
    
    def close_positions(self, current_close, current_time, current_date, end_trading_time, close_n, alarm_ratio, i):
        """平仓操作"""
        if self.order_manager.open_orders == {}:
            return
        
        for order_id, order_info in list(self.order_manager.open_orders.items()):
            open_date = order_info['open_time'].date()
            open_future_price = order_info['open_future_price']
            
            current_option_price = self.option_df.iloc[i]['close']
            
            # 获取期权信息来计算时间
            selected_option_info = xtdata.get_option_detail_data(order_info['code'])
            expire_date = datetime.strptime(selected_option_info['ExpireDate'], '%Y%m%d').date()
            
            day_to_open = (current_date - open_date).days
            expire_to_open = (expire_date - open_date).days
            dynamic_alarm_ratio = alarm_ratio + (day_to_open / expire_to_open) * 0.08
            
            option_type = self.option_selector.parse_option_code(order_info['code'])['option_type']
            
            should_close = False
            close_reason = ""
            
            if option_type == 'call':
                alarm_price = open_future_price * (1 + dynamic_alarm_ratio)
                if current_close >= alarm_price:
                    should_close = True
                    close_reason = "价格触及止损"
                elif day_to_open >= (expire_to_open - close_n):
                    should_close = True
                    close_reason = "临近到期时间"
                elif current_time == end_trading_time:
                    should_close = True
                    close_reason = "交易结束"
                    
            elif option_type == 'put':
                alarm_price = open_future_price * (1 - dynamic_alarm_ratio)
                if current_close <= alarm_price:
                    should_close = True
                    close_reason = "价格触及止损"
                elif day_to_open >= (expire_to_open - close_n):
                    should_close = True
                    close_reason = "临近到期时间"
                elif current_time == end_trading_time:
                    should_close = True
                    close_reason = "交易结束"
            
            if should_close:
                self.order_manager.close_order(
                    order_id=order_id,
                    price=current_option_price,
                    close_time=current_time
                )
                print(f"平仓: {order_id}, 时间: {current_time}, 价格: {current_option_price:.2f}, 原因: {close_reason}")
                
                # 检查是否所有持仓都已平完
                if not self.order_manager.open_orders:
                    self.position_type = 0
                    self.current_option_code = None
                    print("所有持仓已平完，重置持仓状态")


class StrategyManager:
    def __init__(self, order_manager):
        self.order_manager = order_manager
        self.data_manager = DataManager()
        self.signal_generator = SignalGenerator()
        self.option_selector = OptionSelector()
        self.trading_engine = TradingEngine(order_manager, self.option_selector)

    def fill_longer_future(self, code):
        """将短格式的期货代码转换为长格式"""
        if not code.endswith('.ZF'):
            return code
        
        base_code, suffix = code.split('.')
        
        i = 0
        while i < len(base_code) and base_code[i].isalpha():
            i += 1
        
        letters = base_code[:i]
        numbers = base_code[i:]
        
        if len(numbers) == 3:
            new_numbers = '2' + numbers
            return f"{letters}{new_numbers}.{suffix}"
        
        return code

    def check_main_contract_change(self, continuous_contract_code, current_time_str, current_main_code):
        """检查主力合约是否发生变化"""
        try:
            # 获取当前日期的主力合约
            new_main_code = get_main_contract_code(
                continuous_contract_code, 
                start_time=current_time_str, 
                end_time=current_time_str
            )
            
            # 转换为长格式以便比较
            new_main_code = self.fill_longer_future(new_main_code)
            
            # 检查是否发生变化
            if new_main_code != current_main_code:
                print(f"检测到主力合约变化: {current_main_code} -> {new_main_code}")
                
                # 获取新合约的期权列表
                xtdata.download_history_contracts()
                new_option_list_PUT = xtdata.get_option_list(undl_code=new_main_code, dedate=current_time_str, opttype='PUT')
                new_option_list_CALL = xtdata.get_option_list(undl_code=new_main_code, dedate=current_time_str, opttype='CALL')
                
                if new_option_list_PUT and new_option_list_CALL:
                    print(f"成功获取新主力合约期权: PUT={len(new_option_list_PUT)}, CALL={len(new_option_list_CALL)}")
                    return new_main_code, new_option_list_PUT, new_option_list_CALL
                else:
                    print(f"新主力合约 {new_main_code} 期权列表为空，继续使用原合约")
                    return None, None, None
            else:
                # 主力合约没有变化
                return None, None, None
                
        except Exception as e:
            print(f"检查主力合约变化失败: {e}")
            return None, None, None
        
    def cal_lot_size(self, code: str, basic_lot: int, current_date: str, lookback_days: int) -> int:
        """计算合适的开仓手数"""
        pass

    def strategy(self, continuous_contract_code: str, start_date: str, end_date: str, 
                max_signals: int = 30, lookback_days: int = 20, k: float = 0.08, 
                close_n: int = 10, alarm_ratio: float = 0.02, signal_levels: int = 5) -> pd.DataFrame:
        """主策略函数 - 支持可配置多级信号和增量开仓"""
        # 获取期货数据
        initial_code, main_code_list = get_main_contract_code(continuous_contract_code, start_time=start_date, end_time=end_date) # 获取初始主力合约代码
        main_code_list.insert(0, initial_code)  # 将初始合约代码添加到列表开头
        future_dict = get_market_data(codes=main_code_list, period='1m', start_time=start_date, end_time=end_date, count=-1)
        future_df = cook_data(raw_data=future_dict[initial_code])[['date', 'close', 'trading_date']].copy()
        end_trading_time = future_df.iloc[-1]['date']
        
        # 初始化DataFrame列
        future_df['signal_type'] = 0
        future_df['signal_strength'] = 0
        future_df['current_position'] = 0
        future_df['main_contract'] = ""
        future_df['current_price'] = 0.0
        future_df['contract_changed'] = False  # 新增合约变化标记列
        
        # 计算窗口范围
        if signal_levels % 2 == 1:
            half_range = signal_levels // 2
            start_window = lookback_days - half_range
            end_window = lookback_days + half_range + 1
        else:
            half_range = signal_levels // 2
            start_window = lookback_days - half_range + 1
            end_window = lookback_days + half_range + 1
        
        # 为每个时间窗口添加列
        for window in range(start_window, end_window):
            if window > 0:
                future_df[f'close_min_{window}'] = 0.0
                future_df[f'close_max_{window}'] = 0.0
        
        rows_to_drop = []
        
        # 获取期权列表
        current_main_code = self.fill_longer_future(initial_code)
        current_price_code = initial_code  # 用于获取价格的合约代码
        last_check_date = None  # 记录上次检查日期
        
        xtdata.download_history_contracts()
        option_list_PUT = xtdata.get_option_list(undl_code=current_main_code, dedate=start_date, opttype='PUT')
        
        option_list_CALL = xtdata.get_option_list(undl_code=current_main_code, dedate=start_date, opttype='CALL')
        
        print(f"初始主力合约: {current_main_code}")
        print(f"初始价格合约: {current_price_code}")
        print(f"使用信号级别: {signal_levels}, 时间窗口范围: [{start_window}, {end_window-1}], 最大持仓: {signal_levels}手")
        
        # 主循环
        for i in range(len(future_df)):
            # 获取当前数据
            current_time = future_df.iloc[i]['date']
            current_date = current_time.date()
            original_close = future_df.iloc[i]['close']  # 原始期货数据的价格
            current_trading_date = future_df.iloc[i]['trading_date']
            current_time_str = current_time.strftime('%Y%m%d')
            
            contract_changed = False
            
            # 每天检查一次主力合约是否变化（只在新的一天第一次循环时检查）
            if last_check_date != current_date:
                print(f"检查 {current_date} 主力合约是否变化")
                
                new_main_code, new_option_list_PUT, new_option_list_CALL = self.check_main_contract_change(
                    continuous_contract_code, current_time_str, current_main_code
                )
                
                if new_main_code and new_option_list_PUT and new_option_list_CALL:
                    # 如果有持仓，先平仓
                    if self.order_manager.open_orders:
                        print(f"主力合约变化，先平掉所有持仓")
                        for order_id, order_info in list(self.order_manager.open_orders.items()):
                            if self.trading_engine.option_df is not None and i < len(self.trading_engine.option_df):
                                current_option_price = self.trading_engine.option_df.iloc[i]['close']
                                self.order_manager.close_order(
                                    order_id=order_id,
                                    price=current_option_price,
                                    close_time=current_time
                                )
                                print(f"因合约变化平仓: {order_id}, 时间: {current_time}")
                        
                        # 重置持仓状态
                        self.trading_engine.position_type = 0
                        self.trading_engine.current_option_code = None
                    
                    # 更新合约和期权列表
                    old_main_code = current_main_code
                    current_main_code = new_main_code
                    option_list_PUT = new_option_list_PUT
                    option_list_CALL = new_option_list_CALL
                    current_price_code = new_main_code
                    contract_changed = True
                    
                    # 清理缓存，确保获取新合约的数据
                    self.data_manager.price_dict.clear()
                    self.data_manager.current_price_cache.clear()
                    
                    print(f"主力合约已更新: {old_main_code} -> {new_main_code}")
                else:
                    print(f"主力合约未变化，继续使用: {current_main_code}")
                
                last_check_date = current_date
            
            # 获取当前实际使用的价格
            if current_price_code == initial_code:
                # 如果还是初始合约，使用原始数据
                current_close = original_close
            else:
                # 如果切换了合约，获取新合约的价格
                current_close = self.data_manager.get_current_price(current_price_code, current_time, current_trading_date)
                if current_close is None:
                    print(f"无法获取新合约 {current_price_code} 的价格，使用原始价格")
                    current_close = original_close
            
            # 记录当前使用的主力合约和价格
            future_df.at[i, 'main_contract'] = current_main_code
            future_df.at[i, 'current_price'] = current_close
            future_df.at[i, 'contract_changed'] = contract_changed
            
            # 获取历史价格数据（使用当前价格合约）
            price_data = self.data_manager.get_cached_price_data(current_price_code, current_trading_date, lookback_days, signal_levels)
            
            if not price_data:
                print(f"无法获取交易时间 {current_time} 的历史数据，标记删除行 {i}")
                rows_to_drop.append(i)
                continue
            
            # 保存价格数据到DataFrame
            for window in range(start_window, end_window):
                if window > 0 and window in price_data:
                    future_df.at[i, f'close_min_{window}'] = price_data[window]['min']
                    future_df.at[i, f'close_max_{window}'] = price_data[window]['max']
            
            # 生成交易信号（使用当前实际价格）
            signal_type, signal_strength = self.signal_generator.generate_signal(
                current_close, price_data, current_date, max_signals, lookback_days, signal_levels
            )
            future_df.at[i, 'signal_type'] = signal_type
            future_df.at[i, 'signal_strength'] = signal_strength
            
            # 记录当前持仓
            current_position = self.trading_engine.get_current_total_position()
            future_df.at[i, 'current_position'] = current_position
            
            # 先检查平仓条件（平仓优先于开仓）
            self.trading_engine.close_positions(
                current_close, current_time, current_date, end_trading_time, close_n, alarm_ratio, i
            )
            
            # 执行交易（在平仓后再考虑开仓，使用当前价格）
            if signal_type == 1 and signal_strength > 0:  # 卖出PUT信号
                self.trading_engine.open_put_position(
                    option_list_PUT, current_close, current_time, current_date, 
                    k, close_n, start_date, end_date, i, signal_strength, signal_levels
                )
            elif signal_type == -1 and signal_strength > 0:  # 卖出CALL信号
                self.trading_engine.open_call_position(
                    option_list_CALL, current_close, current_time, current_date, 
                    k, close_n, start_date, end_date, i, signal_strength, signal_levels
                )
        
        # 清理无效行
        if rows_to_drop:
            future_df = future_df.drop(rows_to_drop).reset_index(drop=True)
        
        return future_df
    

    def strategy_bollinger_bands(self, continuous_contract_code: str, start_date: str, end_date: str, 
                        window_size: int = 20, num_std: float = 2.0, 
                        close_n: int = 10, alarm_ratio: float = 0.02, 
                        bb_strength_threshold: float = 0.8) -> pd.DataFrame:
        """布林带策略函数 - 基于价格与布林带的关系生成交易信号"""
        # 获取期货数据
        initial_codes = get_main_contract_code(continuous_contract_code, start_time=start_date, end_time=end_date)
        future_dict = get_market_data(codes=initial_codes, period='1m', start_time=start_date, end_time=end_date, count=-1)
        future_df = cook_data(raw_data=future_dict[initial_code])[['date', 'close', 'trading_date']].copy()
        end_trading_time = future_df.iloc[-1]['date']
        
        # 初始化DataFrame列
        future_df['signal_type'] = 0
        future_df['signal_strength'] = 0
        future_df['current_position'] = 0
        future_df['main_contract'] = ""
        future_df['current_price'] = 0.0
        future_df['contract_changed'] = False
        
        # 添加布林带相关列
        future_df['bb_middle'] = 0.0  # 布林带中轨(移动平均线)
        future_df['bb_upper'] = 0.0  # 布林带上轨
        future_df['bb_lower'] = 0.0  # 布林带下轨
        future_df['bb_width'] = 0.0  # 布林带宽度
        future_df['bb_strength'] = 0.0  # 信号强度(基于价格在布林带中的位置)
        
        rows_to_drop = []
        
        # 获取期权列表
        current_main_code = self.fill_longer_future(initial_code)
        current_price_code = initial_code  # 用于获取价格的合约代码
        last_check_date = None  # 记录上次检查日期
        
        xtdata.download_history_contracts()
        option_list_PUT = xtdata.get_option_list(undl_code=current_main_code, dedate=start_date, opttype='PUT')
        option_list_CALL = xtdata.get_option_list(undl_code=current_main_code, dedate=start_date, opttype='CALL')
        
        print(f"初始主力合约: {current_main_code}")
        print(f"初始价格合约: {current_price_code}")
        print(f"布林带参数: 窗口大小={window_size}, 标准差倍数={num_std}")
        
        # 主循环
        for i in range(len(future_df)):
            # 获取当前数据
            current_time = future_df.iloc[i]['date']
            current_date = current_time.date()
            original_close = future_df.iloc[i]['close']  # 原始期货数据的价格
            current_trading_date = future_df.iloc[i]['trading_date']
            current_time_str = current_time.strftime('%Y%m%d')
            
            contract_changed = False
            
            # 每天检查一次主力合约是否变化
            if last_check_date != current_date:
                print(f"检查 {current_date} 主力合约是否变化")
                
                new_main_code, new_option_list_PUT, new_option_list_CALL = self.check_main_contract_change(
                    continuous_contract_code, current_time_str, current_main_code
                )
                
                if new_main_code and new_option_list_PUT and new_option_list_CALL:
                    # 如果有持仓，先平仓
                    if self.order_manager.open_orders:
                        print(f"主力合约变化，先平掉所有持仓")
                        for order_id, order_info in list(self.order_manager.open_orders.items()):
                            if self.trading_engine.option_df is not None and i < len(self.trading_engine.option_df):
                                current_option_price = self.trading_engine.option_df.iloc[i]['close']
                                self.order_manager.close_order(
                                    order_id=order_id,
                                    price=current_option_price,
                                    close_time=current_time
                                )
                                print(f"因合约变化平仓: {order_id}, 时间: {current_time}")
                        
                        # 重置持仓状态
                        self.trading_engine.position_type = 0
                        self.trading_engine.current_option_code = None
                    
                    # 更新合约和期权列表
                    old_main_code = current_main_code
                    current_main_code = new_main_code
                    option_list_PUT = new_option_list_PUT
                    option_list_CALL = new_option_list_CALL
                    current_price_code = new_main_code
                    contract_changed = True
                    
                    # 清理缓存，确保获取新合约的数据
                    self.data_manager.price_dict.clear()
                    self.data_manager.current_price_cache.clear()
                    
                    print(f"主力合约已更新: {old_main_code} -> {new_main_code}")
                else:
                    print(f"主力合约未变化，继续使用: {current_main_code}")
                
                last_check_date = current_date
            
            # 获取当前实际使用的价格
            if current_price_code == initial_code:
                # 如果还是初始合约，使用原始数据
                current_close = original_close
            else:
                # 如果切换了合约，获取新合约的价格
                current_close = self.data_manager.get_current_price(current_price_code, current_time, current_trading_date)
                if current_close is None:
                    print(f"无法获取新合约 {current_price_code} 的价格，使用原始价格")
                    current_close = original_close
            
            # 记录当前使用的主力合约和价格
            future_df.at[i, 'main_contract'] = current_main_code
            future_df.at[i, 'current_price'] = current_close
            future_df.at[i, 'contract_changed'] = contract_changed
            
            # 计算布林带
            if i >= window_size:
                # 获取历史价格序列
                hist_prices = []
                for j in range(i - window_size + 1, i + 1):
                    hist_price = future_df.iloc[j]['close'] if j < len(future_df) else current_close
                    hist_prices.append(hist_price)
                
                # 计算布林带中轨(移动平均)
                middle_band = np.mean(hist_prices)
                
                # 计算布林带上轨和下轨
                std_dev = np.std(hist_prices)
                upper_band = middle_band + num_std * std_dev
                lower_band = middle_band - num_std * std_dev
                
                # 计算布林带宽度
                band_width = (upper_band - lower_band) / middle_band
                
                # 计算价格在布林带中的相对位置(标准化到[-1,1]范围)
                if upper_band > lower_band:
                    bb_strength = 2 * (current_close - lower_band) / (upper_band - lower_band) - 1
                else:
                    bb_strength = 0
                
                # 保存布林带数据到DataFrame
                future_df.at[i, 'bb_middle'] = middle_band
                future_df.at[i, 'bb_upper'] = upper_band
                future_df.at[i, 'bb_lower'] = lower_band
                future_df.at[i, 'bb_width'] = band_width
                future_df.at[i, 'bb_strength'] = bb_strength
                
                # 生成交易信号
                signal_type = 0
                signal_strength = 0
                
                # 当价格触及或突破上轨时，产生卖出CALL信号
                if current_close >= upper_band and bb_strength >= bb_strength_threshold:
                    signal_type = -1  # 卖出CALL
                    signal_strength = min(5, int(round(bb_strength * 5)))  # 信号强度1-5
                    
                # 当价格触及或突破下轨时，产生卖出PUT信号
                elif current_close <= lower_band and bb_strength <= -bb_strength_threshold:
                    signal_type = 1  # 卖出PUT
                    signal_strength = min(5, int(round(abs(bb_strength) * 5)))  # 信号强度1-5
                
                future_df.at[i, 'signal_type'] = signal_type
                future_df.at[i, 'signal_strength'] = signal_strength
                
                # 记录当前持仓
                current_position = self.trading_engine.get_current_total_position()
                future_df.at[i, 'current_position'] = current_position
                
                # 先检查平仓条件
                self.trading_engine.close_positions(
                    current_close, current_time, current_date, end_trading_time, close_n, alarm_ratio, i
                )
                
                # 执行交易
                if signal_type == 1 and signal_strength > 0:  # 卖出PUT信号
                    self.trading_engine.open_put_position(
                        option_list_PUT, current_close, current_time, current_date, 
                        0.08, close_n, start_date, end_date, i, signal_strength, 5
                    )
                elif signal_type == -1 and signal_strength > 0:  # 卖出CALL信号
                    self.trading_engine.open_call_position(
                        option_list_CALL, current_close, current_time, current_date, 
                        0.08, close_n, start_date, end_date, i, signal_strength, 5
                    )
            else:
                # 数据不足，无法计算布林带
                print(f"数据不足，无法计算 {current_time} 的布林带")
                rows_to_drop.append(i)
        
        # 清理无效行
        if rows_to_drop:
            future_df = future_df.drop(rows_to_drop).reset_index(drop=True)
        
        return future_df

if __name__ == '__main__':
    # 示例用法
    order_manager = OrderManager(
                    initial_capital=10000000,
                    contract_size=20,
                    margin_rate=0.0,
                    max_position_ratio=1,
                    fee_per_lot=8,
                    slip_rate=0.0
                )
    strategy_manager = StrategyManager(order_manager)
    
    continuous_contract_code = 'MA00.ZF'
    start_date = '20240101'
    end_date = '20250601'
    
    df = strategy_manager.strategy(
        continuous_contract_code=continuous_contract_code, 
        start_date=start_date, 
        end_date=end_date, 
        max_signals=30, 
        lookback_days=20, 
        k=0.08, 
        close_n=3, # 最后3天后转主力（或次主力） 
        alarm_ratio=0.02,
        signal_levels=5  
    )

    # df = strategy_manager.strategy_bollinger_bands(
    #     continuous_contract_code=continuous_contract_code, 
    #     start_date=start_date, 
    #     end_date=end_date,  
    #     window_size=20,
    #     num_std=2.0,
    #     bb_strength_threshold=1, 
    #     close_n=5, 
    #     alarm_ratio=0.03,
    # )
    
    backtest = Backtest(initial_capital=strategy_manager.order_manager.money, risk_free_rate=0.02)
    analysis = backtest.get_detail_analyze(pd.DataFrame(order_manager.closed_orders))
    print("策略执行完成！")
    print("所有已平仓订单：")
    for order in order_manager.closed_orders:
           print(order, '\n')
    print("详细分析结果：", analysis)