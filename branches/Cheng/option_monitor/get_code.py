from xtquant import xtdatacenter as xtdc
from xtquant import xtdata
import pandas as pd
from datetime import datetime, timedelta
import time

xtdc.set_token('4065054877ce5724155dbc5bcba200381ce5eb35')
xtdc.init()
today = datetime.now().date().strftime('%Y%m%d')

undl_code_ref = 'ni2502.SF'
xtdata.download_history_contracts()
xtdata.download_history_data(undl_code_ref, period = '1d', start_time='', end_time='')
data = xtdata.get_option_undl_data(undl_code_ref)
option_list_PUT = xtdata.get_option_list(undl_code=undl_code_ref,dedate='20250101',opttype='PUT')
print(data, option_list_PUT)

# data_1 = xtdata.get_stock_list_in_sector('ZF')
# print(data_1)


# data2 = xtdata.get_full_tick(['SH509C2560.ZF'])
# print(data2)

# data3 = xtdata.get_market_data_ex([],['sh509.ZF'],period='tick')
# print(data3)

# def get_market_data(codes: list, period: str, start_time: str, end_time: str, count: int) -> dict:
#     for code in codes:
#         xtdata.subscribe_quote(code, period, start_time, end_time, count, callback=None)
#         xtdata.download_history_data(code, period, start_time, end_time)

#     market_data = xtdata.get_market_data_ex([], codes, period, start_time, end_time, count=count, dividend_type='none',
#                                             fill_data=False)

#     for code in codes:
#         if market_data[code].empty:
#             print(f"数据 {code} 获取失败！")
#             break

#     # market_data['time'] = pd.to_datetime(market_data['time'], unit='ms')
#     # market_data["time"] = market_data["time"] + pd.Timedelta(hours=8)#转为北京时区
#     # market_data["time"] = market_data['time'].dt.strftime('%Y%m%d')#将Y-m-d变为Ymd

#     return market_data

# dict_data = get_market_data(['jd2507.DF'], '1d', '20250407', today, 30)
# print(dict_data)