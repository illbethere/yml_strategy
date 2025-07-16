from xtquant import xtdata, xtdatacenter
import pandas as pd
import datetime

xtdatacenter.set_token("4065054877ce5724155dbc5bcba200381ce5eb35")
xtdatacenter.init()

code = ["ps2509.GF"]

today = datetime.datetime.now().strftime("%Y%m%d")
for c in code:
    xtdata.subscribe_quote(c, "1m",today, today, 1)
df = xtdata.get_market_data([],["ps2509.GF"], "1m", today, today, 1)["ps2509.GF"]
df.to_csv("ps2509.GF_1m.csv", index=False)