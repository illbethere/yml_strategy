import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

class GridTrade:
    def __init__(self):
        pass

    def calculate_grid_levels(self, start_price, grid_size, grid_numbers_half):
        levels = [start_price / (1 + grid_size)**i for i in range(grid_numbers_half, 0, -1)]
        levels.append(start_price)
        levels += [start_price * (1 + grid_size)**i for i in range(1, grid_numbers_half + 1)]
        return levels
    
    def find_nearest_grid_level(self, price, grid_levels):
        """找到最接近的网格级别"""
        return min(range(len(grid_levels)), key=lambda i: abs(grid_levels[i] - price))

    def calc_dgt(self, df, grid_size, grid_number_half, fee_pct):
        money = 100000
        open_price = df.iloc[0]['open']
        margin_rate = 0.14
        trade_unit = 5
        count = 0

        # 记录策略资金变化
        strategy_returns = []
        timestamps = []

        trade_map = {
            'price': 0,
            'position': 0,
            'margin': 0
        }

        grid_levels = self.calculate_grid_levels(open_price, grid_size, grid_number_half)
        print(f"Grid levels: {grid_levels[0]}")
        lower_bound = grid_levels[0]
        upper_bound = grid_levels[-1]
        current_level = self.find_nearest_grid_level(open_price, grid_levels)

        current_contracts = df.iloc[0]['contract_code']
        pre_contract = current_contracts

        df_copy = df.copy()
        df_copy['prev_close'] = df_copy['close'].shift(1)

        for index, row in df_copy.iterrows():
            current_price = row['close']
            pre_price = row['open']
            current_contracts = row['contract_code']


            if current_contracts != pre_contract:
                print(f"合约变更: {pre_contract} -> {current_contracts}")
                
                if trade_map['position'] != 0:
                    final_price = row['prev_close']  # 使用前一行的收盘价作为平仓价格
                    if pd.isna(final_price):
                        final_price = row['open']
                    if trade_map['position'] > 0:
                        profit = (final_price - trade_map['price']) * trade_map['position'] * trade_unit
                    else:
                        profit = (trade_map['price'] - final_price) * abs(trade_map['position']) * trade_unit

                    fee = final_price * abs(trade_map['position']) * trade_unit * fee_pct
                    net_profit = profit - fee
                    money += net_profit + trade_map['margin']

                    print(f"平仓: {trade_map['position']} 合约, 平仓价格: {final_price}, 当前资金: {money}, 当前持仓: {trade_map['position']}")

                old_position = trade_map['position']

                trade_map = {
                    'price': 0,
                    'position': 0,
                    'margin': 0
                }

                grid_levels = self.calculate_grid_levels(current_price, grid_size, grid_number_half)
                lower_bound = grid_levels[0]
                upper_bound = grid_levels[-1]
                current_level = self.find_nearest_grid_level(current_price, grid_levels)

                if old_position != 0:
                    new_position = old_position
                    new_price = row['open']
                    margin = abs(new_position) * new_price * margin_rate * trade_unit

                    if money >= margin:
                        money -= margin
                        trade_map['price'] = new_price
                        trade_map['position'] = new_position
                        trade_map['margin'] = margin
                        print(f"开仓: {new_position} 合约, 开仓价格: {new_price}, 当前资金: {money}, 当前持仓: {trade_map['position']}")
                    else:
                        print(f"资金不足，无法开仓: {new_price}, 当前资金: {money}, 需要保证金: {margin}")
                        

                pre_contract = row['contract_code']
                count += 1
            
            # 记录当前时间和资金
            timestamps.append(row['datetime'])
            
            # 计算当前策略总价值（现金 + 持仓价值）
            position_value = 0
            if trade_map['position'] != 0:
                if trade_map['position'] > 0:
                    # 多头持仓价值
                    position_value = (current_price - trade_map['price']) * trade_map['position'] * trade_unit
                else:
                    # 空头持仓价值
                    position_value = (trade_map['price'] - current_price) * abs(trade_map['position']) * trade_unit
            
            total_value = money + trade_map['margin'] + position_value
            strategy_returns.append(total_value)

            if current_price > pre_price:
                while current_level < len(grid_levels) - 1 and row['high'] > grid_levels[current_level + 1]:
                    current_level += 1
                    if trade_map['position'] > 0:
                        sell_price = grid_levels[current_level]
                        contracts = 1
                        profit = (sell_price - trade_map['price']) * contracts * trade_unit
                        fee = sell_price * contracts * trade_unit * fee_pct
                        net_profit = profit - fee
                        release_margin = trade_map['price'] * contracts * trade_unit * margin_rate
                        money += net_profit + release_margin

                        trade_map['margin'] -= release_margin
                        trade_map['position'] -= contracts
                        
                        count += 1
                        print(f"卖出: {contracts} 合约, 卖出价格: {sell_price}, 当前资金: {money}, 当前持仓: {trade_map['position']}, 利润: {profit}")
                    elif trade_map['position'] <= 0 and money > 0:
                        sell_price = grid_levels[current_level]
                        contracts = 1
                        margin = sell_price * contracts * margin_rate * trade_unit
                        if money < margin:
                            print(f"资金不足，无法开仓: {sell_price}, 当前资金: {money}, 需要保证金: {margin}")
                            break
                        hold_price = trade_map['price']
                        hold_contracts = trade_map['position']
                        trade_map['margin'] += margin
                        trade_map['position'] -= contracts
                        money -= margin
                        total_contracts = abs(hold_contracts) + contracts
                        if total_contracts > 0:
                            if abs(hold_contracts) == 0:
                                price_now = sell_price
                            else:
                                price_now = (hold_price * abs(hold_contracts) + sell_price * contracts) / total_contracts
                            trade_map['price'] = price_now
                        count += 1
                        print(f"卖出: {contracts} 合约, 卖出价格: {sell_price}, 当前资金: {money}, 当前持仓: {trade_map['position']}")
            elif current_price < pre_price:
                while current_level > 0 and row['low'] < grid_levels[current_level - 1]:
                    current_level -= 1
                    if trade_map['position'] < 0:
                        buy_price = grid_levels[current_level]
                        contracts = 1
                        profit = (trade_map['price'] - buy_price) * contracts * trade_unit
                        fee = buy_price * contracts * trade_unit * fee_pct
                        net_profit = profit - fee
                        release_margin = trade_map['price'] * contracts * trade_unit * margin_rate
                        money += net_profit + release_margin
                        
                        trade_map['margin'] -= release_margin
                        trade_map['position'] += contracts
                        count += 1
                        print(f"买入: {contracts} 合约, 买入价格: {buy_price}, 当前资金: {money}, 当前持仓: {trade_map['position']}, 利润: {profit}")
                    elif trade_map['position'] >= 0 and money > 0:
                        buy_price = grid_levels[current_level]
                        contracts = 1
                        margin = buy_price * contracts * margin_rate * trade_unit
                        if money < margin:
                            print(f"资金不足，无法开仓: {buy_price}, 当前资金: {money}, 需要保证金: {margin}")
                            break
                        
                        money -= margin
                        hold_price = trade_map['price']
                        hold_contracts = trade_map['position']
                        trade_map['margin'] += margin
                        trade_map['position'] += contracts
                        total_contracts = abs(hold_contracts + contracts)

                        if total_contracts > 0:
                            price_now = (hold_price * hold_contracts + buy_price * contracts) / total_contracts
                            trade_map['price'] = price_now
                        
                        print(f"买入: {contracts} 合约, 买入价格: {buy_price}, 当前资金: {money}, 当前持仓: {trade_map['position']}")
                        count += 1

            if current_price > upper_bound:
                hold_position = trade_map['position']
                if hold_position < 0:
                    buy_price = upper_bound
                    contracts = abs(hold_position)
                    margin = trade_map['margin']
                    hold_price = trade_map['price']
                    profit = (hold_price - buy_price) * contracts * trade_unit
                    fee = buy_price * contracts * trade_unit * fee_pct
                    net_profit = profit - fee
                    money += net_profit + margin
                    trade_map['margin'] = 0
                    trade_map['position'] = 0
                    trade_map['price'] = 0
                    count += 1
                    print(f"平仓: {contracts} 合约, 平仓价格: {buy_price}, 当前资金: {money}, 当前持仓: {trade_map['position']}")
                elif hold_position > 0:
                    sell_price = upper_bound
                    contracts = hold_position
                    margin = trade_map['margin']
                    hold_price = trade_map['price']
                    profit = (sell_price - hold_price) * contracts * trade_unit
                    fee = sell_price * contracts * trade_unit * fee_pct
                    net_profit = profit - fee

                    money += net_profit + margin
                    trade_map['margin'] = 0
                    trade_map['position'] = 0
                    trade_map['price'] = 0
                    count += 1
                    print(f"平仓: {contracts} 合约, 平仓价格: {sell_price}, 当前资金: {money}, 当前持仓: {trade_map['position']}")

                trade_map = {
                    'price': 0,
                    'position': 0,
                    'margin': 0
                }

                grid_levels = self.calculate_grid_levels(current_price, grid_size, grid_number_half)
                print(f"重新计算网格级别: {grid_levels}")
                lower_bound = grid_levels[0]
                upper_bound = grid_levels[-1]
                current_level = self.find_nearest_grid_level(current_price, grid_levels)

                # 重新开仓
                open_contracts = grid_number_half
                open_price = grid_levels[current_level]
                if money < open_price * open_contracts * margin_rate * trade_unit:
                    print(f"资金不足，无法开仓: {open_price}, 当前资金: {money}, 需要保证金: {open_price * open_contracts * margin_rate * trade_unit}")
                    continue
                margin = open_price * open_contracts * margin_rate * trade_unit
                money -= margin
                trade_map['price'] = open_price
                trade_map['position'] = open_contracts
                trade_map['margin'] = margin
                print(f"开仓: {open_contracts} 合约, 开仓价格: {open_price}, 当前资金: {money}, 当前持仓: {trade_map['position']}")
            elif current_price < lower_bound:
                # hold_position = trade_map['position']
                # if hold_position > 0:
                #     sell_price = lower_bound
                #     contracts = hold_position
                #     margin = trade_map['margin']
                #     hold_price = trade_map['price']
                #     profit = (sell_price - hold_price) * contracts * trade_unit
                #     money += profit + margin
                #     trade_map['margin'] = 0
                #     trade_map['position'] = 0
                #     trade_map['price'] = 0
                #     print(f"平仓: {contracts} 合约, 平仓价格: {sell_price}, 当前资金: {money}, 当前持仓: {trade_map['position']}")
                # breakpoint()
                


                grid_levels = self.calculate_grid_levels(current_price, grid_size, grid_number_half)
                print(f"重新计算网格级别: {grid_levels}")
                lower_bound = grid_levels[0]
                upper_bound = grid_levels[-1]
                current_level = self.find_nearest_grid_level(current_price, grid_levels)

                # # 重新开仓
                # open_contracts = grid_number_half
                # open_price = grid_levels[current_level]
                # margin = open_price * open_contracts * margin_rate * trade_unit
                # money -= margin
                # trade_map['price'] = open_price
                # trade_map['position'] = -open_contracts
                # trade_map['margin'] = margin
                # print(f"开仓: {open_contracts} 合约, 开仓价格: {open_price}, 当前资金: {money}, 当前持仓: {trade_map['position']}")


        if trade_map['position'] != 0:
            final_price = df.iloc[-1]['close']
            if trade_map['position'] > 0:
                profit = (final_price - trade_map['price']) * trade_map['position'] * trade_unit
                # money += profit + trade_map['margin']
            else:
                profit = (trade_map['price'] - final_price) * abs(trade_map['position']) * trade_unit
                # money += profit + trade_map['margin']

            fee = final_price * abs(trade_map['position']) * trade_unit * fee_pct
            net_profit = profit - fee
            money += net_profit + trade_map['margin']


        profit_rate = money / 100000 - 1
        print(f"最终资金: {money}, 收益率: {profit_rate:.2%}")
        open = df.iloc[0]['open']
        final_price = df.iloc[-1]['close']
        print(f"开盘价: {open}, 收盘价: {final_price}")

        market_rate = final_price / open - 1
        print(f"市场收益率: {market_rate:.2%}")

        sharpe_ratio = 0

        if timestamps and strategy_returns:
            strategy_df = pd.DataFrame({
                'timestamp': timestamps,
                'strategy_value': strategy_returns
            })
            strategy_df['date'] = pd.to_datetime(strategy_df['timestamp']).dt.date
            daily_strategy = strategy_df.groupby('date').agg({'strategy_value': 'last'}).reset_index()
            daily_returns = daily_strategy['strategy_value'].pct_change().dropna()
            
            if len(daily_returns) > 1 and daily_returns.std() != 0:
                # 假设年化天数为252天
                sharpe_ratio = (daily_returns.mean() / daily_returns.std()) * np.sqrt(252)

        return money, profit_rate, count, timestamps, strategy_returns, sharpe_ratio

    # def plot_comparison(self, df, timestamps, strategy_returns, grid_size, grid_numbers_half, profit_rate):
    #     """绘制市场价格曲线和策略收益曲线的对比图 - 按天汇总"""
        
    #     # 确保输出目录存在
    #     if not os.path.exists('charts'):
    #         os.makedirs('charts')
        
    #     # 创建DataFrame用于按天汇总
    #     strategy_df = pd.DataFrame({
    #         'timestamp': timestamps,
    #         'strategy_value': strategy_returns
    #     })
        
    #     # 添加日期列
    #     strategy_df['date'] = strategy_df['timestamp'].dt.date
    #     df_copy = df.copy()
    #     df_copy['date'] = df_copy['Open Time'].dt.date
        
    #     # 按天汇总策略数据 - 取每天最后一个值
    #     daily_strategy = strategy_df.groupby('date').agg({
    #         'strategy_value': 'last',
    #         'timestamp': 'last'
    #     }).reset_index()
        
    #     # 按天汇总市场数据 - 取每天的开盘价、最高价、最低价、收盘价
    #     daily_market = df_copy.groupby('date').agg({
    #         'open': 'first',   # 每天第一个开盘价
    #         'high': 'max',     # 每天最高价
    #         'low': 'min',      # 每天最低价
    #         'close': 'last',   # 每天最后收盘价
    #         'Open Time': 'last'  # 每天最后时间戳
    #     }).reset_index()
        
    #     # 计算市场每日收益
    #     initial_price = daily_market.iloc[0]['close']
    #     daily_market['market_value'] = [(price / initial_price - 1) * 100000 + 100000 for price in daily_market['close']]
        
    #     # 创建图表
    #     fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
    #     # 设置中文字体
    #     plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
    #     plt.rcParams['axes.unicode_minus'] = False
        
    #     # 第一个子图：市场价格曲线（按天）
    #     ax1.plot(daily_market['date'], daily_market['close'], label='每日收盘价', color='blue', linewidth=2, marker='o', markersize=3)
    #     ax1.fill_between(daily_market['date'], daily_market['low'], daily_market['high'], alpha=0.2, color='blue', label='每日价格区间')
    #     ax1.set_title(f'市场每日价格走势 (网格大小: {grid_size}, 网格数量: {grid_numbers_half})')
    #     ax1.set_ylabel('价格')
    #     ax1.legend()
    #     ax1.grid(True, alpha=0.3)
    #     ax1.tick_params(axis='x', rotation=45)
        
    #     # 第二个子图：策略收益曲线（按天）
    #     ax2.plot(daily_market['date'], daily_market['market_value'], label='市场每日收益', color='blue', linewidth=2, marker='o', markersize=3)
    #     ax2.plot(daily_strategy['date'], daily_strategy['strategy_value'], label='策略每日收益', color='red', linewidth=2, marker='s', markersize=3)
    #     ax2.set_title(f'每日收益对比 (策略收益率: {profit_rate:.2%})')
    #     ax2.set_xlabel('日期')
    #     ax2.set_ylabel('资金')
    #     ax2.legend()
    #     ax2.grid(True, alpha=0.3)
    #     ax2.tick_params(axis='x', rotation=45)
        
    #     # 调整布局
    #     plt.tight_layout()
        
    #     # 保存图片
    #     filename = f'charts/daily_grid_{grid_size}_half_{grid_numbers_half}.png'
    #     plt.savefig(filename, dpi=300, bbox_inches='tight')
    #     plt.close()
        
    #     print(f"每日汇总图表已保存: {filename}")
        
    #     # 打印每日汇总统计
    #     print(f"数据汇总周期: {daily_market['date'].min()} 到 {daily_market['date'].max()}")
    #     print(f"总交易天数: {len(daily_market)} 天")

    def plot_comparison(self, df, timestamps, strategy_returns, grid_size, grid_numbers_half, profit_rate, year):
        """绘制市场价格曲线和策略收益曲线的对比图 - 按天汇总"""
        
        # 确保输出目录存在，为每年创建单独文件夹
        year_folder = f'charts/{year}'
        if not os.path.exists(year_folder):
            os.makedirs(year_folder)
        
        # 创建DataFrame用于按天汇总
        strategy_df = pd.DataFrame({
            'timestamp': timestamps,
            'strategy_value': strategy_returns
        })
        
        # 添加日期列
        strategy_df['date'] = strategy_df['timestamp'].dt.date
        df_copy = df.copy()
        df_copy['date'] = df_copy['datetime'].dt.date
        
        # 按天汇总策略数据 - 取每天最后一个值
        daily_strategy = strategy_df.groupby('date').agg({
            'strategy_value': 'last',
            'timestamp': 'last'
        }).reset_index()
        
        # 按天汇总市场数据 - 取每天的开盘价、最高价、最低价、收盘价
        daily_market = df_copy.groupby('date').agg({
            'open': 'first',   # 每天第一个开盘价
            'high': 'max',     # 每天最高价
            'low': 'min',      # 每天最低价
            'close': 'last',   # 每天最后收盘价
            'datetime': 'last'  # 每天最后时间戳
        }).reset_index()
        
        # 计算市场每日收益
        initial_price = daily_market.iloc[0]['close']
        daily_market['market_value'] = [(price / initial_price - 1) * 100000 + 100000 for price in daily_market['close']]
        
        # 创建图表
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 第一个子图：市场价格曲线（按天）
        ax1.plot(daily_market['date'], daily_market['close'], label='每日收盘价', color='blue', linewidth=2, marker='o', markersize=3)
        ax1.fill_between(daily_market['date'], daily_market['low'], daily_market['high'], alpha=0.2, color='blue', label='每日价格区间')
        ax1.set_title(f'{year}年7-8月市场每日价格走势 (网格大小: {grid_size}, 网格数量: {grid_numbers_half})')
        ax1.set_ylabel('价格')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)
        
        # 第二个子图：策略收益曲线（按天）
        ax2.plot(daily_market['date'], daily_market['market_value'], label='市场每日收益', color='blue', linewidth=2, marker='o', markersize=3)
        ax2.plot(daily_strategy['date'], daily_strategy['strategy_value'], label='策略每日收益', color='red', linewidth=2, marker='s', markersize=3)
        ax2.set_title(f'{year}年7-8月每日收益对比 (策略收益率: {profit_rate:.2%})')
        ax2.set_xlabel('日期')
        ax2.set_ylabel('资金')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.tick_params(axis='x', rotation=45)
        
        # 调整布局
        plt.tight_layout()
        
        # 保存图片到对应年份的文件夹
        filename = f'{year_folder}/daily_grid_{grid_size}_half_{grid_numbers_half}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"{year}年每日汇总图表已保存: {filename}")

