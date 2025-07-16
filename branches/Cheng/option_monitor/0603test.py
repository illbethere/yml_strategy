from xtquant import xtdatacenter as xtdc
from xtquant import xtdata
import re
xtdc.set_token('4065054877ce5724155dbc5bcba200381ce5eb35')
xtdc.init()
# option_pattern = re.compile(r"^[a-zA-Z]+\d{4}-[CP]-\d+\.GF$")

# xtdata.subscribe_quote(stock_code, period='', start_time='', end_time='', count=0, callback=None)
# data1 = xtdata.download_history_data('rb2601.SHFE', period = '1m', start_time='20240101', end_time='20250531')
# data = xtdata.get_market_data_ex(field_list=[], 
#                                  stock_list=['rb2601.SHFE'], 
#                                  period='1m', 
#                                  start_time = '20240101', 
#                                  end_time='20250531', 
#                                  count=-1)

data = xtdata.get_stock_list_in_sector('SF')
print(data)
codes = []
for code in data:
    if len(code) == 7 and 'JQ00' not in code and '00' in code:
        codes.append(code)
print(codes)
# codes = []
# for code in data:
#     if option_pattern.match(code):
#         codes.append(code)
# print(codes)
with open('data/code.txt', 'wb') as f:
    for code in codes:
        f.write(code.encode('utf-8') + b'\n')
