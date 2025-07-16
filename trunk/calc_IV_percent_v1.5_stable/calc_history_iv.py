from calc_HV_IV import calc_iv
from xtquant import xtdatacenter as xtdc
from xtquant import xtdata
import pandas as pd
from datetime import datetime
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import re
import glob



xtdc.set_token('4065054877ce5724155dbc5bcba200381ce5eb35')
xtdc.init()


class IVPercentCalculator:

    def __init__(self):
        self.put_option_list = {}
        self.call_option_list = {}


    def load_trade_calendar(self):
        """加载交易日历"""

        with open("trade_cal.txt", "r", encoding='utf-8') as f:
            df = pd.read_csv(f, encoding='utf-8-sig')
            df['cal_date'] = pd.to_datetime(df['cal_date'], format='%Y%m%d')
            df = df[df['is_open'] == 1]
            trade_dates = df['cal_date'].dt.strftime('%Y%m%d').tolist()
        return sorted(trade_dates)

    def get_last_trade_date(self, target_date: str):
        """获取目标日期之前的最后一个交易日"""

        trade_dates = self.load_trade_calendar()
        target_date_str = pd.to_datetime(target_date).strftime('%Y%m%d')

        for i, date in enumerate(trade_dates):
            if date >= target_date_str and i > 0:
                return trade_dates[i - 1]
        return trade_dates[-1] if trade_dates else None

    def load_history_iv_csv(self, code):
        """加载历史IV数据"""

        csv_file = f"iv_rsult/{code}_history_iv.csv"
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            df['date'] = df['date'].astype(str)
            print(f"历史IV数据已加载: {csv_file}")
            return df
        else:
            return pd.DataFrame(columns=['date', 'main_contract', 'put_option', 'call_option', 'put_iv', 'call_iv', 'avg_iv'])


    def save_history_iv_csv(self, code, df):
        """保存历史IV数据到CSV文件"""

        csv_file = f"iv_rsult/{code}_history_iv.csv"
        if not os.path.exists('iv_rsult'):
            os.makedirs('iv_rsult')
        df.to_csv(csv_file, index=False)
        print(f"历史IV数据已保存到: {csv_file}")

    def get_history_main_contract(self, codes: list):
        """获取历史主力合约数据"""

        period = "historymaincontract"
        if isinstance(codes, list):
            codes = codes[0]
        xtdata.download_history_data(codes, period, '', '')
        if isinstance(codes, str):
            codes = [codes]
        data = xtdata.get_market_data_ex([], codes, period)

        return data

    def get_main_contract_by_date(self, date: str, data_df: pd.DataFrame, tail: str):
        """根据日期获取主力合约"""

        if isinstance(date, str):
            target_date = pd.to_datetime(date)

        data_df = data_df.sort_values('datetime')

        mask = data_df['datetime'] <= target_date
        filtered_data = data_df[mask]

        if filtered_data.empty:
            print(f"未找到主力合约: {date}, {data_df['期货统一规则代码'].unique()}")
            return None

        lastest_record = filtered_data.iloc[-1]
        main_contract = lastest_record['期货统一规则代码']
        secondary_main_contract = lastest_record['次主力合约代码']
        if '.' not in main_contract:
            main_contract += '.' + tail
        if '.' not in secondary_main_contract:
            secondary_main_contract += '.' + tail

        return main_contract, secondary_main_contract

    def get_close_price(self, future_contract: str, date: str):
        """获取期货合约的收盘价"""

        if isinstance(date, str):
            date = pd.to_datetime(date).strftime('%Y%m%d')
        pre_date = pd.to_datetime(date) - pd.Timedelta(days=10)
        pre_date = pre_date.strftime('%Y%m%d')

        if future_contract is not None:
            xtdata.download_history_data(future_contract, period = '1d', start_time = pre_date, end_time = date)
            if isinstance(future_contract, str):
                future_contract = [future_contract]  
                data = xtdata.get_market_data_ex(field_list=[], stock_list=future_contract, period='1d', start_time='', end_time=date, count=1)
                # print(data)
                close_price = data[future_contract[0]]['close'].iloc[-1]
                return close_price

    def get_put_option_list(self, future_code: str, date: str):
        """获取PUT期权列表"""
        if future_code not in self.put_option_list:
            xtdata.download_history_contracts()
            option_list = xtdata.get_option_list(future_code, date, 'PUT', isavailavle= False)
            self.put_option_list[future_code] = option_list
        else:
            option_list = self.put_option_list[future_code]
        # print(self.put_option_list)
        return option_list  

    def get_call_option_list(self, future_code: str, date: str):
        """获取CALL期权列表"""

        if future_code not in self.call_option_list:
            xtdata.download_history_contracts()
            option_list = xtdata.get_option_list(future_code, date, 'CALL', isavailavle= False)
            self.call_option_list[future_code] = option_list
        else:
            option_list = self.call_option_list[future_code]
        # print(self.call_option_list)
        return option_list

    def get_flat_option(self, future_code: str, date: str):
        """获取平值期权"""

        close_price = self.get_close_price(future_code, date)
        if close_price is None:
            print(f"未找到{future_code}的收盘价")
            return None

        put_option_list = self.get_put_option_list(future_code, date)
        call_option_list = self.get_call_option_list(future_code, date)

        if len(put_option_list) == 0 and len(call_option_list) == 0 :
            print(f"未找到{future_code}的期权列表")
            return None

        strike_price: list[float] = []
        put_dict: dict = {}
        call_dict: dict = {}

        for option in put_option_list:
            try:
                exchange_market = '.' + option.split('.')[-1]
                option_code = option.replace(exchange_market, '')
                if '-P-' in option_code:
                    strike = float(option_code.split('-P-')[-1])
                elif 'P' in option_code:
                    strike = float(option_code.split('P')[-1])
                strike_price.append(strike)
                put_dict[strike] = option

            except Exception as e:
                print(f"解析PUT期权失败: {option}, 错误: {e}")
                continue

        for option in call_option_list:
            try:
                exchange_market = '.' + option.split('.')[-1]
                option_code = option.replace(exchange_market, '')
                if '-C-' in option_code:
                    strike = float(option_code.split('-C-')[-1])
                elif 'C' in option_code:
                    strike = float(option_code.split('C')[-1])
                if strike not in strike_price:
                    strike_price.append(strike)
                call_dict[strike] = option

            except Exception as e:
                print(f"解析CALL期权失败: {option}, 错误: {e}")
                continue

        strike_price = [float(s) for s in strike_price]

        strike_price.sort()

        put_strike = None
        put_option = None


        for strike in reversed(strike_price):
            if strike < close_price and strike in put_dict:
                put_strike = strike
                put_option = put_dict[strike]
                break


        call_strike = None
        call_option = None

        for strike in strike_price:
            if strike > close_price and strike in call_dict:
                call_strike = strike
                call_option = call_dict[strike]
                break

        result = {
            'close_price': close_price,
            'put':put_option,
            'put_strike': put_strike,
            'call': call_option,
            'call_strike': call_strike
        }

        if put_option is None or call_option is None:
            print(f"未找到平值期权: {future_code}, {date}")
            return None

        return result


    def calc_option_iv(self, future_code: str, date: str):
        """计算期权IV"""

        result = self.get_flat_option(future_code, date)
        if result is None:
            print(f"获取平值期权失败: {future_code}, {date}")
            return None
        try:
            put_option = result['put']
            call_option = result['call']
        except KeyError as e:
            print(f"获取平值期权失败: {future_code}, {date}, 错误: {e}")
            return None

        if put_option is None or call_option is None:
            print(f"未找到平值期权: {future_code}, {date}")
            return None

        if isinstance(date, str):
            if '-' in date:
                date = date.replace('-', '')
        else:
            print(f"日期格式错误: {date}")


        put_iv_dict = calc_iv(put_option, date)
        if len(put_iv_dict) == 0:
            return 999
        call_iv_dict = calc_iv(call_option, date)
        if len(call_iv_dict) == 0:
            return 999
        put_iv = put_iv_dict[put_option]['iv']
        call_iv = call_iv_dict[call_option]['iv']

        print(f"平值期权IV: {put_option, call_option}, {date}, PUT_IV: {put_iv}%, CALL_IV: {call_iv}%")

        avg_iv = (put_iv + call_iv) / 2

        return avg_iv



    def calc_miss_iv_data(self, code, start_date, end_date):
        """计算缺失的IV数据"""

        trade_dates = self.load_trade_calendar()
        tail = code.split('.')[-1]

        target_dates = [d for d in trade_dates if start_date <= d <= end_date]

        main_contract_data = self.get_history_main_contract(code)
        temp_data = main_contract_data[code]
        temp_data.columns = temp_data.columns.str.strip()
        if 'time' in temp_data.columns:
            temp_data['datetime'] = pd.to_datetime(temp_data['time'], unit='ms')

        new_records = []

        for date in target_dates:
            # if date == '20240207':
            #     breakpoint()
            try:
                print(f"处理日期: {date}")
                query_date = pd.to_datetime(date).strftime('%Y-%m-%d')
                contracts = self.get_main_contract_by_date(query_date, temp_data, tail)
                main_contract, secondary_main_contract = contracts 
                # print(f"主力合约: {main_contract}, 次主力合约: {secondary_main_contract}")

                if main_contract is None:
                    print(f"未找到主力合约: {date}")
                    continue
                
                iv_result = self.calc_option_iv(main_contract, date)
                if iv_result == 999:
                    print(f"主力合约IV计算失败: {main_contract}, {date}")
                    print(f"尝试使用次主力合约: {secondary_main_contract} 计算IV")
                    iv_result = self.calc_option_iv(secondary_main_contract, date)
                    option_info = self.get_flat_option(secondary_main_contract, date)
                    if option_info:
                        put_iv_dict = calc_iv(option_info['put'], date)
                        call_iv_dict = calc_iv(option_info['call'], date)

                        put_iv = put_iv_dict[option_info['put']]['iv']
                        call_iv = call_iv_dict[option_info['call']]['iv']

                        record = {
                            'date': date,
                            'main_contract': secondary_main_contract,
                            'put_option': option_info['put'],
                            'call_option': option_info['call'],
                            'put_iv': put_iv,
                            'call_iv': call_iv,
                            'avg_iv': iv_result
                        }
                        new_records.append(record)
                        print(f"主力合约:{secondary_main_contract}, 平均IV:{iv_result}")

                elif iv_result:
                    option_info = self.get_flat_option(main_contract, date)
                    if option_info:
                        put_iv_dict = calc_iv(option_info['put'], date)
                        call_iv_dict = calc_iv(option_info['call'], date)

                        put_iv = put_iv_dict[option_info['put']]['iv']
                        call_iv = call_iv_dict[option_info['call']]['iv']

                        record = {
                            'date': date,
                            'main_contract': main_contract,
                            'put_option': option_info['put'],
                            'call_option': option_info['call'],
                            'put_iv': put_iv,
                            'call_iv': call_iv,
                            'avg_iv': iv_result
                        }
                        new_records.append(record)
                        print(f"主力合约:{main_contract}, 平均IV:{iv_result}")
                    else:
                        print(f"未找到平值期权: {main_contract}, {date}")
                else:
                    print(f"未计算出IV: {main_contract}, {date}")
            except Exception as e:
                print(f"处理日期 {date} 时出错: {e}")

        return pd.DataFrame(new_records)

    def calc_today_percent(self, code, today = None):
        """计算今日IV百分位排名"""

        tail: str = code.split('.')[-1]
        if today is None:
            today: datetime = datetime.now().strftime('%Y%m%d')
        elif isinstance(today, str):
            today: datetime = pd.to_datetime(today).strftime('%Y%m%d')

        history_df: pd.DataFrame = self.load_history_iv_csv(code)

        last_trade_date: str = self.get_last_trade_date(today)

        if history_df.empty:
            print(f"未找到历史IV数据: {code}")
            start_date: str = '20240101'
            end_date: str = last_trade_date
            new_data: pd.DataFrame = self.calc_miss_iv_data(code, start_date, end_date)
            history_df: pd.DataFrame = new_data
            self.save_history_iv_csv(code, history_df)
        else:
            # last_record_date = pd.to_datetime(history_df['date'].iloc[-1]).strftime('%Y%m%d')
            last_record_date: str = history_df['date'].iloc[-1]
            print(f"最后记录日期: {last_record_date}, 当前日期: {today}")
            if last_record_date < last_trade_date:
                print(f"需要补齐数据: {code}, {last_record_date} 到 {last_trade_date}")
                trade_dates: list[str] = self.load_trade_calendar()
                try:
                    start_idx: str = trade_dates.index(last_record_date) + 1 if last_record_date in trade_dates else 0
                    end_idx: str = trade_dates.index(last_trade_date) + 1 if last_trade_date in trade_dates else len(trade_dates)
                except ValueError:
                    print(f"未找到最后记录日期 {last_record_date} 在交易日历中")

                if start_idx < end_idx:
                    missing_start: str = trade_dates[start_idx]
                    missing_end: str = last_trade_date
                    new_data: pd.DataFrame = self.calc_miss_iv_data(code, missing_start, missing_end)

                    if not new_data.empty:
                        new_data['date'] = new_data['date'].astype(str)
                        history_df: pd.DataFrame = pd.concat([history_df, new_data], ignore_index=True)
                        history_df: pd.DataFrame = history_df.drop_duplicates(subset=['date']).sort_values('date')
                        self.save_history_iv_csv(code, history_df)
                else:
                    print(f"没有需要补齐的数据: {code}, {last_record_date} 到 {last_trade_date}")
            else:
                print(f"已有最新数据: {code}, 数据截止日期{last_record_date}")



        print(f"计算今日{code}的IV百分位排名")

        main_contract_data = self.get_history_main_contract([code])

        temp_data = main_contract_data[code]
        temp_data.columns = temp_data.columns.str.strip()
        if 'time' in temp_data.columns:
            temp_data['datetime'] = pd.to_datetime(temp_data['time'], unit='ms')

        query_date = pd.to_datetime(today).strftime('%Y-%m-%d')
        main_contract, secondary_contract = self.get_main_contract_by_date(query_date, temp_data, tail)

        if not main_contract:
            print(f"未找到主力合约: {query_date}")
            return None

        today_iv = self.calc_option_iv(main_contract, today)
        if today_iv == 999:
            print(f"主力合约IV计算失败: {main_contract}, {today}")
            print(f"尝试使用次主力合约: {secondary_contract} 计算IV")
            today_iv = self.calc_option_iv(secondary_contract, today)
            if today_iv == 999:
                print(f"次主力合约IV计算失败: {secondary_contract}, {today}")
                return None
            history_iv_values = history_df['avg_iv'].dropna().values
            if len(history_iv_values) > 0:
                percent = (np.sum(history_iv_values <= today_iv) / len(history_iv_values)) * 100
                print(f"今日IV: {today_iv}, 百分位排名: {percent:.2f}%")

                result = {
                    'code': code,
                    'date': today,
                    'main_contract': secondary_contract,
                    'today_iv': today_iv,
                    'percentile_rank': percent,
                    'history_count': len(history_iv_values),
                    'history_mean': np.mean(history_iv_values),
                    'history_std': np.std(history_iv_values),
                    'history_min': np.min(history_iv_values),
                    'history_max': np.max(history_iv_values)
                }

        if today_iv is None:
            print(f"未计算出今日IV: {main_contract}, {today}")
            return None


        elif not history_df.empty:
            history_iv_values = history_df['avg_iv'].dropna().values
            if len(history_iv_values) > 0:
                percent = (np.sum(history_iv_values <= today_iv) / len(history_iv_values)) * 100
                print(f"今日IV: {today_iv}, 百分位排名: {percent:.2f}%")

                if percent is not None:
                    result = {
                        'code': code,
                        'date': today,
                        'main_contract': main_contract,
                        'today_iv': today_iv,
                        'percentile_rank': percent,
                        'history_count': len(history_iv_values),
                        'history_mean': np.mean(history_iv_values),
                        'history_std': np.std(history_iv_values),
                        'history_min': np.min(history_iv_values),
                        'history_max': np.max(history_iv_values)
                    }

        return result
    

    def get_signle_history_percent(self, future_simple_code: str, iv: float):
        names= os.listdir('iv_rsult')
        for name in names:
            if name.startswith(future_simple_code):
                code = name.split('_')[0]

        
        history_df = self.load_history_iv_csv(code)

        if history_df.empty:
            print(f"未找到历史IV数据: {code},需使用 calc_miss_iv_data 补齐数据")
            return None
        
        history_iv_values = history_df['avg_iv'].dropna().values
        if len(history_iv_values) == 0:
            print(f"没有历史IV数据: {code}")
            return None
        percent = (np.sum(history_iv_values <= iv) / len(history_iv_values)) * 100
        if percent is None:
            print(f"无法计算百分位排名: {code}, IV: {iv}")
            return None
        print(f"IV: {iv}, 百分位排名: {percent:.2f}%")

        plt.figure(figsize=(12, 8))
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
        plt.rcParams['axes.unicode_minus'] = False

        # 转换日期格式用于绘图
        history_df['date_plot'] = pd.to_datetime(history_df['date'], format='%Y%m%d')

        # 子图1: 历史IV时间序列
        plt.subplot(2, 2, 1)
        plt.plot(history_df['date_plot'], history_df['avg_iv'], 'b-', linewidth=1, alpha=0.7)
        plt.axhline(y=iv, color='red', linestyle='--', linewidth=2, label=f'当前IV: {iv:.2f}%')
        plt.title(f'{code} 历史IV走势')
        plt.xlabel('日期')
        plt.ylabel('IV (%)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)

        # 子图2: IV分布直方图
        plt.subplot(2, 2, 2)
        n, bins, patches = plt.hist(history_iv_values, bins=50, alpha=0.7, color='skyblue', edgecolor='black')
        plt.axvline(x=iv, color='red', linestyle='--', linewidth=2, label=f'当前IV: {iv:.2f}%')
        plt.title(f'{code} IV分布直方图')
        plt.xlabel('IV (%)')
        plt.ylabel('频次')
        plt.legend()
        plt.grid(True, alpha=0.3)

        # 子图3: 百分位排名可视化
        plt.subplot(2, 2, 3)
        sorted_iv = np.sort(history_iv_values)
        percentiles = np.arange(1, len(sorted_iv) + 1) / len(sorted_iv) * 100
        plt.plot(sorted_iv, percentiles, 'g-', linewidth=2)
        plt.axvline(x=iv, color='red', linestyle='--', linewidth=2)
        plt.axhline(y=percent, color='red', linestyle='--', linewidth=2)
        plt.scatter([iv], [percent], color='red', s=100, zorder=5, label=f'当前位置: {percent:.1f}%')
        plt.title(f'{code} IV百分位排名')
        plt.xlabel('IV (%)')
        plt.ylabel('百分位 (%)')
        plt.legend()
        plt.grid(True, alpha=0.3)

        # 子图4: 统计信息表格
        plt.subplot(2, 2, 4)
        plt.axis('off')

        # 计算统计信息
        stats_data = [
            ['统计项目', '数值'],
            ['当前IV', f'{iv:.2f}%'],
            ['百分位排名', f'{percent:.1f}%'],
            ['历史均值', f'{np.mean(history_iv_values):.2f}%'],
            ['历史标准差', f'{np.std(history_iv_values):.2f}%'],
            ['历史最小值', f'{np.min(history_iv_values):.2f}%'],
            ['历史最大值', f'{np.max(history_iv_values):.2f}%'],
            ['数据点数量', f'{len(history_iv_values)}']
        ]

        table = plt.table(cellText=stats_data[1:], colLabels=stats_data[0], 
                         cellLoc='center', loc='center',
                         colWidths=[0.4, 0.3])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)

        plt.suptitle(f'{code} IV百分位分析 - 当前IV: {iv}% (第{percent:.1f}百分位)', 
                    fontsize=14, fontweight='bold')
        plt.tight_layout()

        # 保存图片
        filename = f'iv_picture/iv_analysis_{code}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
        if not os.path.exists('iv_picture'):
            os.makedirs('iv_picture')


            
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"图表已保存: {filename}")

        # 显示图片
        # plt.show()

        return {
            'code': code,
            'current_iv': iv,
            'percentile': percent,
            'history_mean': np.mean(history_iv_values),
            'history_std': np.std(history_iv_values),
            'history_min': np.min(history_iv_values),
            'history_max': np.max(history_iv_values),
            'data_count': len(history_iv_values)
        }

    def get_today_picture(self, code: str, date: str = None):
        """计算今日的IV百分位排位，并产出图片，每次传入一个连续合约代码"""

        if date == None:
            date = datetime.now().strftime('%Y%m%d')

        main_contract = xtdata.get_main_contract(code)
        option_result = xtdata.get_option_undl_data(main_contract)
        # print(option_result)

        close_price = self.get_close_price(main_contract, date)
        if close_price is None:
            print(f"未找到{main_contract}的收盘价")
            return None
        
        call_options = {}
        put_options = {}

        for option in option_result:
            try:
                short_option = option[2:]
                if 'C' in short_option and 'P' not in short_option:
                    if '-' in short_option:
                        strike_str = short_option.split('-C-')[-1]
                        strike = float(strike_str[:-3])
                        call_options[strike] = option
                    else:
                        strike_str = short_option.split('C')[-1]
                        strike = float(strike_str[:-3])
                        call_options[strike] = option
                elif 'P' in short_option and 'C' not in short_option:
                    if '-' in short_option:
                        strike_str = short_option.split('-P-')[-1]
                        strike = float(strike_str[:-3])
                        put_options[strike] = option
                    else:
                        strike_str = short_option.split('P')[-1]
                        strike = float(strike_str[:-3])
                        put_options[strike] = option
            except Exception as e:
                print(f"解析期权失败: {option}, 错误: {e}")
                continue

        all_strikes = sorted(set(list(call_options.keys()) + list(put_options.keys())))

        put_option = None
        for strike in reversed(all_strikes):
            if strike < close_price and strike in put_options:
                put_option = put_options[strike]
                break

        call_option = None
        for strike in all_strikes:
            if strike > close_price and strike in call_options:
                call_option = call_options[strike]
                break

        try:
            put_result = calc_iv(put_option, date, risk_free_rate=0.02)
            call_result = calc_iv(call_option, date, risk_free_rate=0.02)

            put_iv = put_result[put_option]['iv']
            call_iv = call_result[call_option]['iv']
            avg_iv = (put_iv + call_iv) / 2

            match = re.match(r'^([a-zA-Z]+)', code)

            if match:
                self.get_signle_history_percent(match.group(1), avg_iv)
            else:
                print(f"无法解析代码: {code} 或计算IV失败")
                return None
        except Exception as e:
            import traceback
            print(f"计算IV时出错: {e}")

    def clean_history_picture(self):

        image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp']
        for extension in image_extensions:
            files = glob.glob(os.path.join('iv_picture', extension))
            for file in files:
                try:
                    os.remove(file)
                    print(f"已删除图片: {file}")
                except Exception as e:
                    print(f"删除图片失败: {file}, 错误: {e}")


        # result = self.get_flat_option(main_contract, date)
        # put_option = result['put']
        # call_option = result['call']

        # put_result = calc_iv(put_option, date, risk_free_rate= 0.02)
        # call_result = calc_iv(call_option, date, risk_free_rate= 0.02)
        # put_iv = put_result[put_option]['iv']
        # call_iv = call_result[call_option]['iv']
        # avg_iv = (put_iv + call_iv) / 2
        # match = re.match(r'^([a-zA-Z]+)', code)


if __name__ == "__main__":
    start_time = datetime.now()
    IV = IVPercentCalculator()

    with open('code(2).txt', 'r') as f:
        future_code = f.read().strip()

    codes = [code.strip() for code in future_code.split('\n') if code.strip()]

    # 需要计算的品种
    # codes: list[str] = ['c00.DF', 'TA00.ZF','ag00.SF', 'ps00.GF']
    # codes: list[str] = ['CJ00.ZF']
    # codes = [future_code]
    # print(codes)
    # date = datetime.now().strftime('%Y%m%d')
    # print(f"计算日期: {date}")
    # results: list[dict] = []

    # for code in codes:
    #     # 计算今日IV百分位排名
    #     result: dict = IV.calc_today_percent(code, date)
    #     if result:
    #         results.append(result)

    # IV.get_signle_history_percent('CJ', 28.51)

    IV.clean_history_picture()
    for code in codes:
        print(f"计算{code}的IV百分位排名")
        IV.get_today_picture(code)

    end_time = datetime.now()
    print(f"总耗时: {end_time - start_time}")