from xtquant import xtdata
from xtquant import xtdatacenter as xtdc
from calc_HV_IV import calc_iv
import pandas as pd

xtdc.set_token("810b8b575d9401768bb81320214e958f541a34cc958603e65049f2ce")

with open("./option_monitor/data/code.txt", "r") as file:
    lines = file.readlines()

list1 = []
for i in lines:
    i = i.replace("\n", "")
    print(i)
    list1.append(i)


code_list = ["TA509P4600.ZF"]
trading_date = pd.read_csv(
    r"C:\Users\Administrator\Desktop\Liang1\work_space-main\data\trading_days.csv"
)
trading_date = trading_date["trading_days"].tolist()
trading_date = [str(date) for date in trading_date if str(date).startswith("202505")]
for i in trading_date:
    calc_iv(code_list, 0.03, i)
