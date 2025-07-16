from XtTraderPyApi import *
import time

class MultiAccountCallBack(XtTraderApiCallback):
    def __init__(self, client):
        super().__init__()
        self.client = client
        print("callback __init__, client id:", id(client))

    def onConnected(self, success, error_msg):
        print("[onConnected]", success, error_msg)
        self.client.connected = success

    def onUserLogin(self, username, password, nRequestId, error):
        print("[onUserLogin]", error.isSuccess(), error.errorMsg())
        self.client.logined = error.isSuccess()

    def onRtnLoginStatusWithActKey(self, account_id, status, account_type, account_key, error_msg):
        print("[onRtnLoginStatusWithActKey] called, id:", id(self.client), account_id)
        self.client.account_keys[account_id] = account_key  # 直接收集，无需判断
        print("[onRtnLoginStatusWithActKey] set account_keys:", list(self.client.account_keys.keys())[0])

    def onOrder(self, request_id, order_id, remark, error):
        print("[onOrder]", error.isSuccess(), order_id, error.errorMsg())

class SimpleApiClient:
    def __init__(self, server_addr, username, password):
        self.server_addr = server_addr
        self.username = username
        self.password = password
        self.connected = False
        self.logined = False
        self.account_keys = {}  
        self.api = XtTraderApi.createXtTraderApi(self.server_addr)
        self.callback = MultiAccountCallBack(self)
        self.api.setCallback(self.callback)
        self.api.init("./config")

    def wait_connected(self, timeout=15):
        for _ in range(timeout * 2):
            if self.connected:
                return True
            time.sleep(0.5)
        return False

    def user_login(self):
        machine_info = "192.168.1.1|||||"   # 按需
        appid = "xt_api_2.0"
        authcode = "7f3c92e678f9ec77"
        error = self.api.userLoginSync(self.username, self.password, machine_info, appid, authcode)
        print("[userLoginSync]", error.isSuccess(), error.errorMsg())
        return error.isSuccess()

    def wait_all_account_keys(self, expect_num=1, timeout=10):
        """
        等待回调收集到全部资金账号key。expect_num可根据你的账户资金账号数量设定
        """
        for _ in range(timeout * 2):
            if len(self.account_keys) >= expect_num:
                print("[wait_all_account_keys] 已收集：", self.account_keys)
                return True
            time.sleep(0.5)
        print("[wait_all_account_keys] 当前收集到：", self.account_keys)
        return False

    def order(self, account_id, price, volume, market, code, price_type, operation_type, super_price_rate=0):
        """
        指定资金账号account_id下单，自动获取对应key
        """
        if account_id not in self.account_keys:
            print(f"[future_order] 未知资金账号: {account_id}")
            return
        account_key = self.account_keys[account_id]
        order = COrdinaryOrder()
        order.m_strAccountID = account_id
        order.m_dPrice = price
        order.m_dSuperPriceRate = super_price_rate
        order.m_nVolume = volume
        order.m_strMarket = market
        order.m_strInstrument = code
        order.m_ePriceType = price_type
        order.m_eOperationType = operation_type
        order.m_strRemark = "multi account demo"
        print(f"[future_order] 用 {account_id}({account_key}) 下单 {order.m_strInstrument}, {order.m_dPrice}, {order.m_nVolume}")
        self.api.order(order, 1, account_key)

    def join(self):
        self.api.join()

if __name__ == "__main__":
    server_addr = "192.168.10.100:65300"
    username = "唐斌"
    password = "yml666888"

    client = SimpleApiClient(server_addr, username, password)
    print("main client id:", id(client))
    if not client.wait_connected():
        print("连接失败，退出")
        exit(1)
    if not client.user_login():
        print("登录失败，退出")
        exit(1)

    # 输入实际的账号数量
    expect_account_num = 2
    if not client.wait_all_account_keys(expect_num=1):
        print("没有收集到全部资金账号key，退出")
        exit(1)

    # 打印所有资金账号，可以人工挑选
    print("可用资金账号列表：", client.account_keys)
    # 例如你想用某个资金账号下单：
    # account_id = list(client.account_keys.keys())
    # for acc_id in account_id:
    #     client.order(
    #         account_id=acc_id,
    #         price=50,
    #         volume=1,
    #         market="DCE",
    #         code="jd2508-C-3700",
    #         price_type=EPriceType.PRTP_FIX,
    #         operation_type=EOperationType.OPT_OPEN_SHORT
    #     )
    client.join()
