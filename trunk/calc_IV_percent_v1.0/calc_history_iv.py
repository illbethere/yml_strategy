from calc_HV_IV import calc_iv
from xtquant import xtdatacenter as xtdc
from xtquant import xtdata
import pandas as pd
from datetime import datetime
import tushare as ts
import os
import numpy as np


def load_trade_calendar():
    with open("trade_cal.txt", "r", encoding='utf-8') as f:
        df = pd.read_csv(f, encoding='utf-8-sig')
        df['cal_date'] = pd.to_datetime(df['cal_date'], format='%Y%m%d')
        df = df[df['is_open'] == 1]
        trade_dates = df['cal_date'].dt.strftime('%Y%m%d').tolist()
    return sorted(trade_dates)

def get_last_trade_date(target_date: str):
    trade_dates = load_trade_calendar()
    target_date_str = pd.to_datetime(target_date).strftime('%Y%m%d')

    for i, date in enumerate(trade_dates):
        if date >= target_date_str and i > 0:
            return trade_dates[i - 1]
    return trade_dates[-1] if trade_dates else None

def load_history_iv_csv(code):
    csv_file = f"iv_rsult/{code}_history_iv.csv"
    if os.path.exists(csv_file):
        # last_date = df['date'].iloc[-1]
        # if isinstance(last_date, str) and len(last_date) == 8:

        df = pd.read_csv(csv_file)
        df['date'] = df['date'].astype(str)
        # df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y%m%d')
        print(f"历史IV数据已加载: {csv_file}")
        return df
    else:
        return pd.DataFrame(columns=['date', 'main_contract', 'put_option', 'call_option', 'put_iv', 'call_iv', 'avg_iv'])


def save_history_iv_csv(code, df):
    csv_file = f"iv_rsult/{code}_history_iv.csv"
    if not os.path.exists('iv_rsult'):
        os.makedirs('iv_rsult')
    df.to_csv(csv_file, index=False)
    print(f"历史IV数据已保存到: {csv_file}")




def get_history_main_contract(codes: list):
    period = "historymaincontract"
    if isinstance(codes, str):
        codes = [codes]
    data = xtdata.get_market_data_ex([], codes, period)

    return data

def get_main_contract_by_date(date: str, data_df: pd.DataFrame):

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
    # switch_date = lastest_record['datetime']

    return main_contract

def get_close_price(future_contract: str, date: str):
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
        
def get_put_option_list(future_code: str, date: str):
    xtdata.download_history_contracts()
    option_list = xtdata.get_option_list(future_code, date, 'PUT', isavailavle= False)
    return option_list  

def get_call_option_list(future_code: str, date: str):
    xtdata.download_history_contracts()
    option_list = xtdata.get_option_list(future_code, date, 'CALL', isavailavle= False)
    return option_list

def get_flat_option(future_code: str, date: str):


    close_price = get_close_price(future_code, date)
    if close_price is None:
        print(f"未找到{future_code}的收盘价")
        return None
    
    put_option_list = get_put_option_list(future_code, date)
    call_option_list = get_call_option_list(future_code, date)

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
            if 'P' in option_code:
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
            if 'C' in option_code:
                strike = float(option_code.split('C')[-1])
                if strike not in strike_price:
                    strike_price.append(strike)
                call_dict[strike] = option

        except Exception as e:
            print(f"解析CALL期权失败: {option}, 错误: {e}")
            continue

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


def calc_option_iv(future_code: str, date: str):

    result = get_flat_option(future_code, date)
    put_option = result['put']
    call_option = result['call']

    if put_option is None or call_option is None:
        print(f"未找到平值期权: {future_code}, {date}")
        return None
    
    if isinstance(date, str):
        if '-' in date:
            date = date.replace('-', '')
    else:
        print(f"日期格式错误: {date}")

    
    put_iv_dict = calc_iv(put_option, date)
    call_iv_dict = calc_iv(call_option, date)
    put_iv = put_iv_dict[put_option]['iv']
    call_iv = call_iv_dict[call_option]['iv']

    print(f"平值期权IV: {put_option, call_option}, {date}, PUT: {put_iv}, CALL: {call_iv}")

    avg_iv = (put_iv + call_iv) / 2
    # print(f"平均IV: {future_code}, {date}, IV: {avg_iv}")
    return avg_iv

    

def calc_miss_iv_data(code, start_date, end_date):
    trade_dates = load_trade_calendar()

    target_dates = [d for d in trade_dates if start_date <= d <= end_date]

    main_contract_data = get_history_main_contract(code)
    temp_data = main_contract_data[code]
    temp_data.columns = temp_data.columns.str.strip()
    if 'time' in temp_data.columns:
        temp_data['datetime'] = pd.to_datetime(temp_data['time'], unit='ms')

    new_records = []

    for date in target_dates:
        try:
            print(f"处理日期: {date}")
            query_date = pd.to_datetime(date).strftime('%Y-%m-%d')
            main_contract = get_main_contract_by_date(query_date, temp_data)

            if main_contract is None:
                print(f"未找到主力合约: {date}")
                continue
            
            iv_result = calc_option_iv(main_contract, date)

            if iv_result:
                option_info = get_flat_option(main_contract, date)
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

