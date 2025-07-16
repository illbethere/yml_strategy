from xtquant import xtdatacenter as xtdc
from xtquant import xtdata

xtdc.set_token('4065054877ce5724155dbc5bcba200381ce5eb35')
xtdc.init()

def get_put_option_list(future_code: str, date: str):

    xtdata.download_history_contracts()
    option_list = xtdata.get_option_list(future_code, date, 'PUT', isavailavle= False)

    # option_list = self.put_option_list[future_code]
    # print(self.put_option_list)
    return option_list  

def get_history_main_contract(codes: list):
        """获取历史主力合约数据"""

        period = "historymaincontract"
        if isinstance(codes, list):
            codes = codes[0]
        xtdata.download_history_data(codes, period, '', '')
        if isinstance(codes, str):
            codes = [codes]
        data = xtdata.get_market_data_ex([], codes, period)

        return data


if __name__ == '__main__':
    future_code = 'cj2505.ZF'  # 期货代码
    date = ''
    with open('code(2).txt', 'r') as f:
        future_code = f.read().strip()
        print(future_code)

    put_option_list = get_put_option_list(future_code, date)
    print(put_option_list)

    code = 'cj00.ZF'
    data = get_history_main_contract(code)
    # print(data)
    data = data[code]
    print(data)
    with open('cj00.ZF.txt', 'w') as f:
        f.write('time,合约在交易所的代码,期货统一规则代码,次主力合约代码\n')
        for index, row in data.iterrows():
            line = f"{row['time']},{row['合约在交易所的代码']},{row['期货统一规则代码']},{row['次主力合约代码']}\n"
            f.write(line)
