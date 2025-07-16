import tushare as ts
from datetime import datetime, timedelta
from read_data import *

ts.set_token('810b8b575d9401768bb81320214e958f541a34cc958603e65049f2ce')
pro = ts.pro_api()

interest_rate = 0.02
ag_storage_cost = 0.001 # 白银1元/kg
au_storage_cost = 0.045 # 黄金0.5元/kg
ag_pre_lot = 15 # 1手15kg
au_pre_lot = 1 # 1手1kg
today = datetime.now().strftime('%Y%m%d')
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
spot_future = ['Ag(T+d)', 'Au(T+d)']
spot_dict = {}
result_dict = {}
today_datetime = datetime.strptime(today, '%Y%m%d')


for code in spot_future:
    print(code)
    df = pro.sge_daily(ts_code=code, start_date=yesterday, end_date=today, fields='ts_code,trade_date,open,high,low,close')
    close = df['close'].iloc[-1]
    if 'Ag' in code:
        spot_dict[code] = close * 1000
        close = close * 1000
    else:
        spot_dict[code] = close 
    print(f"现货{code}的最新收盘价: {close}")
    if 'Ag' in code:
        future_code = 'ag2508.SF'
        detail_data = xtdata.get_instrument_detail(future_code)
    else:
        future_code = 'au2508.SF'
        detail_data = xtdata.get_instrument_detail(future_code)
    expire_date = detail_data['ExpireDate']
    expire_date = datetime.strptime(expire_date, '%Y%m%d')

    # today = datetime.strptime(today, '%Y%m%d')
    until_expire_dates = (expire_date - today_datetime).days

    if 'Ag' in code:
        theoretical_price = close + (close * interest_rate * until_expire_dates / 365) + (ag_storage_cost  * until_expire_dates)
        print('close',close, 'interest_rate',interest_rate, 'until_expire_dates',until_expire_dates, 'ag_storage_cost',ag_storage_cost)
        result_dict[code] = theoretical_price
    else:
        theoretical_price = close + (close * interest_rate * until_expire_dates / 365) + (au_storage_cost  * until_expire_dates)
        print('close',close, 'interest_rate',interest_rate, 'until_expire_dates',until_expire_dates, 'au_storage_cost',au_storage_cost)
        result_dict[code] = theoretical_price


    # theoretical_price = close + (close * interest_rate * until_expire_dates.days / 365) + 
# df = pro.sge_daily(ts_code='Ag(T+D)', start_date=yesterday, end_date=today, fields='ts_code,trade_date,open,high,low,close')
# close = df['close'].iloc[-1]
print(result_dict)




