from read_data import *
from calc_HV_IV import calc_iv
from xtquant import xtdatacenter as xtdc
from xtquant import xtdata
from datetime import datetime, timedelta


xtdc.set_token('4065054877ce5724155dbc5bcba200381ce5eb35')
xtdc.init()

codes = ['ao2508C3100.SF', 'rb2510P2900.SF', 'sn2508P245000.SF', 'ag2508C9300.SF']
count = 0
time_list = []
while True:
    start_time = datetime.now()
    option_data = xtdata.get_full_tick(codes)
    print("1", option_data[codes[0]]['askPrice'][1])
    print("2",option_data[codes[1]]['bidPrice'][1])
    print("3", option_data[codes[2]]['askPrice'][1])
    print("4", option_data[codes[3]]['askPrice'][1])
    end_time = datetime.now()
    time_loss = end_time - start_time
    time_list.append(time_loss)
    count += 1
    print(f"获取期权数据耗时: {end_time - start_time}")

    if count >= 10000:
        break

avg_time_loss = sum(time_list, timedelta()) / len(time_list)
print(f"平均获取期权数据耗时: {avg_time_loss}")
    