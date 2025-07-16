from xtquant import xtdata, xtdatacenter
import time

now = time.time()
xtdatacenter.set_token("4065054877ce5724155dbc5bcba200381ce5eb35")
xtdatacenter.init()
print(time.time() - now)
markets = ["大商所", "郑商所", "上期所", "广交所", "能源中心"]

opt_list = []
for market in markets:
    opt_list += xtdata.get_stock_list_in_sector(market)

opt_list = [opt for opt in opt_list if len(opt) > 11 and not opt.startswith("SH")]
print(opt_list)
print(time.time() - now)

# for i in markets:
#     opt_list.append(xtdata.get_main_contract(i))
#     opt_list.append(xtdata.get_main_contract(f'过期{i}'))
