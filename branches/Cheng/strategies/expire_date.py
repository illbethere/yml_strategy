from read_data import *
from datetime import datetime, timedelta
code = 'ag2508.SF'
today = datetime.now().strftime('%Y-%m-%d')


detail_data = xtdata.get_instrument_detail(code)
# print(detail_data)
expire_date = detail_data['ExpireDate']
print(f"期权代码: {code} 的到期日: {expire_date}")
expire_date = datetime.strptime(expire_date, '%Y%m%d')
today = datetime.strptime(today, '%Y-%m-%d')

date = expire_date - today

print(f"期权代码: {code} 的到期日: {expire_date}, 距离到期天数: {date.days}")

# SF_list = xtdata.get_stock_list_in_sector("SGE")
# print(SF_list)
# with open('SF_list.txt', 'w') as f:
#     for item in SF_list:
#         f.write(f"{item}\n")

spot_list = xtdata.get_stock_list_in_sector('期权市场指数')
print(spot_list)