if __name__ == "__main__":
    gt = GridTrade()
    path = 'jd_futures_1m_data(1).csv'

    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    print(df.columns)

    # df['Open Time'] = pd.to_datetime(df['time'], unit='ms')  + pd.Timedelta(hours=8)
    # print(df['Open Time'])
    df['datetime'] = pd.to_datetime(df['datetime'])

    df['year'] = df['datetime'].dt.year
    df['month'] = df['datetime'].dt.month

    july_august_data = df[(df['month'].isin([7, 8]))]

    if july_august_data.empty:
        raise ValueError("DataFrame is empty after filtering for July and August.")
    
    years = sorted(july_august_data['year'].unique())
    print(f"找到的年份: {years}")

    # start_time = '2022-07-01 00:00:00'
    # end_time = '2022-08-31 23:59:00'

    # df = df[(df['Open Time'] >= start_time) & (df['Open Time'] <= end_time)]

    if df.empty:
        raise ValueError("DataFrame is empty after filtering by date range.")

    # grid_sizes = [0.005, 0.01, 0.015, 0.02, 0.025, 0.03]
    # grid_numbers_half_list = [3, 4, 5, 7, 10]
    # grid_sizes = [0.1]
    # grid_numbers_half_list = [10]
    fee_pct = 0.00015
    all_results = []
    best_results_per_year = []

    for year in years:
        print(f"\n{'='*50}")
        print(f"处理 {year} 年 7-8月份数据")
        print(f"{'='*50}")
        grid_sizes = [0.005, 0.01, 0.015, 0.02]
        grid_numbers_half_list = [2, 3, 4, 5]
        # if year != 2015:  # TODO: 只处理2015年数据
        #     continue
        
        # 筛选当年7-8月份数据
        year_data = july_august_data[july_august_data['year'] == year].copy()
        year_data = year_data.sort_values('datetime')
        
        if year_data.empty:
            print(f"{year}年没有7-8月份数据，跳过")
            continue
        
        print(f"{year}年数据范围: {year_data['datetime'].min()} 到 {year_data['datetime'].max()}")
        print(f"数据条数: {len(year_data)}")
        print(f"合约代码: {year_data['contract_code'].unique()}")
        
        year_results = []

        for grid_size in grid_sizes:
            for grid_numbers_half in grid_numbers_half_list:
                print(f"\n计算参数: 网格大小={grid_size}, 网格数量={grid_numbers_half}")
                
                try:
                    money, profit_rate, count, timestamps, strategy_returns, sharpe_ratio = gt.calc_dgt(
                        year_data, grid_size, grid_numbers_half, fee_pct
                    )
                    
                    result = {
                        'year': year,
                        'grid_size': grid_size,
                        'grid_numbers_half': grid_numbers_half,
                        'final_money': money,
                        'profit_rate': profit_rate,
                        'sharpe_ratio': sharpe_ratio,
                        'trade_count': count,
                        'start_date': year_data['datetime'].min(),
                        'end_date': year_data['datetime'].max(),
                        'contracts': ', '.join(year_data['contract_code'].unique())
                    }
                    
                    year_results.append(result)
                    all_results.append(result)
                    
                    # 绘制图表
                    gt.plot_comparison(year_data, timestamps, strategy_returns, 
                                     grid_size, grid_numbers_half, profit_rate, year)
                    
                except Exception as e:
                    print(f"计算出错: {e}")
                    continue
        
        # 保存当年结果
        if year_results:
            year_df = pd.DataFrame(year_results)
            year_df.to_csv(f'{year}_grid_trade_results.csv', index=False)
            print(f"\n{year}年结果已保存到 {year}_grid_trade_results.csv")
            
            # 显示当年最佳参数
            best_result = year_df.loc[year_df['profit_rate'].idxmax()]
            print(f"{year}年最佳参数:")
            print(f"  网格大小: {best_result['grid_size']}")
            print(f"  网格数量: {best_result['grid_numbers_half']}")
            print(f"  收益率: {best_result['profit_rate']:.2%}")
            print(f"  交易次数: {best_result['trade_count']}")
            print(f"  最终资金: {best_result['final_money']}")
            best_results_per_year.append(best_result)


    # 保存所有年份的汇总结果
    if all_results:
        summary_df = pd.DataFrame(all_results)
        summary_df.to_csv('all_years_grid_trade_results.csv', index=False)
        print(f"\n所有年份汇总结果已保存到 all_years_grid_trade_results.csv")
        
        # 按年份汇总统计
        yearly_summary = summary_df.groupby('year').agg({
            'profit_rate': ['mean', 'max', 'min'],
            'sharpe_ratio': ['mean', 'max', 'min'],
            'trade_count': 'mean',
            'final_money': 'mean'
        }).round(4)
        
        print("\n各年份收益率统计:")
        print(yearly_summary)

    if best_results_per_year:
        best_df = pd.DataFrame(best_results_per_year)
        best_df.to_csv('best_grid_trade_results_per_year.csv', index=False)
        print(f"\n每年最佳参数已保存到 best_grid_trade_results_per_year.csv")
        
        print("\n每年最佳参数:")
        for index, row in best_df.iterrows():
            print(f"{row['year']}年: 网格大小={row['grid_size']}, 网格数量={row['grid_numbers_half']}, 收益率={row['profit_rate']:.2%}, 最终资金={row['final_money']:.2f}")
    else:
        print("没有成功计算出任何结果")

    # for grid_size in grid_sizes:
    #     for grid_numbers_half in grid_numbers_half_list:
    #         print(f"Calculating for grid size: {grid_size}, grid numbers half: {grid_numbers_half}")

    #         money, profit_rate, count, timestamps, strategy_returns = gt.calc_dgt(df, grid_size, grid_numbers_half, fee_pct)
    #         result.append({
    #             'grid_size': grid_size,
    #             'grid_numbers_half': grid_numbers_half,
    #             'final_money': money,
    #             'profit_rate': profit_rate,
    #             'trade_count': count
    #         })
    #         gt.plot_comparison(df, timestamps, strategy_returns, grid_size, grid_numbers_half, profit_rate)
    
    # result_df = pd.DataFrame(result)
    # result_df.to_csv('0624_grid_trade_results.csv', index=False)


















