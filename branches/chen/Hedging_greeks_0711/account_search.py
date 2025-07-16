from XtTraderPyApi import *
import pandas as pd
import time
import threading
import re
from datetime import datetime
from xtquant import xtdata, xtdatacenter

xtdatacenter.set_token("4065054877ce5724155dbc5bcba200381ce5eb35")
xtdatacenter.init()


def extract_code(code):
    """拆分期权代码
    输入：'c2509-P-2750'
    返回：'ao2509P2750.SF' """
    # 拆分
    result = re.findall(r"[a-zA-Z]+|[^a-zA-Z]+", code)

    # 添加后缀
    code_class = result[0]
    code_date = result[1]
    if code_class in [
        "a",
        "b",
        "bz",
        "c",
        "cs",
        "eb",
        "eg",
        "fb",
        "i",
        "j",
        "jd",
        "jm",
        "l",
        "lg",
        "lh",
        "m",
        "p",
        "pg",
        "pp",
        "rr",
        "v",
        "y",
    ]:
        code_suffix = ".DF"  # 大商所
    elif code_class in [
        "ad",
        "ag",
        "al",
        "ao",
        "au",
        "bc",
        "br",
        "bu",
        "cu",
        "ec",
        "fu",
        "hc",
        "lu",
        "ni",
        "nr",
        "pb",
        "rb",
        "ru",
        "sc",
        "sn",
        "sp",
        "ss",
        "wr",
        "zn",
    ]:
        code_suffix = ".SF"  # 上期所
    elif code_class in [
        "AP",
        "CF",
        "CJ",
        "CY",
        "FG",
        "JR",
        "LR",
        "MA",
        "OI",
        "PF",
        "PK",
        "PM",
        "PR",
        "PX",
        "RI",
        "RM",
        "RS",
        "SA",
        "SF",
        "SH",
        "SM",
        "SR",
        "TA",
        "UR",
        "WH",
        "ZC",
    ]:
        code_suffix = ".ZF"  # 郑商所
    elif code_class in ["lc", "ps", "si"]:
        code_suffix = ".GF"  # 广期所
    elif code_class in ["sc"]:
        code_suffix = "INE"
    else:
        print(f"{code}: 未找到品种对应的交易所代码后缀")
        return None
    code = code + code_suffix
    return code

def get_market_data(codes, period, start_time, end_time, count):
    """批量获取行情数据，返回dict"""
    for code in codes:
        xtdata.download_history_data(code, period, start_time, end_time)
    market_data = xtdata.get_market_data_ex(
        [],
        codes,
        period,
        start_time,
        end_time,
        count=count,
        dividend_type="none",
        fill_data=False,
    )
    return market_data

def get_latest_price(code):
    today = time.strftime("%Y%m%d")
    data = get_market_data([code], "1m", today, today, 1)
    if code in data and not data[code].empty:
        return data[code]["close"].iloc[-1]
    else:
        return None

def get_future_code(code):
    # 期权代码有'-'或'C/P'等，需归一化
    # 先去掉所有'-'和'C/P'及后面的内容，只保留主合约部分
    # 提取期货主合约 + 后缀（如.DF/.SF等）
    m = re.match(r"(..[^-PpCc]*)[-PpCc].*(\.\w+)", code)
    if m:
        return m.group(1) + m.group(2)
    # 如果本来就是期货合约
    return code

def get_option_code(code: str):
    ''' 'ag2508.SF' -> 获取标的对应期权代码(Series)'''
    code_prefix = code.split(".")[0]
    market = code.split(".")[1]
    opt_list = xtdata.get_stock_list_in_sector(market)

    opt_list = [opt for opt in opt_list if len(opt) > 11 and opt.startswith(code_prefix)
                and 'MSC' not in opt and 'MSP' not in opt]
    opt_list = pd.Series(opt_list)
    
    return opt_list

def get_expire_time(code: str, today: str):
    '''计算到期时间'''
    detail_data = xtdata.get_instrument_detail(code)
    if detail_data == None:
        raise ValueError(f"{code}: 无法获取信息")
    else:
        expire_date = detail_data['ExpireDate']
        days_to_expiration = (datetime.strptime(expire_date, '%Y%m%d') - datetime.strptime(today, '%Y%m%d')).days
        if days_to_expiration <= 0:
            raise ValueError(f"{code}: T值非正，即将或已到期")
        else:
            return days_to_expiration

