from read_data import get_market_data
from datetime import datetime, timedelta
import pandas as pd
from xtquant import xtdatacenter as xtdc
from xtquant import xtdata

#calendar要求：list，元素为datetime.date类型
def get_trading_date(dt,calendar:list):
    if isinstance(dt, str):
        dt = pd.to_datetime(dt)

    hour = dt.hour
    
    # 夜盘时间：21:00 到次日 02:30
    if hour >= 21 or hour <= 2:
        # 如果是21:00之后，交易日为第二天
        if hour >= 21:
            idx = calendar.index(dt.date()) + 1
            if idx < len(calendar):
                trading_date = calendar[idx]
            else:
                print("日期超出交易日历范围")
        else:
            # 如果是00:00-02:30，交易日就是当天
            trading_date = dt.date()
    else:
        # 日盘时间：09:00-15:00，交易日就是当天
        trading_date = dt.date()
    
    return trading_date.strftime('%Y%m%d')

def cook_data(raw_data: pd.DataFrame) -> pd.DataFrame:
    # 获取数据
    df = raw_data.copy()

    # 修复：始终将索引数据作为'date'列
    #print("\n将索引数据转换为'date'列")
    df = df.reset_index()

    # 如果索引有名称，重命名为'date'
    if df.columns[0] != 'date':
        df = df.rename(columns={df.columns[0]: 'date'})

    # 将date列转换为字符串格式
    if 'date' in df.columns:
        # 根据数据类型进行适当的转换
        if pd.api.types.is_datetime64_any_dtype(df['date']):
            # 如果是datetime类型，格式化为YYYYMMDDHHMM
            df['date'] = df['date'].dt.strftime('%Y%m%d%H%M%S')
        else:
            # 如果不是datetime类型，直接转为字符串
            df['date'] = df['date'].astype(str)

    # 删除任何可能的空值行
    data = df.dropna().reset_index(drop=True)

    data.columns = data.columns.str.strip()
    data = data.dropna(subset=['date', 'time']).copy()

    # 获取交易日历
    

    if 'date' in data.columns and 'time' in data.columns:
        data['date'] = pd.to_datetime(data['date'], format='%Y%m%d%H%M%S', errors='coerce')
        data['time'] = pd.to_numeric(data['time'], errors='coerce').astype('Int64')
    
    calendar = data['date'].dt.date.unique().tolist()

    if 'date' in data.columns and 'time' in data.columns:
        data['trading_date'] = data['date'].apply(lambda dt: get_trading_date(dt, calendar))
        data['date_str'] = data['trading_date']  
        
    price_columns = ['open', 'high', 'low', 'close']
    for col in price_columns:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors='coerce')
    
    
    print(f"数据解析完成: {len(data)} 条有效数据")
    return data
    