def calc_today_percent(code, today = None):
    if today is None:
        today = datetime.now().strftime('%Y%m%d')
    elif isinstance(today, str):
        today = pd.to_datetime(today).strftime('%Y%m%d')

    history_df = load_history_iv_csv(code)

    last_trade_date = get_last_trade_date(today)

    if history_df.empty:
        print(f"未找到历史IV数据: {code}")
        start_date = '20240101'
        end_date = last_trade_date
        new_data = calc_miss_iv_data(code, start_date, end_date)
        history_df = new_data
        save_history_iv_csv(code, history_df)
    else:
        # last_record_date = pd.to_datetime(history_df['date'].iloc[-1]).strftime('%Y%m%d')
        last_record_date = history_df['date'].iloc[-1]
        print(f"最后记录日期: {last_record_date}, 当前日期: {today}")
        if last_record_date < last_trade_date:
            print(f"需要补齐数据: {code}, {last_record_date} 到 {last_trade_date}")
            trade_dates = load_trade_calendar()
            try:
                start_idx = trade_dates.index(last_record_date) + 1 if last_record_date in trade_dates else 0
                end_idx = trade_dates.index(last_trade_date) + 1 if last_trade_date in trade_dates else len(trade_dates)
            except ValueError:
                print(f"未找到最后记录日期 {last_record_date} 在交易日历中")

            if start_idx < end_idx:
                missing_start = trade_dates[start_idx]
                missing_end = last_trade_date
                new_data = calc_miss_iv_data(code, missing_start, missing_end)

                if not new_data.empty:
                    new_data['date'] = new_data['date'].astype(str)
                    history_df = pd.concat([history_df, new_data], ignore_index=True)
                    history_df = history_df.drop_duplicates(subset=['date']).sort_values('date')
                    save_history_iv_csv(code, history_df)
            else:
                print(f"没有需要补齐的数据: {code}, {last_record_date} 到 {last_trade_date}")
        else:
            print(f"已有最新数据: {code}, {last_record_date} 到 {last_trade_date}")
    

    
    print(f"计算今日{code}的IV百分位排名")

    main_contract_data = get_history_main_contract([code])
    temp_data = main_contract_data[code]
    temp_data.columns = temp_data.columns.str.strip()
    if 'time' in temp_data.columns:
        temp_data['datetime'] = pd.to_datetime(temp_data['time'], unit='ms')

    query_date = pd.to_datetime(today).strftime('%Y-%m-%d')
    main_contract = get_main_contract_by_date(query_date, temp_data)

    if not main_contract:
        print(f"未找到主力合约: {query_date}")
        return None
    
    today_iv = calc_option_iv(main_contract, today)
    if today_iv is None:
        print(f"未计算出今日IV: {main_contract}, {today}")
        return None
    

    if not history_df.empty:
        history_iv_values = history_df['avg_iv'].dropna().values
        if len(history_iv_values) > 0:
            percent = (np.sum(history_iv_values <= today_iv) / len(history_iv_values)) * 100
            print(f"今日IV: {today_iv}, 百分位排名: {percent:.2f}%")

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
















if __name__ == "__main__":
    # ts.set_token('810b8b575d9401768bb81320214e958f541a34cc958603e65049f2ce')
    # pro = ts.pro_api()
    # df = pro.trade_cal(exchange='DCE', start_date='20240101', end_date='20251231')
    # with open("trade_cal.txt", "w", encoding='utf-8') as f:
    #     df.to_csv(f, index=False, encoding='utf-8-sig', lineterminator='\n')

    # with open("trade_cal.txt", "r", encoding='utf-8') as f:
    #     df = pd.read_csv(f, encoding='utf-8-sig')
    #     df['cal_date'] = pd.to_datetime(df['cal_date'], format='%Y%m%d')
    #     df = df[df['is_open'] == 1]
    #     trade_dates = df['cal_date'].dt.strftime('%Y%m%d').tolist()
    #     print("交易日历:", trade_dates)


    start_time = datetime.now()
    # with open("code.txt", "r") as f:
    #     codes = f.read().splitlines()
    #     # print("读取代码:", codes)
    # print("读取代码:", codes)

    codes = ['ag00.SF', 'al00.SF']
    
    date = "20250626"
    results = []

    for code in codes:
        result = calc_today_percent(code, date)
        if result:
            results.append(result)
        

    # data = get_history_main_contract(codes)
    # # print(data[codes[0]])
    # # with open("test.csv", "w", encoding='utf-8-sig') as f:
    # #     data[codes[0]].to_csv(f, index=False, encoding = 'utf-8', lineterminator='\n')

    # # with open("test.csv", "r", encoding='utf-8') as f:
    # #     data = f.read().splitlines()
    # # data = pd.read_csv("test.csv", encoding='utf-8-sig')
    # for code in codes:
    #     temp_data = data[code]
    #     # print(data)
    #     temp_data.columns = temp_data.columns.str.strip() 
    #     if 'time' in temp_data.columns:
    #         temp_data['datetime'] = pd.to_datetime(temp_data['time'], unit='ms')
    #         # print("转换后的时间:")
    #         # print(temp_data)
    #     else:
    #         print("未找到time列")

    #     main_contract = get_main_contract_by_date(date, temp_data)
    #     print("主力合约:", main_contract)

    #     avg_iv = calc_option_iv(main_contract, date)
    #     print(f"{main_contract}平均IV: {avg_iv}%")
    

    end_time = datetime.now()


    print(f"总耗时: {end_time - start_time}")


