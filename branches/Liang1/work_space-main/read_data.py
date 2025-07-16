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
    for code in codes:
        xtdata.subscribe_quote(code, period, start_time, end_time, count, callback=None)
        xtdata.download_history_data(code, period, start_time, end_time)
    market_data = xtdata.get_market_data_ex([], codes, period, start_time, end_time, count=count, 
                                          dividend_type='none', fill_data=False)
    for code in codes:
        if market_data[code].empty:
            print(f"{code} 数据获取失败！")
            break
    
    # 如果是获取交易日数据，则过滤掉最后一天21:00之后的数据。输入的time为具体某分钟时，不用处理
    if market_data and len(start_time) == 8 and len(end_time) == 8:
        
        for code in codes:
            if not market_data[code].empty:
                df = market_data[code].copy()
                
                # 将索引转换为datetime（如果还不是的话）
                if not isinstance(df.index, pd.DatetimeIndex):
                    df.index = pd.to_datetime(df.index)

                # 获取当前数据的最后一天
                end_date = df.index[-1].date()
                
                # 创建过滤条件：排除最后一天21:00之后的数据
                mask = ~((df.index.date == end_date) & (df.index.hour >= 21))
                market_data[code] = df[mask]
    
    return market_data

'''当输入为日期时，我剔除了最后一个交易日夜盘的数据，但没有加入上个交易日夜盘的数据'''
def get_single_market_data(code: str, period: str, start_time: str, end_time: str, count: int) -> pd.DataFrame:
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

    df = market_data[code].copy()

    #当输入的time为具体某分钟时，不用处理
    if not df.empty and len(start_time) == 8 and len(end_time) == 8:
        # 将索引转换为datetime（如果还不是的话）
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index)
        
        # 获取当前数据的最后一天
        end_date = df.index[-1].date()
        
        # 创建过滤条件：排除最后一天21:00之后的数据
        mask = ~((df.index.date == end_date) & (df.index.hour >= 21))
        df = df[mask]

    return df

def get_main_contract_code(continuous_contract_code: str, start_time: str, end_time: str)-> str:
    if not continuous_contract_code or '.' not in continuous_contract_code:
        print("错误: 请输入正确的连续合约代码")
    
    parts = continuous_contract_code.split('.')
    exchange_code = parts[-1] if len(parts) > 1 else ''
    
    start_time_dt = datetime.strptime(start_time, '%Y%m%d')
    dt = start_time_dt - timedelta(days=360)
    dt_str = dt.strftime('%Y%m%d')
    main_df = get_single_market_data(continuous_contract_code, 'historymaincontract', start_time=dt_str, end_time=end_time, count=-1)[['time','合约在交易所的代码']]

    main_df.columns = ['time','code']        
    main_df['time'] = pd.to_datetime(main_df['time'], unit='ms')
    main_df["time"] = main_df["time"] + pd.Timedelta(hours=8)#转为北京时区
    main_df["time"] = main_df['time'].dt.strftime('%Y%m%d')#将Y-m-d变为Ymd
    main_df = main_df.drop_duplicates(subset=['code'], keep='first')

    main_contract = main_df[main_df['time']< start_time].iloc[-1,1]  # 获取开始时间之前的最后一个主力合约代码
    if "." not in main_contract:
        main_contract = main_contract + '.' + exchange_code  # 添加交易所代码后缀
    main_df = main_df[main_df['time']> start_time]  # 过滤出主力合约的记录
    return main_contract, main_df['code'].tolist()
