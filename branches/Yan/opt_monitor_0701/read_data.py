import pandas as pd
from xtquant import xtdatacenter as xtdc
from xtquant import xtdata
from datetime import datetime, timedelta



def read_history_file(file_path: str) -> pd.DataFrame:
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.pkl'):
        return pd.read_pickle(file_path)
    else:
        raise ValueError("Unsupported file format. Please use .csv or .pkl files.")
    
def get_market_data(codes: list, period: str, start_time: str, end_time: str, count: int) -> dict:
    """获取市场数据"""
    # if len(codes) == 1:
    #     xtdata.subscribe_quote(codes[0], period, start_time, end_time, count, callback=None)
    #     xtdata.download_history_data(codes[0], period, start_time, end_time)
    #     market_data = xtdata.get_market_data_ex([], codes, period, start_time, end_time, count=count, 
    #                                           dividend_type='none', fill_data=False)
    #     if market_data[codes[0]].empty:
    #         print(f"{codes[0]} 数据获取失败！")
    #         return {}
    #     return market_data
    # else:
    for code in codes:
        xtdata.subscribe_quote(code, period, start_time, end_time, count, callback=None)
        xtdata.download_history_data(code, period, start_time, end_time)
    market_data = xtdata.get_market_data_ex([], codes, period, start_time, end_time, count=count, 
                                          dividend_type='none', fill_data=False)
    for code in codes:
        if market_data[code].empty:
            print(f"{code} 数据获取失败！")
            break
    return market_data

def get_singel_market_data(code: str, period: str, start_time: str, end_time: str, count: int) -> pd.DataFrame:
    """获取单个市场数据"""
    market_data = xtdata.get_market_data_ex([], [code], period, start_time, end_time, count=count, 
                                          dividend_type='none', fill_data=False)
    if len(market_data[code]) == 0:
        xtdata.subscribe_quote(code, period, start_time, end_time, count, callback=None)
        xtdata.download_history_data(code, period, start_time, end_time)
        market_data = xtdata.get_market_data_ex([], [code], period, start_time, end_time, count=count, 
                                          dividend_type='none', fill_data=False)
    if market_data[code].empty:
        print(f"{code} 数据获取失败！")
        return pd.DataFrame()
    return market_data[code]

def get_main_contract_code(continuous_contract_code: str, start_time: str, end_time: str)-> str:
    if not continuous_contract_code or '.' not in continuous_contract_code:
        print("错误: 请输入正确的连续合约代码")
    
    parts = continuous_contract_code.split('.')
    exchange_code = parts[-1] if len(parts) > 1 else ''
    
    start_time_dt = datetime.strptime(start_time, '%Y%m%d')
    dt = start_time_dt - timedelta(days=30)
    dt_str = dt.strftime('%Y%m%d')
    print(dt_str)
    main_df = get_singel_market_data(continuous_contract_code, 'historymaincontract', start_time=dt_str, end_time=end_time, count=-1)[['time','合约在交易所的代码']]

    main_df.columns = ['time','code']        
    main_df['time'] = pd.to_datetime(main_df['time'], unit='ms')
    main_df["time"] = main_df["time"] + pd.Timedelta(hours=8)#转为北京时区
    main_df["time"] = main_df['time'].dt.strftime('%Y%m%d')#将Y-m-d变为Ymd

    main_contract = main_df[main_df['time']< start_time].iloc[-1,1]  # 获取开始时间之前的最后一个主力合约代码
    main_contract = main_contract + '.' + exchange_code  # 添加交易所代码后缀
    return main_contract