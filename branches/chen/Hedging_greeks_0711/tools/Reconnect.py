import time
from xtquant_gt.xttrader import XtQuantTrader, XtQuantTraderCallback
from xtquant_gt.xttype import StockAccount
from xtquant_gt import xtconstant

xt_trader_stauts = 1


class MyXtQuantTraderCallback(XtQuantTraderCallback):
    def __init__(self, log):
        self.log = log

    # 更多说明见 http://dict.thinktrader.net/nativeApi/xttrader.html?id=I3DJ97#%E5%A7%94%E6%89%98xtorder
    def on_disconnected(self):
        """
        连接断开
        :return:
        """
        print("connection lost, 交易接口断开，即将重连")
        self.log.info("connection lost, 交易接口断开，即将重连")
        global xt_trader_stauts
        xt_trader_stauts = 0

    def on_stock_order(self, order):
        print(
            f'委托回报: 股票代码:{order.stock_code} 账号:{order.account_id}, 订单编号:{order.order_id} 柜台合同编号:{order.order_sysid} \
            委托状态:{order.order_status} 成交数量:{order.order_status} 委托数量:{order.order_volume} 已成数量：{order.traded_volume}')

    def on_stock_trade(self, trade):
        print(
            f'成交回报: 股票代码:{trade.stock_code} 账号:{trade.account_id}, 订单编号:{trade.order_id} 柜台合同编号:{trade.order_sysid} \
            成交编号:{trade.traded_id} 成交数量:{trade.traded_volume} 委托数量:{trade.direction} ')

    def on_order_error(self, order_error):
        print(
            f"报单失败： 订单编号：{order_error.order_id} 下单失败具体信息:{order_error.error_msg} 委托备注:{order_error.order_remark}")

    def on_cancel_error(self, cancel_error):
        print(
            f"撤单失败: 订单编号：{cancel_error.order_id} 失败具体信息:{cancel_error.error_msg} 市场：{cancel_error.market}")

    def on_order_stock_async_response(self, response):
        print(f"异步下单的请求序号:{response.seq}, 订单编号：{response.order_id} ")

    def on_account_status(self, status):
        print(f"账号状态发生变化， 账号:{status.account_id} 最新状态：{status.status}")


def create_trader(xt_acc, path, session_id, log):
    trader = XtQuantTrader(path, session_id, callback=MyXtQuantTraderCallback(log))
    trader.start()
    connect_result = trader.connect()
    trader.subscribe(xt_acc)
    return trader if connect_result == 0 else None


def try_connect(xt_acc, path, log):
    session_id_range = [i for i in range(301, 321)]

    import random
    random.shuffle(session_id_range)

    # 遍历尝试session_id列表尝试连接
    for session_id in session_id_range:
        trader = create_trader(xt_acc, path, session_id, log)
        if trader:
            log.info(f'连接成功，session_id:{session_id}')
            print(f'连接成功，session_id:{session_id}')
            return trader
        else:
            log.info(f'连接失败，session_id:{session_id}，继续尝试下一个id')
            print(f'连接失败，session_id:{session_id}，继续尝试下一个id')
            continue

    log.info('所有id都尝试后仍失败，放弃连接')
    print('所有id都尝试后仍失败，放弃连接')
    return None


def reconnect_xttrader(origin_xt_trader, xt_acc, path, log):
    global xt_trader_stauts
    if xt_trader_stauts == 0:
        new_xt_trader = try_connect(xt_acc, path, log)
        if new_xt_trader is not None:
            xt_trader_stauts = 1
        return new_xt_trader
    else:
        return origin_xt_trader


def connect_xttrader(xt_acc, path, log):
    xt_trader = try_connect(xt_acc, path, log)
    return xt_trader