def get_multiplier(code: str):
    '''计算合约乘数'''
    detail_data = xtdata.get_instrument_detail(code)
    multiplier = detail_data['VolumeMultiple']
    
    return multiplier


class SimplePositionQuery(XtTraderApiCallback):
    def __init__(self, address, username, password, accountID):
        super().__init__()
        self.address = address
        self.username = username
        self.password = password
        self.accountID = accountID
        self.connected = False
        self.logined = False
        self.api = XtTraderApi.createXtTraderApi(address)
        self.accountKeyDict = {}  # 账号id -> accountKey
        self.today = datetime.now().strftime('%Y%m%d')
        
    def init(self):
        self.api.setCallback(self)
        return self.api.init("./config/")

    def join(self):
        self.api.join_async()

    def onConnected(self, success, error_msg):
        self.connected = success

    def onUserLogin(self, username, password, nRequestId, error):
        self.logined = error.isSuccess()

    def onRtnLoginStatusWithActKey(
        self, account_id, status, account_type, account_key, error_msg
    ):
        # 记录所有账号的 key
        self.accountKeyDict[account_id] = account_key

    def doLogin(self):
        self.api.userLoginSync(
            self.username, self.password, "", "xt_api_2.0", "7f3c92e678f9ec77"
        )

    def reqPositionStaticsSync(self, accountIDs=None):
        """
        accountIDs: list or str, 支持单账号或账号列表。如果为None，则查self.accountID
        """
        error = XtError(0, "")
        if accountIDs is None:
            accountIDs = [self.accountID]
        elif isinstance(accountIDs, str):
            accountIDs = [accountIDs]

        all_data = []
        for aid in accountIDs:
            accountKey = self.accountKeyDict.get(aid, "")
            if not accountKey:
                print(f"账号 {aid} 未获取到accountKey，已跳过")
                continue
            pos_list = self.api.reqPositionStaticsSync(aid, error, accountKey)
            if error.isSuccess():
                for x in pos_list:
                    if getattr(x, "m_nPosition", 0) != 0:
                        all_data.append(
                            {
                                "账号": aid,
                                "合约代码": x.m_strInstrumentID,
                                "总持仓": x.m_nPosition,
                                "方向": x.m_nDirection,
                                "保证金": x.m_dUsedMargin,
                            }
                        )
            else:
                print(f"账号 {aid} 持仓查询失败:", error.errorMsg())
        df = pd.DataFrame(all_data)
        df = df[df["总持仓"] != 0].reset_index(drop=True)
        df["方向"] = df["方向"].apply(
            lambda x: -1
            if x == EEntrustBS.ENTRUST_SELL
            else 1
            if x == EEntrustBS.ENTRUST_BUY
            else 0
        )
        df["合约代码"] = df["合约代码"].apply(extract_code)
        df["期权现价"] = df["合约代码"].apply(get_latest_price)
        df["期货代码"] = df["合约代码"].apply(get_future_code)
        df["期货现价"] = df["期货代码"].apply(get_latest_price)
        df["到期时间"] = df["合约代码"].apply(get_expire_time, today=self.today)
        df["合约乘数"] = df["合约代码"].apply(get_multiplier)
        
        return df


# if __name__ == "__main__":
#     server_addr = "192.168.10.100:65300"
#     username = "唐斌"
#     password = "yml666888"
#     accountIDs = ["8000138", "709981"]
#     start = time.time()
#     # 1. 查询持仓
#     pos_query = SimplePositionQuery(server_addr, username, password, accountIDs[0])
#     pos_query.init()
#     pos_query.join()
#     while not pos_query.connected:
#         time.sleep(0.1)
#     pos_query.doLogin()
#     while not all(aid in pos_query.accountKeyDict for aid in accountIDs):
#         time.sleep(0.1)
#     df_pos = pos_query.reqPositionStaticsSync(accountIDs)
#     print("持仓合约：")
#     print(df_pos)
#     print(time.time() - start)
#     df_pos.to_csv("position_static.csv")






