from xtquant import xtdatacenter as xtdc
from xtquant import xtdata
import pandas as pd
from datetime import datetime, timedelta
import time
import tkinter as tk
from tkinter import messagebox
import asyncio
import concurrent.futures
xtdc.set_token('4065054877ce5724155dbc5bcba200381ce5eb35')
xtdc.init()

def show_message(title, message):
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    messagebox.showinfo(title, message)
    root.destroy()


def get_market_data(codes: list, period: str, start_time: str, end_time: str, count: int) -> dict:
    for code in codes:
        xtdata.subscribe_quote(code, period, start_time, end_time, count, callback=None)
        xtdata.download_history_data(code, period, start_time, end_time)

    market_data = xtdata.get_market_data_ex([], codes, period, start_time, end_time, count=count, dividend_type='none',
                                            fill_data=False)

    for code in codes:
        if market_data[code].empty:
            print(f"数据 {code} 获取失败！")
            break

    # market_data['time'] = pd.to_datetime(market_data['time'], unit='ms')
    # market_data["time"] = market_data["time"] + pd.Timedelta(hours=8)#转为北京时区
    # market_data["time"] = market_data['time'].dt.strftime('%Y%m%d')#将Y-m-d变为Ymd

    return market_data

async def get_tick_data_async(codes: list, start_time: str, end_time: str, count: int) -> dict:
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = await loop.run_in_executor(
            executor, 
            get_market_data, 
            codes, 'tick', start_time, end_time, count
        )
    return result


if __name__ == "__main__":
    contract_price = 70.5
    contract_deal = ['ag2508.SF']  
    option_codes = ['ag2508P7800.SF']
    n = 0.08
    alarm_price = 8400

    with open('./data/code.txt', 'r') as f:
        codes = f.read().splitlines()

    main_contract = []
    for code in codes:
        data = xtdata.get_main_contract(code)
        if data:
            main_contract.append(data)
        else:
            print(f"No main contract found for {code}")

    today = datetime.now().date().strftime('%Y%m%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    dict_data = get_market_data(contract_deal, '1d', '20250407', today, 20)

    dict_history = {}

    for contract in contract_deal:
        close_min = dict_data[contract]['close'].min()
        close_max = dict_data[contract]['close'].max()
        dict_history[contract] = {'close_min': close_min, 'close_max': close_max}
    
    columns = ['signal', 'pos', 'neg', 'strike', 'min', 'max', 'price']
    df_results = pd.DataFrame(index=contract_deal, columns=columns)
    df_results['pos'] = 0
    df_results['neg'] = 0
    while True:
        option_now_data = xtdata.get_full_tick(option_codes)
        option_now_price = option_now_data[option_codes[0]]['lastPrice']
        print(f"期权当前价格: {option_now_price}")
        gain = contract_price - option_now_price
        print("每单位盈亏", gain) 
        percentage_gain = (contract_price - option_now_price) / contract_price * 100
        print(f"盈亏百分比: {percentage_gain:.2f}%")
        if percentage_gain < -5:
            # show_message("警告", "期权价格下跌超过5%，请注意！")
            print("期权价格下跌超过5%，请注意！")
        current_time = datetime.now().time()
        morning_start = datetime.strptime('09:00:00', '%H:%M:%S').time()
        morning_end = datetime.strptime('11:30:00', '%H:%M:%S').time()
        afternoon_start = datetime.strptime('13:30:00', '%H:%M:%S').time()
        afternoon_end = datetime.strptime('15:00:00', '%H:%M:%S').time()
        night_start = datetime.strptime('21:00:00', '%H:%M:%S').time()
        night_end = datetime.strptime('23:00:00', '%H:%M:%S').time()
        print(f"当前时间: {current_time}")
        if current_time > afternoon_start and current_time < afternoon_end:
            minutes_open = (datetime.combine(datetime.today(), current_time) 
                            - datetime.combine(datetime.today(), afternoon_start)).seconds // 60 
            print(f"已经是下午时间: {current_time}，已开市{minutes_open}分钟")
            print("------------------------------------------------")
        elif current_time > datetime.strptime('09:00:00', '%H:%M:%S').time() \
                and current_time < datetime.strptime('11:30:00', '%H:%M:%S').time():
            minutes_open = (datetime.combine(datetime.today(), current_time) 
                            - datetime.combine(datetime.today(), morning_start)).seconds // 60
            print(f"已经是上午时间: {current_time}，已开市{minutes_open}分钟")
            print("------------------------------------------------")
        elif current_time > night_start and current_time < night_end:
            minutes_open = (datetime.combine(datetime.today(), current_time) 
                            - datetime.combine(datetime.today(), night_start)).seconds // 60
            print(f"已经是夜盘时间: {current_time}，已开市{minutes_open}分钟")
            print("------------------------------------------------")
        if current_time >= datetime.strptime('23:00:00', '%H:%M:%S').time():
            print("交易日结束")
            break

        df = get_market_data(contract_deal, 'tick', today, today, 1)

        

        for contract in contract_deal:
            close_min = dict_history[contract]['close_min']
            close_max = dict_history[contract]['close_max']
            close_now = df[contract]['lastPrice'].iloc[-1]

            df_results.at[contract, 'min'] = close_min
            df_results.at[contract, 'max'] = close_max
            df_results.at[contract, 'price'] = close_now


            count_pos = df_results.at[contract, 'pos']
            count_neg = df_results.at[contract, 'neg']


            if close_now < alarm_price:
                print(f"////////////////价格 {close_now} 低于警戒线 {alarm_price}，请注意！////////////////")

            if close_now > close_max :
                count_pos += 1
                df_results.at[contract, 'pos'] = count_pos
            elif close_now < close_min:
                count_neg += 1
                df_results.at[contract, 'neg'] = count_neg

            if count_pos >= 30 and df_results.at[contract, 'signal'] != 1:
                df_results.at[contract, 'signal'] = 1
                df_results.at[contract, 'strike'] = close_now * (1 - n)
                print(f"Sell Put信号: {contract} at price {df_results.at[contract, 'strike']}，现在价格: {close_now}， 最高价: {close_max}")
            elif count_neg >= 30 and df_results.at[contract, 'signal'] != -1:
                df_results.at[contract, 'signal'] = -1
                df_results.at[contract, 'strike'] = close_now * (1 + n)
                print(f"Sell Call信号: {contract} at price {df_results.at[contract, 'strike']}，现在价格: {close_now}， 最低价: {close_min}")
        df_sorted = df_results.sort_values(by=['signal', 'strike', 'pos', 'neg'], 
                                        ascending=[False, False, False, False])
        print(df_sorted)
        time.sleep(1) 