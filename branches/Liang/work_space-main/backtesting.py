import pandas as pd
from pandas import DataFrame

from read_data import *
import numpy as np
from datetime import datetime, timedelta, time
import os
import matplotlib.pyplot as plt

class Backtest:
    def __init__(self, initial_capital, risk_free_rate):
        self.trading_calendar_path = "./data/trading_calendar.pkl"
        self.trading_calendar = []
        self.initial_capital = initial_capital  # 使用参数传入
        self.risk_free_rate = risk_free_rate

    def get_trading_calendar(self):
        if os.path.exists(self.trading_calendar_path):
            trading_calendar = read_history_file(self.trading_calendar_path)
            trading_calendar = trading_calendar.values.flatten().tolist()
            return trading_calendar
        else:


            raise FileNotFoundError(f"Trading calendar file not found at {self.trading_calendar_path}")

    def get_trading_days(self, start_date: str, close_date: str) -> list:
        trading_calendar = self.get_trading_calendar()
        trade_cal = []
        
        if isinstance(start_date, pd.Timestamp):
            start_date = start_date.strftime('%Y%m%d')
        if isinstance(close_date, pd.Timestamp):
            close_date = close_date.strftime('%Y%m%d')

        if start_date in trading_calendar:
            if close_date in trading_calendar:
                trade_cal = trading_calendar[trading_calendar.index(start_date):trading_calendar.index(close_date) + 1]
        return trade_cal

    def get_detail_analyze(self, df, initial_capital: int = None, risk_free_rate: float = None) -> str | DataFrame:

        
        if df.empty:
            print("警告: 没有交易数据")
            return pd.DataFrame()
        
        # 使用传入参数或实例属性
        if initial_capital is None:
            initial_capital = self.initial_capital
        if risk_free_rate is None:
            risk_free_rate = self.risk_free_rate
            
        trading_calendar = self.get_trading_calendar()
        results = {}
        
        print(f"分析 {len(df)} 条交易记录，初始资金: {initial_capital:,.0f}")

        # 修复: 使用 initial_capital 而不是 OrderManager.money
        daily_profit = df.groupby(df['open_time'].dt.date)['net_profit'].sum()
        total_days = len(daily_profit)
        total_return = (df['equity'].iloc[-1] / initial_capital - 1)
        daily_avg_return = total_return / total_days if total_days > 0 else 0
        daily_volatility = daily_profit.std() / initial_capital if len(daily_profit) > 1 else 0
        annualized_volatility = daily_volatility * np.sqrt(252)
        annualized_return = daily_avg_return * 252

        results['夏普比率'] = (annualized_return - risk_free_rate) / annualized_volatility if annualized_volatility != 0 else 0

        total_profit = df[df['net_profit'] > 0]['net_profit'].sum()
        total_loss = abs(df[df['net_profit'] < 0]['net_profit'].sum())
        results['盈亏比'] = total_profit / total_loss if total_loss != 0 else float('inf')

        # 修复: 使用 initial_capital
        total_return = (df['equity'].iloc[-1] / initial_capital - 1)
        results['总收益率(%)'] = total_return * 100

        # 年化收益率计算
        try:
            start_date = pd.to_datetime(df['open_time'].iloc[0].date())
            end_date = pd.to_datetime(df['close_time'].iloc[-1].date())
            
            start_idx = trading_calendar.index(start_date.strftime('%Y%m%d'))
            end_idx = trading_calendar.index(end_date.strftime('%Y%m%d'))
            
            trading_days = end_idx - start_idx + 1
            results['年化收益率(%)'] = total_return * 252 / trading_days * 100
        except (ValueError, IndexError) as e:
            print(f"年化收益率计算失败: {e}")
            results['年化收益率(%)'] = annualized_return * 100

        # 胜率
        wins = (df['net_profit'] > 0).sum()
        results['胜率'] = wins / len(df) if len(df) > 0 else 0

        # 持有时间计算
        holding_times = []
        try:
            cal = self.get_trading_days(df['open_time'].min(), df['close_time'].max())
            
            morning_start = time(9, 30)
            morning_end = time(11, 30)
            afternoon_start = time(13, 0)
            afternoon_end = time(15, 0)

            for index, row in df.iterrows():
                open_time = row['open_time']
                close_time = row['close_time']

                open_date = open_time.date()
                close_date = close_time.date()

                open_date_str = open_date.strftime('%Y%m%d')
                close_date_str = close_date.strftime('%Y%m%d')

                try:
                    day_during = cal.index(close_date_str) - cal.index(open_date_str)
                except ValueError:
                    print(f"日期不在交易日历中: {open_date_str} 或 {close_date_str}")
                    # 使用简单的小时差作为备选
                    holding_hours = (close_time - open_time).total_seconds() / 3600
                    holding_times.append(holding_hours)
                    continue

                # 计算持有时间
                holding_time = timedelta()

                if day_during == 0:
                    if close_time.time() <= morning_end:
                        holding_time = close_time - open_time
                    elif open_time.time() >= afternoon_start:
                        holding_time = close_time - open_time
                    else:
                        morning_part = datetime.combine(open_time.date(), morning_end) - open_time
                        afternoon_part = close_time - datetime.combine(close_time.date(), afternoon_start)
                        holding_time = morning_part + afternoon_part
                else:
                    first_day_part = datetime.combine(open_time.date(), afternoon_end) - open_time
                    last_day_part = close_time - datetime.combine(close_time.date(), morning_start)

                    if open_time.time() >= afternoon_start:
                        first_day_part = datetime.combine(open_time.date(), afternoon_end) - open_time
                    elif open_time.time() <= morning_end:
                        first_day_part = (datetime.combine(open_time.date(), morning_end) - open_time) + timedelta(hours=1, minutes=30)

                    if close_time.time() <= morning_end:
                        last_day_part = close_time - datetime.combine(close_time.date(), morning_start)
                    elif close_time.time() >= afternoon_start:
                        last_day_part = close_time - datetime.combine(close_time.date(), afternoon_start)

                    full_days = day_during - 1
                    middle_days_part = timedelta(hours=4) * full_days

                    holding_time = first_day_part + middle_days_part + last_day_part

                holding_hours = round(holding_time.total_seconds() / 3600, 2)
                holding_times.append(holding_hours)

            results['平均持有时间（H）'] = sum(holding_times) / len(holding_times) if holding_times else 0
            
        except Exception as e:
            print(f"持有时间计算失败: {e}")
            results['平均持有时间（H）'] = 0

        # 最大回撤
        df_copy = df.copy()
        peaks = df_copy['equity'].cummax()
        drawdowns = (peaks - df_copy['equity']) / peaks
        results['相对最大回撤(%)'] = drawdowns.max() * 100 if len(df_copy) > 0 else 0

        lines = []
        max_key_length = max(len(str(key)) for key in results)

        for key, value in results.items():
            # 处理数值类型并保留两位小数
            if isinstance(value, (np.number, float, int)):
                formatted_value = f"{float(value):.2f}"
            else:
                formatted_value = str(value)

            # 对齐键并构建行
            key_str = str(key).ljust(max_key_length)
            lines.append(f"{key_str}: {formatted_value}")

        return "\n".join(lines)
    
    def plt_output(self, equity_df, max_time_ticks=30):
        plt.rcParams["font.family"] = ["DejaVu Sans"]
        plt.rcParams['axes.unicode_minus'] = False

        fig = plt.figure(figsize=(14, 7))

        if isinstance(equity_df, pd.DataFrame) and 'equity' in equity_df.columns:
            times = pd.to_datetime(equity_df['time'])
            plt.plot(times, equity_df['equity'], label='Equity', linewidth=2, color='blue')
        else:
            print("Error: 'equity' column not found")
            return fig

        plt.title('Equity Curve', fontsize=16)
        plt.xlabel('Time', fontsize=14)
        plt.ylabel('Equity', fontsize=14)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(loc='best')

        ax = plt.gca()
        if max_time_ticks > 0:
            ax.xaxis.set_major_locator(plt.MaxNLocator(max_time_ticks))
        plt.xticks(rotation=45)
        plt.tight_layout()

        return fig