import pandas as pd
from xtquant import xtdatacenter as xtdc
from xtquant import xtdata

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