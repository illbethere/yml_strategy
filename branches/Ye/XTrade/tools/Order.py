import re
import time

import xtquant.xtdata as xtdata
from xtquant import xtdatacenter as xtdc
import pandas as pd
import datetime
from typing import Union, List, Dict
import numpy as np
from xtquant.qmttools.contextinfo import ContextInfo
from xtquant.qmttools.functions import get_trade_detail_data, passorder
import warnings
from xtquant_gt import xttrader
from xtquant_gt import xtconstant
from xtquant_gt.xttype import StockAccount
from tools.DebugTool import try_except
import math

xtdc.set_token("4065054877ce5724155dbc5bcba200381ce5eb35")
xtdc.init()

@try_except
def order_target_value(stock_code: str, target_value, account: Union[str, StockAccount], contextinfo: ContextInfo,
                       order_id: str = '', price=-1, xt_trader: Union[None, xttrader.XtQuantTrader] = None,
                       quote_mode: str = 'backtest', quick_trade=True) -> None:
    '''
    将持仓调整至目标金额，没有该持仓会买入；金额为0时卖出全部持仓；可指定price参数，默认-1为市价单，只支持股票
    :param stock_code: 标的代码
    :param target_value: 目标持仓金额
    :param account: 账户
    :param contextinfo: 含有k线信息和接口的上下文对象
    :param order_id: 订单号
    :param price: 委托价格
    :param xt_trader: API实例对象
    :param quote_mode: 模式（回测/模拟盘/实盘）
    :param quick_trade: 是否快速成交
    :return: None
    '''
    if quote_mode in ['realtime', 'all']:
        if type(account) is not StockAccount: raise TypeError("实盘/模拟盘传入账户应当为StockAccount类型")
        if type(xt_trader) is None: raise TypeError("实盘/模拟盘应当传入xt_trader参数，且类型为XtQuantTrader")
        remark = datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
        for i in range(1, 11):
            print(f'尝试下单 {i}代码:{stock_code}')
            current_value = 0
            usable_value = 0
            can_use_volume = 0
            current_price = \
                xtdata.get_full_tick([stock_code])[stock_code]['lastPrice']
            position_list = xt_trader.query_stock_positions(account)
            available_cash = xt_trader.query_stock_asset(account).cash
            available_cash = available_cash * 0.9995  # 预留手续费
            for position in position_list:
                if position.stock_code == stock_code and position.volume > 0:
                    current_value = position.market_value
                    usable_value = position.can_use_volume / position.volume * current_value
                    can_use_volume = position.can_use_volume
                    break
            adjust_value = target_value - current_value
            if adjust_value < 0:
                if usable_value < abs(adjust_value):
                    warnings.warn(f'{stock_code}可用数量不足，将卖出所有可用持仓。')
                    adjust_value = -usable_value

                sell_volume = abs(adjust_value) / current_price if price == -1 else abs(adjust_value) / price
                if stock_code[:2] in ['00', '60', '30']:
                    sell_volume = int(sell_volume // 100) * 100
                elif stock_code[:2] == '68':
                    sell_volume = sell_volume if sell_volume >= 200 else can_use_volume
                elif stock_code[0] == '1':
                    sell_volume = int(sell_volume // 10) * 10
                elif stock_code[0] in ['4', '8', '9']:
                    sell_volume = sell_volume if sell_volume >= 100 else can_use_volume
                else:
                    sell_volume = int(sell_volume // 100) * 100

                resp = xt_trader.order_stock_async(account, stock_code, 24, sell_volume, 5 if price == -1 else 11,
                                                   price,
                                                   'order_target_value', remark)
            else:
                buy_volume = adjust_value / current_price if price == -1 else adjust_value / price
                if stock_code[:2] in ['00', '60', '30']:
                    buy_volume = int(buy_volume // 100) * 100
                elif stock_code[:2] == '68':
                    buy_volume = buy_volume if buy_volume >= 200 else can_use_volume
                elif stock_code[0] == '1':
                    buy_volume = int(buy_volume // 10) * 10
                else:
                    buy_volume = int(buy_volume // 100) * 100

                if stock_code[:2] in ['00', '60', '30']:
                    can_buy_volume = int(
                        (available_cash / current_price if price == -1 else available_cash / price)) // 100 * 100
                elif stock_code[:2] == '68':
                    can_buy_volume = int(available_cash / current_price) if price == -1 else int(available_cash / price)
                    can_buy_volume = can_buy_volume if can_buy_volume >= 200 else 0
                elif stock_code[0] == '1':
                    can_buy_volume = int(
                        (available_cash / current_price if price == -1 else available_cash / price)) // 10 * 10
                else:
                    can_buy_volume = int(
                        (available_cash / current_price if price == -1 else available_cash / price)) // 100 * 100

                if can_buy_volume == 0:
                    warnings.warn('可买数量为0')
                    return
                if buy_volume <= can_buy_volume:
                    resp = xt_trader.order_stock_async(account, stock_code, 23, buy_volume, 5 if price == -1 else 11,
                                                       price,
                                                       'order_target_value', remark)
                else:
                    warnings.warn(f'原下单数量{buy_volume}，可用资金不足，将调整下单数量为{can_buy_volume}。')
                    resp = xt_trader.order_stock_async(account, stock_code, 23, can_buy_volume,
                                                       5 if price == -1 else 11,
                                                       price,
                                                       'order_target_value', remark)
            if not quick_trade:
                break
            if i == 10:
                print(f'{stock_code}暂未成交，维持最后委托')
                break
            time.sleep(1.5)
            orders = [
                {'status': order.order_status, 'remark': order.order_remark, 'time': order.order_time,
                 'sysid': order.order_sysid, 'id':order.order_id, 'type': order.order_type}
                for order in
                xt_trader.query_stock_orders(account) if order.order_remark == remark]
            if len(orders) == 0:
                print(f'{stock_code}此备注（{remark}）无委托任务')
                break
            orders = sorted(orders, key=lambda x: x['time'])
            print(orders)
            latest_order = orders[-1]
            if latest_order['status'] == 56:
                break
            else:
                resp = None
                if latest_order['sysid'] is not None:
                    resp = xt_trader.cancel_order_stock_sysid_async(account, 0 if 'SH' in stock_code else 1,
                                                                    latest_order['sysid'])
                elif latest_order['id'] is not None:
                    resp = xt_trader.cancel_order_stock_async(account, latest_order['id'])
                else:
                    print(f'{stock_code}查询不到委托，无法进行撤单重下')
                    break
                for i in range(1, 6):
                    if resp == -1:
                        print(f'{stock_code}撤单暂未成功_{i}')
                        time.sleep(0.5)
                    elif resp is None:
                        print(f'{stock_code}撤单暂未响应_{i}')
                        time.sleep(0.5)
                    else:
                        print(f'{stock_code}撤单成功')
                        break
                new_orders = [{'status': order.order_status, 'remark': order.order_remark, 'time': order.order_time}
                              for order in xt_trader.query_stock_orders(account) if order.order_remark == remark]
                order_status = sorted(new_orders, key=lambda x: x['time'], reverse=False)[-1]['status']
                if resp == -1:
                    print(f'{stock_code}撤单失败, 无法进行重下，维持原委托')
                    break
                elif resp is None:
                    print(f'{stock_code}撤单无响应，无法进行重下，维持原委托')
                    break
                elif order_status == 56:
                    print(f'{stock_code}最近一笔交易已全部成交，不进入重下流程')
                    break
                else:
                    current_price = xtdata.get_full_tick([stock_code])[stock_code]['lastPrice']
                    price = current_price * 1.001 if latest_order['type'] == 23 else current_price * 0.999
                    info_dict = xtdata.get_instrument_detail(stock_code)
                    price = max(min(price, info_dict['UpStopPrice']), info_dict['DownStopPrice'])
                    print(f'{stock_code}委托价调整为市价偏离0.1%即{price}，准备重新下单')
    else:
        if type(account) is not str: raise TypeError('回测传入账户应当为str类型')
        position_value = {dt.m_strInstrumentID: dt.m_dMarketValue for dt in
                          get_trade_detail_data(account, 'stock', 'position')}
        position_usable_value = {dt.m_strInstrumentID: dt.m_dLastPrice * dt.m_nCanUseVolume for dt in
                                 get_trade_detail_data(account, 'stock', 'position')}
        if stock_code[:-3] in position_value.keys():
            current_value = position_value[stock_code[:-3]]
            usable_value = position_usable_value[stock_code[:-3]]
        else:
            current_value = 0
            usable_value = 0
        if current_value == target_value:
            return
        if current_value < target_value:
            passorder(
                23, 1102, account
                , stock_code, 5 if price == -1 else 11, price, target_value - current_value
                , 'order_target_value', 1,
                datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                , contextinfo
            )
        else:
            if current_value - target_value < usable_value:
                passorder(
                    24, 1102, account
                    , stock_code, 5 if price == -1 else 11, price, current_value - target_value
                    , 'order_target_value', 1,
                    datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                    , contextinfo
                )
            else:
                passorder(
                    24, 1102, account
                    , stock_code, 5 if price == -1 else 11, price, usable_value
                    , 'order_target_value', 1,
                    datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                    , contextinfo
                )
    return


@try_except
def order_target_volume_final(stock_code: str, target_volume, account: Union[str, StockAccount],
                              contextinfo: ContextInfo,
                              order_id: str = '', price=-1, xt_trader: Union[None, xttrader.XtQuantTrader] = None,
                              quote_mode: str = 'backtest', quick_trade=True, order_count=1,
                              order_price_type='market_order') -> None:
    """
    将持仓调整至目标数量
    order_price_type is in ['limit_order','limit_market_order','market_order']
    """
    if target_volume < 0: raise ValueError("目标数量应当位于为自然数")
    if quote_mode in ['realtime', 'all']:
        if type(account) is not StockAccount: raise TypeError("实盘/模拟盘传入账户应当为StockAccount类型")
        if type(xt_trader) is None: raise TypeError("实盘/模拟盘应当传入xt_trader参数，且类型为XtQuantTrader")
        remark = datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
        for i in range(1, order_count + 1):
            print(f'尝试下单-{i}代码:{stock_code}')

            current_weight = 0
            volume = 0
            usable_volume = 0
            current_price = \
                xtdata.get_full_tick([stock_code])[stock_code]['lastPrice']
            total_value = xt_trader.query_stock_asset(account).total_asset
            position_list = xt_trader.query_stock_positions(account)
            available_cash = xt_trader.query_stock_asset(account).cash
            # available_cash = available_cash * 0.9995  # 预留手续费

            current_volume = 0
            usable_volume = 0
            for position in position_list:
                if position.stock_code == stock_code and position.volume > 0:
                    current_volume = position.volume
                    usable_volume = position.can_use_volume
                    break

            adjust_volume = (target_volume - current_volume)

            if adjust_volume < 0:

                if usable_volume > 0:

                    sell_volume = abs(adjust_volume)

                    if sell_volume > usable_volume:
                        warnings.warn(f'{stock_code}可用数量不足，将卖出所有可用持仓！')

                    sell_volume = min(sell_volume, usable_volume)

                    if stock_code[:2] in ['00', '60', '30']:
                        sell_volume = int(sell_volume // 100) * 100
                    elif stock_code[:2] == '68':
                        sell_volume = sell_volume if sell_volume >= 200 else usable_volume
                    elif stock_code[0] == '1':
                        sell_volume = int(sell_volume // 10) * 10
                    elif stock_code[0] in ['4', '8', '9']:
                        sell_volume = sell_volume if sell_volume >= 100 else usable_volume
                    else:
                        sell_volume = int(sell_volume // 100) * 100

                    current_price = xtdata.get_full_tick([stock_code])[stock_code]['lastPrice']

                    if price == -1 or order_price_type == 'market_order':
                        order_price = current_price
                    elif price != -1 and order_price_type == 'limit_order':
                        order_price = max(price, xtdata.get_instrument_detail(stock_code)['DownStopPrice'])
                    elif price != -1 and order_price_type == 'limit_market_order':
                        order_price = max(current_price * (1 - price),
                                          xtdata.get_instrument_detail(stock_code)['DownStopPrice'])
                    else:
                        order_price = current_price

                    if sell_volume > 0:
                        resp = xt_trader.order_stock_async(account, stock_code, 24, sell_volume, 11,
                                                           order_price,
                                                           'order_target_weight', remark)
                else:
                    warnings.warn(f'{stock_code}无可用持仓！')
                    return

            elif adjust_volume > 0:
                if available_cash > total_value * 0.0005:

                    current_price = xtdata.get_full_tick([stock_code])[stock_code]['lastPrice']

                    if price == -1 or order_price_type == 'market_order':
                        order_price = current_price
                    elif price != -1 and order_price_type == 'limit_order':
                        order_price = min(price, xtdata.get_instrument_detail(stock_code)['UpStopPrice'])
                    elif price != -1 and order_price_type == 'limit_market_order':
                        order_price = min(current_price * (1 + price),
                                          xtdata.get_instrument_detail(stock_code)['UpStopPrice'])
                    else:
                        order_price = current_price

                    buy_volume = adjust_volume
                    can_buy_volume = available_cash / order_price

                    if buy_volume > can_buy_volume:
                        warnings.warn(f'{stock_code}可用现金不足，用剩余现金全部买入！')

                    buy_volume = min(buy_volume, can_buy_volume)

                    if stock_code[:2] in ['00', '60', '30']:
                        buy_volume = int(buy_volume // 100) * 100
                    elif stock_code[:2] == '68':
                        buy_volume = buy_volume if buy_volume >= 200 else 0
                    elif stock_code[0] == '1':
                        buy_volume = int(buy_volume // 10) * 10
                    elif stock_code[0] in ['4', '8', '9']:
                        buy_volume = buy_volume if buy_volume >= 100 else 0
                    else:
                        buy_volume = int(buy_volume // 100) * 100

                    if buy_volume > 0:
                        resp = xt_trader.order_stock_async(account, stock_code, 23, buy_volume, 11,
                                                           order_price,
                                                           'order_target_weight', remark)

                else:
                    warnings.warn(f'{stock_code}无可用现金！')
                    return

            if not quick_trade:
                break
            # if i == 10:
            #     print(f'{stock_code}暂未成交，维持最后委托')
            #     break
            time.sleep(1)
            orders = [
                {'status': order.order_status, 'remark': order.order_remark, 'time': order.order_time,
                 'sysid': order.order_sysid, 'id': order.order_id}
                for order in
                xt_trader.query_stock_orders(account) if order.order_remark == remark]
            if len(orders) == 0:
                print(f'{stock_code}今日无委托任务')
                break
            orders = sorted(orders, key=lambda x: x['time'])
            print(orders)
            latest_order = orders[-1]
            if latest_order['status'] == 56:
                break
            else:
                resp = None
                if latest_order['sysid'] is not None:
                    resp = xt_trader.cancel_order_stock_sysid_async(account, 0 if 'SH' in stock_code else 1,
                                                                    latest_order['sysid'])
                elif latest_order['id'] is not None:
                    resp = xt_trader.cancel_order_stock_async(account, latest_order['id'])
                else:
                    print(f'{stock_code}查询不到委托，无法进行撤单重下')
                    break
                for i in range(1, 6):
                    if resp == -1:
                        print(f'{stock_code}撤单暂未成功_{i}')
                        time.sleep(0.2)
                    elif resp is None:
                        print(f'{stock_code}撤单暂未响应_{i}')
                        time.sleep(0.2)
                    else:
                        print(f'{stock_code}撤单成功')
                        break
                if resp == -1:
                    print(f'{stock_code}撤单失败, 无法进行重下，维持原委托')
                    break
                elif resp is None:
                    print(f'{stock_code}撤单无响应，无法进行重下，维持原委托')
                    break
                else:
                    print(f'{stock_code}委托价调整为市价，准备重新下单')
                    price = -1
    else:

        if type(account) is not str: raise TypeError('回测传入账户应当为str类型')
        current_volume_dict = {dt.m_strInstrumentID: dt.m_nVolume for dt in
                               get_trade_detail_data(account, 'stock', 'position')}
        if stock_code[:-3] in current_volume_dict.keys():
            current_volume = current_volume_dict[stock_code[:-3]]
        else:
            current_volume = 0

        adjust_volume = (target_volume - current_volume)

        if adjust_volume > 0:
            passorder(
                23, 1101, account
                , stock_code, 5 if price == -1 else 11, price, adjust_volume
                , 'order_volume', 1,
                datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                , contextinfo
            )
        elif adjust_volume < 0:
            useable_volume_dict = {dt.m_strInstrumentID: dt.m_nCanUseVolume for dt in
                                   get_trade_detail_data(account, 'stock', 'position')}
            if stock_code[:-3] not in useable_volume_dict.keys():
                raise Exception(f'当前账户{account}没有{stock_code}持仓')
            else:
                useable_volume = useable_volume_dict[stock_code[:-3]]
                adjust_volume = min(abs(adjust_volume), useable_volume)
                passorder(
                    24, 1101, account
                    , stock_code, 5 if price == -1 else 11, price, adjust_volume
                    , 'order_volume', 1,
                    datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                    , contextinfo
                )
    return

@try_except
def order_target_weight(stock_code: str, target_weight, account: Union[str, StockAccount], contextinfo: ContextInfo,
                        order_id: str = '', price=-1, xt_trader: Union[None, xttrader.XtQuantTrader] = None,
                        quote_mode: str = 'backtest', quick_trade=True) -> None:
    '''
    将持仓调整至目标权重，没有该持仓会买入；权重为0时卖出全部持仓；可指定price参数，默认-1为市价单，只支持股票
    :param stock_code: 标的代码
    :param target_weight: 目标持仓权重
    :param account: 账户
    :param contextinfo: 含有k线信息和接口的上下文对象
    :param order_id: 订单号
    :param price: 委托价格
    :param xt_trader: API实例对象
    :param quote_mode: 模式（回测/模拟盘/实盘）
    :param quick_trade: 是否快速成交
    :return: None
    '''
    if 1 < target_weight or target_weight < 0: raise ValueError("目标权重应当位于0到1之间（闭区间）")
    if quote_mode in ['realtime', 'all']:
        if type(account) is not StockAccount: raise TypeError("实盘/模拟盘传入账户应当为StockAccount类型")
        if type(xt_trader) is None: raise TypeError("实盘/模拟盘应当传入xt_trader参数，且类型为XtQuantTrader")
        remark = datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
        for i in range(1, 11):
            print(f'尝试下单{i} 代码:{stock_code}')

            current_value = 0
            usable_value = 0
            usable_volume = 0
            current_price = xtdata.get_full_tick([stock_code])[stock_code]['lastPrice']
            total_value = xt_trader.query_stock_asset(account).total_asset
            position_list = xt_trader.query_stock_positions(account)
            available_cash = xt_trader.query_stock_asset(account).cash
            available_cash = available_cash * 0.9995  # 预留手续费
            for position in position_list:
                if position.stock_code == stock_code and position.volume > 0:
                    # current_value = position.volume * current_price if price == -1 else position.volume * price
                    current_value = position.market_value
                    usable_value = position.can_use_volume / position.volume * position.market_value
                    usable_volume = position.can_use_volume
                    break
            if abs(target_weight - current_value / total_value) < 0.0005 and target_weight != 0:
                return
            adjust_value = (target_weight - current_value / total_value) * total_value
            print(f'调整价值{adjust_value}, 申报价格{price}')
            if adjust_value < 0:
                if usable_value < abs(adjust_value):
                    warnings.warn(f'{stock_code}可用数量不足，将卖出所有可用持仓。')
                    print(f'{stock_code}可用数量{usable_value}不足，将卖出所有可用持仓。')
                    adjust_value = -usable_value

                sell_volume = abs(adjust_value) / current_price if price == -1 else abs(adjust_value) / price
                if stock_code[:2] in ['00', '60', '30']:
                    sell_volume = int(sell_volume // 100) * 100
                elif stock_code[:2] == '68':
                    sell_volume = sell_volume if sell_volume >= 200 else usable_volume
                elif stock_code[0] == '1':
                    sell_volume = int(sell_volume // 10) * 10
                elif stock_code[0] in ['4', '8', '9']:
                    sell_volume = sell_volume if sell_volume >= 100 else usable_volume
                else:
                    sell_volume = int(sell_volume // 100) * 100

                if sell_volume > usable_volume:
                    warnings.warn(f'{stock_code}可用数量不足，将卖出所有可用持仓。')
                    sell_volume = usable_volume
                print(f'卖出数量{sell_volume}')
                resp = xt_trader.order_stock_async(account, stock_code, 24, sell_volume, 5 if price == -1 else 11,
                                                   price,
                                                   'order_target_weight', remark)
            else:
                # print(price)
                buy_volume = adjust_value / current_price if price == -1 else adjust_value / price
                if stock_code[:2] in ['00', '60', '30']:
                    buy_volume = int(buy_volume // 100) * 100
                elif stock_code[:2] == '68':
                    buy_volume = buy_volume if buy_volume >= 200 else usable_volume
                elif stock_code[0] == '1':
                    buy_volume = int(buy_volume // 10) * 10
                else:
                    buy_volume = int(buy_volume // 100) * 100

                if stock_code[:2] in ['00', '60', '30']:
                    can_buy_volume = int(
                        (available_cash / current_price if price == -1 else available_cash / price)) // 100 * 100
                elif stock_code[:2] == '68':
                    can_buy_volume = int(available_cash / current_price) if price == -1 else int(available_cash / price)
                    can_buy_volume = can_buy_volume if can_buy_volume >= 200 else 0
                elif stock_code[0] == '1':
                    can_buy_volume = int(
                        (available_cash / current_price if price == -1 else available_cash / price)) // 10 * 10
                else:
                    can_buy_volume = int(
                        (available_cash / current_price if price == -1 else available_cash / price)) // 100 * 100

                if can_buy_volume == 0:
                    warnings.warn('可买数量为0')
                    return
                if buy_volume <= can_buy_volume:
                    print(f'买入数量{buy_volume}')
                    resp = xt_trader.order_stock_async(account, stock_code, 23, buy_volume, 5 if price == -1 else 11,
                                                       price,
                                                       'order_target_weight', remark)
                else:
                    warnings.warn(f'原下单数量{buy_volume}，可用资金不足，将调整下单数量为{can_buy_volume}。')
                    resp = xt_trader.order_stock_async(account, stock_code, 23, can_buy_volume,
                                                       5 if price == -1 else 11,
                                                       price,
                                                       'order_target_weight', remark)
            if not quick_trade:
                break
            if i == 10:
                print(f'{stock_code}暂未成交，维持最后委托')
                break
            time.sleep(2)
            orders = [
                {'status': order.order_status, 'remark': order.order_remark, 'time': order.order_time,
                 'sysid': order.order_sysid, 'id': order.order_id, 'type': order.order_type}
                for order in
                xt_trader.query_stock_orders(account) if order.order_remark == remark]
            if len(orders) == 0:
                print(f'{stock_code}此备注（{remark}）无委托任务')
                break
            orders = sorted(orders, key=lambda x: x['time'])
            print(orders)
            latest_order = orders[-1]
            if latest_order['status'] == 56:
                break
            else:
                resp = None
                if latest_order['sysid'] is not None:
                    resp = xt_trader.cancel_order_stock_sysid_async(account, 0 if 'SH' in stock_code else 1,
                                                                    latest_order['sysid'])
                elif latest_order['id'] is not None:
                    resp = xt_trader.cancel_order_stock_async(account, latest_order['id'])
                else:
                    print(f'{stock_code}查询不到委托，无法进行撤单重下')
                    break
                for i in range(1, 6):
                    if resp < 0:
                        print(f'{stock_code}撤单暂未成功_{i}')
                        time.sleep(0.5)
                    elif resp is None:
                        print(f'{stock_code}撤单暂未响应_{i}')
                        time.sleep(0.5)
                    else:
                        print(f'{stock_code}撤单成功')
                        break
                new_orders = [{'status': order.order_status, 'remark': order.order_remark, 'time': order.order_time}
                              for order in xt_trader.query_stock_orders(account) if order.order_remark == remark]
                order_status = sorted(new_orders, key=lambda x: x['time'], reverse=False)[-1]['status']
                if resp < 0:
                    print(f'{stock_code}撤单失败, 无法进行重下，维持原委托')
                    break
                elif resp is None:
                    print(f'{stock_code}撤单无响应，无法进行重下，维持原委托')
                    break
                elif order_status == 56:
                    print(f'{stock_code}最近一笔交易已全部成交，不进入重下流程')
                    break
                else:
                    current_price = xtdata.get_full_tick([stock_code])[stock_code]['lastPrice']
                    price = current_price * 1.001 if latest_order['type'] == 23 else current_price * 0.999
                    info_dict = xtdata.get_instrument_detail(stock_code)
                    price = max(min(price, info_dict['UpStopPrice']), info_dict['DownStopPrice'])
                    print(f'{stock_code}委托价调整为市价偏离0.1%即{price}，准备重新下单')
    else:
        if type(account) is not str: raise TypeError('回测传入账户应当为str类型')
        position_value = {dt.m_strInstrumentID: dt.m_dMarketValue for dt in
                          get_trade_detail_data(account, 'stock', 'position')}
        position_usable_value = {dt.m_strInstrumentID: dt.m_dLastPrice * dt.m_nCanUseVolume for dt in
                                 get_trade_detail_data(account, 'stock', 'position')}
        total_value = get_trade_detail_data(account, 'stock', 'ACCOUNT')[0].m_dBalance
        if stock_code[:-3] in position_value.keys():
            current_weight = position_value[stock_code[:-3]] / total_value
            usable_weight = position_usable_value[stock_code[:-3]] / total_value
        else:
            current_weight = 0
            usable_weight = 0
        if current_weight == target_weight:
            return
        if current_weight < target_weight:
            passorder(
                23, 1113, account
                , stock_code, 5 if price == -1 else 11, price, target_weight - current_weight
                , 'order_target_weight', 1,
                datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                , contextinfo
            )
        else:
            if current_weight - target_weight < usable_weight:
                passorder(
                    24, 1113, account
                    , stock_code, 5 if price == -1 else 11, price, current_weight - target_weight
                    , 'order_target_weight', 1,
                    datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                    , contextinfo
                )
            else:
                passorder(
                    24, 1113, account
                    , stock_code, 5 if price == -1 else 11, price, usable_weight
                    , 'order_target_weight', 1,
                    datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                    , contextinfo
                )
    return


@try_except
def order_target_weight_final(stock_code: str, target_weight, account: Union[str, StockAccount],
                              contextinfo: ContextInfo,
                              order_id: str = '', price=-1, xt_trader: Union[None, xttrader.XtQuantTrader] = None,
                              quote_mode: str = 'backtest', quick_trade=True, order_count=1,
                              order_price_type='market_order') -> None:
    """
    将持仓调整至目标权重，没有该持仓会买入；权重为0时卖出全部持仓；可指定price参数，默认-1为市价单，只支持股票
    非快速下单，order_count默认为1，可不填
    按指定价下单，需要设为order_price_type='limit_order'
    order_price_type is in ['limit_order','limit_market_order','market_order']
    """
    if 1 < target_weight or target_weight < 0: raise ValueError("目标权重应当位于0到1之间（闭区间）")
    if quote_mode in ['realtime', 'all']:
        if type(account) is not StockAccount: raise TypeError("实盘/模拟盘传入账户应当为StockAccount类型")
        if type(xt_trader) is None: raise TypeError("实盘/模拟盘应当传入xt_trader参数，且类型为XtQuantTrader")
        remark = datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
        for i in range(1, order_count + 1):
            print(f'尝试下单-{i}代码:{stock_code}')

            current_weight = 0
            volume = 0
            usable_volume = 0
            current_price = \
                xtdata.get_full_tick([stock_code])[stock_code]['lastPrice']
            total_value = xt_trader.query_stock_asset(account).total_asset
            position_list = xt_trader.query_stock_positions(account)
            available_cash = xt_trader.query_stock_asset(account).cash
            # available_cash = available_cash * 0.9995  # 预留手续费

            for position in position_list:
                if position.stock_code == stock_code and position.volume > 0:
                    current_weight = position.volume * current_price / total_value
                    volume = position.volume
                    usable_volume = position.can_use_volume
                    break

            adjust_weight = (target_weight - current_weight)
            print(f'下单函数内：当前总资产{total_value}')
            print(f'调整数量{adjust_weight}, 目标数量{target_weight}, 当前数量{current_weight}')

            # if adjust_weight > 0.04:
            #     print(f'单笔委托超过风控阈值4%, 不下单')
            #     return

            if adjust_weight < 0:

                if current_weight > 0 and usable_volume > 0:

                    sell_volume = min((1 - target_weight / current_weight) * volume, usable_volume)

                    if stock_code[:2] in ['00', '60', '30']:
                        sell_volume = int(sell_volume // 100) * 100
                    elif stock_code[:2] == '68':
                        sell_volume = sell_volume if sell_volume >= 200 else usable_volume
                    elif stock_code[0] == '1':
                        sell_volume = int(sell_volume // 10) * 10
                    elif stock_code[0] in ['4', '8', '9']:
                        sell_volume = sell_volume if sell_volume >= 100 else usable_volume
                    else:
                        sell_volume = int(sell_volume // 100) * 100

                    if sell_volume > usable_volume:
                        warnings.warn(f'{stock_code}可用数量不足，将卖出所有可用持仓！')

                    current_price = xtdata.get_full_tick([stock_code])[stock_code]['lastPrice']

                    if price == -1 or order_price_type == 'market_order':
                        order_price = current_price
                    elif price != -1 and order_price_type == 'limit_order':
                        order_price = max(price, xtdata.get_instrument_detail(stock_code)['DownStopPrice'])
                    elif price != -1 and order_price_type == 'limit_market_order':
                        order_price = max(current_price * (1 - price),
                                          xtdata.get_instrument_detail(stock_code)['DownStopPrice'])
                    else:
                        order_price = current_price

                    print(f'卖出数量{sell_volume}, 下单价格{order_price}')
                    if sell_volume > 0:
                        resp = xt_trader.order_stock_async(account, stock_code, 24, sell_volume, 11,
                                                           order_price,
                                                           'order_target_weight', remark)
                else:
                    warnings.warn(f'{stock_code}无可用持仓！')
                    return

            elif adjust_weight > 0:
                if available_cash > total_value * 0.0005:

                    adjust_value = adjust_weight * total_value
                    current_price = xtdata.get_full_tick([stock_code])[stock_code]['lastPrice']
                    print('currentsss', stock_code, current_price)

                    if price == -1 or order_price_type == 'market_order':
                        order_price = current_price
                    elif price != -1 and order_price_type == 'limit_order':
                        order_price = min(price, xtdata.get_instrument_detail(stock_code)['UpStopPrice'])
                    elif price != -1 and order_price_type == 'limit_market_order':
                        order_price = min(current_price * (1 + price),
                                          xtdata.get_instrument_detail(stock_code)['UpStopPrice'])
                    else:
                        order_price = current_price
                    print('order_price', order_price, current_price)
                    can_buy_volume = available_cash / order_price
                    buy_volume = min(adjust_value / order_price, can_buy_volume)

                    if stock_code[:2] in ['00', '60', '30']:
                        buy_volume = int(buy_volume // 100) * 100
                    elif stock_code[:2] == '68':
                        buy_volume = buy_volume if buy_volume >= 200 else 0
                    elif stock_code[0] == '1':
                        buy_volume = int(buy_volume // 10) * 10
                    elif stock_code[0] in ['4', '8', '9']:
                        buy_volume = buy_volume if buy_volume >= 100 else 0
                    else:
                        buy_volume = int(buy_volume // 100) * 100

                    if buy_volume > can_buy_volume:
                        warnings.warn(f'{stock_code}可用现金不足，用剩余现金全部买入！')

                    print(f'买入数量{buy_volume}, 下单价格{order_price}')
                    if buy_volume > 0:
                        resp = xt_trader.order_stock_async(account, stock_code, 23, buy_volume, 11,
                                                       order_price,
                                                       'order_target_weight', remark)
                else:
                    warnings.warn(f'{stock_code}无可用现金！')
                    return

            if not quick_trade:
                break
            # if i == 10:
            #     print(f'{stock_code}暂未成交，维持最后委托')
            #     break
            time.sleep(1)
            orders = [
                {'status': order.order_status, 'remark': order.order_remark, 'time': order.order_time,
                 'sysid': order.order_sysid, 'id': order.order_id}
                for order in
                xt_trader.query_stock_orders(account) if order.order_remark == remark]
            if len(orders) == 0:
                print(f'{stock_code}今日无委托任务')
                break
            orders = sorted(orders, key=lambda x: x['time'])
            print(orders)
            latest_order = orders[-1]
            if latest_order['status'] == 56:
                break
            else:
                resp = None
                if latest_order['sysid'] is not None:
                    resp = xt_trader.cancel_order_stock_sysid_async(account, 0 if 'SH' in stock_code else 1,
                                                                    latest_order['sysid'])
                elif latest_order['id'] is not None:
                    resp = xt_trader.cancel_order_stock_async(account, latest_order['id'])
                else:
                    print(f'{stock_code}查询不到委托，无法进行撤单重下')
                    break
                for i in range(1, 6):
                    if resp == -1:
                        print(f'{stock_code}撤单暂未成功_{i}')
                        time.sleep(0.2)
                    elif resp is None:
                        print(f'{stock_code}撤单暂未响应_{i}')
                        time.sleep(0.2)
                    else:
                        print(f'{stock_code}撤单成功')
                        break
                if resp == -1:
                    print(f'{stock_code}撤单失败, 无法进行重下，维持原委托')
                    break
                elif resp is None:
                    print(f'{stock_code}撤单无响应，无法进行重下，维持原委托')
                    break
                else:
                    print(f'{stock_code}委托价调整为市价，准备重新下单')
                    price = -1
    else:
        if type(account) is not str: raise TypeError('回测传入账户应当为str类型')
        position_value = {dt.m_strInstrumentID: dt.m_dMarketValue for dt in
                          get_trade_detail_data(account, 'stock', 'position')}
        total_value = get_trade_detail_data(account, 'stock', 'ACCOUNT')[0].m_dBalance
        if stock_code[:-3] in position_value.keys():
            current_weight = position_value[stock_code[:-3]] / total_value
        else:
            current_weight = 0
        if current_weight < target_weight:
            passorder(
                23, 1113, account
                , stock_code, 5 if price == -1 else 11, price, target_weight - current_weight
                , 'order_target_weight', 1,
                datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                , contextinfo
            )
        else:
            passorder(
                24, 1113, account
                , stock_code, 5 if price == -1 else 11, price, current_weight - target_weight
                , 'order_target_weight', 1,
                datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                , contextinfo
            )
    return

def order_target_weight_final_realtime(stock_code: str, target_weight, account: Union[str, StockAccount],
                              contextinfo: ContextInfo,
                              order_id: str = '', price=-1, xt_trader: Union[None, xttrader.XtQuantTrader] = None,
                              quote_mode: str = 'backtest', quick_trade=True, order_count=1,
                              order_price_type='market_order') -> None:
    """
    单笔委托超过风控阈值4%, 不下单
    将持仓调整至目标权重，没有该持仓会买入；权重为0时卖出全部持仓；可指定price参数，默认-1为市价单，只支持股票
    非快速下单，order_count默认为1，可不填
    按指定价下单，需要设为order_price_type='limit_order'
    order_price_type is in ['limit_order','limit_market_order','market_order']
    """
    if 1 < target_weight or target_weight < 0: raise ValueError("目标权重应当位于0到1之间（闭区间）")
    if quote_mode in ['realtime', 'all']:
        if type(account) is not StockAccount: raise TypeError("实盘/模拟盘传入账户应当为StockAccount类型")
        if type(xt_trader) is None: raise TypeError("实盘/模拟盘应当传入xt_trader参数，且类型为XtQuantTrader")
        remark = datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
        for i in range(1, order_count + 1):
            print(f'尝试下单-{i}代码:{stock_code}')

            current_weight = 0
            volume = 0
            usable_volume = 0
            current_price = \
                xtdata.get_full_tick([stock_code])[stock_code]['lastPrice']
            total_value = xt_trader.query_stock_asset(account).total_asset
            # total_value = 1050000
            position_list = xt_trader.query_stock_positions(account)
            available_cash = xt_trader.query_stock_asset(account).cash
            # available_cash = available_cash * 0.9995  # 预留手续费

            for position in position_list:
                if position.stock_code == stock_code and position.volume > 0:
                    current_weight = position.volume * current_price / total_value
                    volume = position.volume
                    usable_volume = position.can_use_volume
                    break

            adjust_weight = (target_weight - current_weight)
            print(f'下单函数内：当前总资产{total_value}')
            print(f'调整数量{adjust_weight}, 目标数量{target_weight}, 当前数量{current_weight}')

            if adjust_weight > 0.04:
                print(f'单笔委托超过风控阈值4%, 不下单')
                return

            if adjust_weight < 0:

                if current_weight > 0 and usable_volume > 0:

                    sell_volume = min((1 - target_weight / current_weight) * volume, usable_volume)

                    if stock_code[:2] in ['00', '60', '30']:
                        sell_volume = int(sell_volume // 100) * 100
                    elif stock_code[:2] == '68':
                        sell_volume = sell_volume if sell_volume >= 200 else usable_volume
                    elif stock_code[0] == '1':
                        sell_volume = int(sell_volume // 10) * 10
                    elif stock_code[0] in ['4', '8', '9']:
                        sell_volume = sell_volume if sell_volume >= 100 else usable_volume
                    else:
                        sell_volume = int(sell_volume // 100) * 100

                    if sell_volume > usable_volume:
                        warnings.warn(f'{stock_code}可用数量不足，将卖出所有可用持仓！')

                    current_price = xtdata.get_full_tick([stock_code])[stock_code]['lastPrice']

                    if price == -1 or order_price_type == 'market_order':
                        order_price = current_price
                    elif price != -1 and order_price_type == 'limit_order':
                        order_price = max(price, xtdata.get_instrument_detail(stock_code)['DownStopPrice'])
                    elif price != -1 and order_price_type == 'limit_market_order':
                        order_price = max(current_price * (1 - price),
                                          xtdata.get_instrument_detail(stock_code)['DownStopPrice'])
                    else:
                        order_price = current_price

                    print(f'卖出数量{sell_volume}, 下单价格{order_price}')
                    if sell_volume > 0:
                        resp = xt_trader.order_stock_async(account, stock_code, 24, sell_volume, 11,
                                                           order_price,
                                                           'order_target_weight', remark)
                else:
                    warnings.warn(f'{stock_code}无可用持仓！')
                    return

            elif adjust_weight > 0:
                if available_cash > total_value * 0.0005:

                    adjust_value = adjust_weight * total_value
                    current_price = xtdata.get_full_tick([stock_code])[stock_code]['lastPrice']

                    if price == -1 or order_price_type == 'market_order':
                        order_price = current_price
                    elif price != -1 and order_price_type == 'limit_order':
                        order_price = min(price, xtdata.get_instrument_detail(stock_code)['UpStopPrice'])
                    elif price != -1 and order_price_type == 'limit_market_order':
                        order_price = min(current_price * (1 + price),
                                          xtdata.get_instrument_detail(stock_code)['UpStopPrice'])
                    else:
                        order_price = current_price

                    can_buy_volume = available_cash / order_price
                    buy_volume = min(adjust_value / order_price, can_buy_volume)

                    if stock_code[:2] in ['00', '60', '30']:
                        buy_volume = int(buy_volume // 100) * 100
                    elif stock_code[:2] == '68':
                        buy_volume = buy_volume if buy_volume >= 200 else 0
                    elif stock_code[0] == '1':
                        buy_volume = int(buy_volume // 10) * 10
                    elif stock_code[0] in ['4', '8', '9']:
                        buy_volume = buy_volume if buy_volume >= 100 else 0
                    else:
                        buy_volume = int(buy_volume // 100) * 100

                    if buy_volume > can_buy_volume:
                        warnings.warn(f'{stock_code}可用现金不足，用剩余现金全部买入！')

                    print(f'买入数量{buy_volume}, 下单价格{order_price}')
                    if buy_volume > 0:
                        resp = xt_trader.order_stock_async(account, stock_code, 23, buy_volume, 11,
                                                       order_price,
                                                       'order_target_weight', remark)
                else:
                    warnings.warn(f'{stock_code}无可用现金！')
                    return

            if not quick_trade:
                break
            # if i == 10:
            #     print(f'{stock_code}暂未成交，维持最后委托')
            #     break
            time.sleep(1)
            orders = [
                {'status': order.order_status, 'remark': order.order_remark, 'time': order.order_time,
                 'sysid': order.order_sysid, 'id': order.order_id}
                for order in
                xt_trader.query_stock_orders(account) if order.order_remark == remark]
            if len(orders) == 0:
                print(f'{stock_code}今日无委托任务')
                break
            orders = sorted(orders, key=lambda x: x['time'])
            print(orders)
            latest_order = orders[-1]
            if latest_order['status'] == 56:
                break
            else:
                resp = None
                if latest_order['sysid'] is not None:
                    resp = xt_trader.cancel_order_stock_sysid_async(account, 0 if 'SH' in stock_code else 1,
                                                                    latest_order['sysid'])
                elif latest_order['id'] is not None:
                    resp = xt_trader.cancel_order_stock_async(account, latest_order['id'])
                else:
                    print(f'{stock_code}查询不到委托，无法进行撤单重下')
                    break
                for i in range(1, 6):
                    if resp == -1:
                        print(f'{stock_code}撤单暂未成功_{i}')
                        time.sleep(0.2)
                    elif resp is None:
                        print(f'{stock_code}撤单暂未响应_{i}')
                        time.sleep(0.2)
                    else:
                        print(f'{stock_code}撤单成功')
                        break
                if resp == -1:
                    print(f'{stock_code}撤单失败, 无法进行重下，维持原委托')
                    break
                elif resp is None:
                    print(f'{stock_code}撤单无响应，无法进行重下，维持原委托')
                    break
                else:
                    print(f'{stock_code}委托价调整为市价，准备重新下单')
                    price = -1
    else:
        if type(account) is not str: raise TypeError('回测传入账户应当为str类型')
        position_value = {dt.m_strInstrumentID: dt.m_dMarketValue for dt in
                          get_trade_detail_data(account, 'stock', 'position')}
        total_value = get_trade_detail_data(account, 'stock', 'ACCOUNT')[0].m_dBalance
        print('get_trade_detail_data:total_value返回值', total_value)
        if stock_code[:-3] in position_value.keys():
            current_weight = position_value[stock_code[:-3]] / total_value
            print('a-get_trade_detail_data:total_value返回值', total_value)
        else:
            current_weight = 0
        if current_weight < target_weight:
            passorder(
                23, 1113, account
                , stock_code, 5 if price == -1 else 11, price, target_weight - current_weight
                , 'order_target_weight', 1,
                datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                , contextinfo
            )
        else:
            passorder(
                24, 1113, account
                , stock_code, 5 if price == -1 else 11, price, current_weight - target_weight
                , 'order_target_weight', 1,
                datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                , contextinfo
            )
    return

@try_except
def order_volume(stock_code: str, volume: int, account: Union[str, StockAccount], contextinfo: ContextInfo,
                 order_id: str = '',
                 price=-1, xt_trader: Union[None, xttrader.XtQuantTrader] = None,
                 quote_mode: str = 'backtest') -> None:
    '''
    买入或卖出指定数量的标的，为负数时卖出，只支持股票
    :param stock_code: 标的代码
    :param volume: 下单数量（股）
    :param account: 账户
    :param contextinfo: 含有k线信息和接口的上下文对象
    :param order_id: 订单号
    :param price: 委托价格
    :param xt_trader: API实例对象
    :param quote_mode: 模式（回测/模拟盘/实盘）
    :return: None
    '''
    if quote_mode in ['realtime', 'all']:
        if type(account) is not StockAccount: raise TypeError("实盘/模拟盘传入账户应当为StockAccount类型")
        if type(xt_trader) is None: raise TypeError("实盘/模拟盘应当传入xt_trader参数，且类型为XtQuantTrader")
        if volume > 0:
            resp = xt_trader.order_stock_async(account, stock_code, 23, volume, 5 if price == -1 else 11, price,
                                               'order_target_value', datetime.datetime.now().strftime(
                    '%Y%m%d%H%M%S委托单') if order_id == '' else order_id)
        elif volume < 0:
            usable_vol = 0
            position_list = xt_trader.query_stock_positions(account)
            for position in position_list:
                if position.stock_code == stock_code and position.volume > 0:
                    usable_vol = position.can_use_volume
                    break
            if usable_vol < abs(volume):
                warnings.warn(f'{stock_code}可用数量不足，将卖出所有持仓')
                volume = usable_vol
            resp = xt_trader.order_stock_async(account, stock_code, 24, -volume, 5 if price == -1 else 11, price,
                                               'order_target_value', datetime.datetime.now().strftime(
                    '%Y%m%d%H%M%S委托单') if order_id == '' else order_id)
    else:
        if type(account) is not str: raise TypeError('回测传入账户应当为str类型')
        if volume == 0:
            return
        if volume > 0:
            passorder(
                23, 1101, account
                , stock_code, 5 if price == -1 else 11, price, volume
                , 'order_volume', 1,
                datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                , contextinfo
            )
        else:
            position_volume = {dt.m_strInstrumentID: dt.m_nVolume for dt in
                               get_trade_detail_data(account, 'stock', 'position')}
            position_usable_volume = {dt.m_strInstrumentID: dt.m_nCanUseVolume for dt in
                                      get_trade_detail_data(account, 'stock', 'position')}
            if stock_code[:-3] in position_volume.keys():
                usable_volume = position_usable_volume[stock_code[:-3]]
            else:
                usable_volume = 0
            if usable_volume < abs(volume):
                warnings.warn(
                    f'当前账户{account} {stock_code}持仓可用数量为{usable_volume}，小于欲卖出的数量{abs(volume)}，将全部卖出',
                    UserWarning)
                passorder(
                    24, 1101, account
                    , stock_code, 5 if price == -1 else 11, price, usable_volume
                    , 'order_volume', 1,
                    datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                    , contextinfo
                )
            else:
                passorder(
                    24, 1101, account
                    , stock_code, 5 if price == -1 else 11, price, abs(volume)
                    , 'order_volume', 1,
                    datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                    , contextinfo
                )
    return


@try_except
def order_target_contract(future_code: str, volume: int, account: Union[str, StockAccount], contextinfo: ContextInfo,
                          order_id: str = '',
                          price=-1, xt_trader: Union[None, xttrader.XtQuantTrader] = None,
                          quote_mode: str = 'backtest', quick_trade=True):
    """
    期货操作，调整至目标合约份数，负数表示空头操作，正数表示多头操作
    :param future_code: 标的代码
    :param volume: 下单数量（手）
    :param account: 账户
    :param contextinfo: 含有k线信息和接口的上下文对象
    :param order_id: 订单号
    :param price: 委托价格
    :param xt_trader: API实例对象
    :param quote_mode: 模式（回测/模拟盘/实盘）
    :param quick_trade: 是否快速成交
    :return: None
    """
    if quote_mode in ['realtime', 'all']:
        if type(account) is not StockAccount: raise TypeError("实盘/模拟盘传入账户应当为StockAccount类型")
        if type(xt_trader) is None: raise TypeError("实盘/模拟盘应当传入xt_trader参数，且类型为XtQuantTrader")
        remark = datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
        for i in range(1, 11):
            print(f'尝试下单 {i}代码:{future_code}')
            position_list = xt_trader.query_position_statistics(account)
            current_volume = 0
            current_direction = 0
            for position in position_list:
                if position.instrument_id == future_code.split('.')[0]:
                    current_volume = position.position
                    current_direction = 1 if position.direction == 48 else -1
                    break
            current = current_volume * current_direction
            cash = xt_trader.query_stock_asset(account).cash
            price = xtdata.get_full_tick([future_code])[future_code]['lastPrice']
            info_dict = xtdata.get_instrument_detail(future_code)
            LongMargin = info_dict['LongMarginRatio'] * price * info_dict['VolumeMultiple']
            ShortMargin = info_dict['ShortMarginRatio'] * price * info_dict['VolumeMultiple']

            if current == 0: #无持仓
                resp = xt_trader.order_stock_async(account, future_code, 0 if volume > 0 else 3, abs(volume),
                                                   5 if price == -1 else 11, price, 'order_target_contract',
                                                   remark)
            elif current * volume > 0: #持仓和目标方向相同
                if volume > 0: #做多
                    if volume - current > 0: #目标多单大于持仓多单
                        adjust_volume = volume - current
                        if LongMargin * adjust_volume > cash:
                            adjust_volume = cash // LongMargin
                            warnings.warn(f'{future_code}可用资金不足，将剩余资金全部开多。')
                        resp = xt_trader.order_stock_async(account, future_code, 0, adjust_volume,
                                                           5 if price == -1 else 11, price
                                                           , 'order_target_contract',
                                                           remark)
                    elif volume - current < 0: #目标多单小于持仓多单
                        resp = xt_trader.order_stock_async(account, future_code, 7, current - volume,
                                                           5 if price == -1 else 11, price,
                                                           'order_target_contract',
                                                           remark)
                elif volume < 0: #做空
                    if volume - current > 0: #目标空单小于持仓空单
                        resp = xt_trader.order_stock_async(account, future_code, 9, abs(volume - current),
                                                           5 if price == -1 else 11, price,
                                                           'order_target_contract',
                                                           remark)
                    elif volume - current < 0: #目标空单大于持仓空单
                        adjust_volume = abs(volume - current)
                        if ShortMargin * adjust_volume > cash:
                            adjust_volume = cash // ShortMargin
                            warnings.warn(f'{future_code}可用资金不足，将剩余资金全部开空。')
                        resp = xt_trader.order_stock_async(account, future_code, 3, adjust_volume,
                                                           5 if price == -1 else 11, price,
                                                           'order_target_contract',
                                                           remark)
            elif current * volume <= 0: #持仓与目标方向不用（平多开空/平空开多）
                if current < 0: #平掉持仓空单
                    resp = xt_trader.order_stock_async(account, future_code, 9, abs(current), 5 if price == -1 else 11,
                                                       price,
                                                       'order_target_contract',
                                                       remark)
                else: #平掉持仓多单
                    resp = xt_trader.order_stock_async(account, future_code, 7, abs(current), 5 if price == -1 else 11,
                                                       price,
                                                       'order_target_contract',
                                                       remark)
                if volume > 0: #开多
                    if LongMargin * volume > cash + ShortMargin * current:
                        volume = cash // LongMargin
                        warnings.warn(f'{future_code}可用资金不足，将资金全部开多。')
                    resp = xt_trader.order_stock_async(account, future_code, 0, abs(volume), 5 if price == -1 else 11,
                                                       price,
                                                       'order_target_contract',
                                                       remark)
                elif volume < 0: #开空
                    if ShortMargin * abs(volume) > cash + LongMargin * current:
                        volume = - cash // LongMargin
                        warnings.warn(f'{future_code}可用资金不足，将资金全部开空。')
                    resp = xt_trader.order_stock_async(account, future_code, 3, abs(volume), 5 if price == -1 else 11,
                                                       price,
                                                       'order_target_contract',
                                                       remark)
            if not quick_trade:
                break
            if i == 10:
                print(f'{future_code}暂未成交，维持最后委托')
                break
            time.sleep(1)
            orders = [{'status': order.order_status, 'remark': order.order_remark, 'time': order.order_time,
                       'sysid': order.order_sysid, 'id': order.order_id, 'direction': order.direction} for order in
                      xt_trader.query_stock_orders(account) if order.order_remark == remark]
            if len(orders) == 0:
                print(f'{future_code}此备注（{remark}）无委托任务')
                break
            orders = sorted(orders, key=lambda x: x['time'])
            print(orders)
            latest_order = orders[-1]
            if latest_order['status'] == 56:
                break
            else:
                resp = None
                if latest_order['sysid'] is not None:
                    resp = xt_trader.cancel_order_stock_sysid_async(account, 0, latest_order['sysid'])
                elif latest_order['id'] is not None:
                    resp = xt_trader.cancel_order_stock_async(account, latest_order['id'])
                else:
                    print(f'{future_code}查询不到委托，无法进行撤单重下')
                    break
                for i in range(1, 6):
                    if resp == -1:
                        print(f'{future_code}撤单暂未成功_{i}')
                        time.sleep(0.5)
                    elif resp is None:
                        print(f'{future_code}撤单暂未响应_{i}')
                        time.sleep(0.5)
                    else:
                        print(f'{future_code}撤单成功')
                        break
                new_orders = [{'status': order.order_status, 'remark': order.order_remark, 'time': order.order_time}
                              for order in xt_trader.query_stock_orders(account) if order.order_remark == remark]
                order_status = sorted(new_orders, key=lambda x: x['time'], reverse=False)[-1]['status']
                if resp == -1:
                    print(f'{future_code}撤单失败, 无法进行重下，维持原委托')
                    break
                elif resp is None:
                    print(f'{future_code}撤单无响应，无法进行重下，维持原委托')
                    break
                elif order_status == 56:
                    print(f'{future_code}最近一笔交易已全部成交，不进入重下流程')
                    break
                else:
                    current_price = xtdata.get_full_tick([future_code])[future_code]['lastPrice']
                    price = current_price * 1.0005 if latest_order['direction'] == 48 else current_price * 0.9995
                    print(f'{future_code}委托价调整为市价偏离0.05%即{price}，准备重新下单')
    else:
        if type(account) is not str: raise TypeError('回测传入账户应当为str类型')
        current_volume = {dt.m_strInstrumentID: dt.m_nVolume for dt in
                          get_trade_detail_data(account, 'future', 'position')}
        current_direction = {dt.m_strInstrumentID: 1 if dt.m_nDirection == 48 else -1 for dt in
                             get_trade_detail_data(account, 'future', 'position')}
        if future_code.split('.')[0] in current_volume.keys():
            current = current_volume[future_code.split('.')[0]] * current_direction[future_code.split('.')[0]]
            if current * volume <= 0:
                if current < 0:
                    passorder(
                        9, 1101, account
                        , future_code, 5 if price == -1 else 11, price, abs(current)
                        , 'order_target_contract', 1,
                        datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                        , contextinfo
                    )
                else:
                    passorder(
                        7, 1101, account
                        , future_code, 5 if price == -1 else 11, price, current
                        , 'order_target_contract', 1,
                        datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                        , contextinfo
                    )
                if volume > 0:
                    passorder(
                        0, 1101, account
                        , future_code, 5 if price == -1 else 11, price, volume
                        , 'order_target_contract', 1,
                        datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                        , contextinfo
                    )
                elif volume < 0:
                    passorder(
                        3, 1101, account
                        , future_code, 5 if price == -1 else 11, price, abs(volume)
                        , 'order_target_contract', 1,
                        datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                        , contextinfo
                    )
            elif current * volume > 0:
                if volume > 0:
                    if volume - current > 0:
                        passorder(
                            0, 1101, account
                            , future_code, 5 if price == -1 else 11, price, volume - current
                            , 'order_target_contract', 1,
                            datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                            , contextinfo
                        )
                    elif volume - current < 0:
                        passorder(
                            7, 1101, account
                            , future_code, 5 if price == -1 else 11, price, current - volume
                            , 'order_target_contract', 1,
                            datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                            , contextinfo
                        )
                elif volume < 0:
                    if volume - current > 0:
                        passorder(
                            9, 1101, account
                            , future_code, 5 if price == -1 else 11, price, abs(volume - current)
                            , 'order_target_contract', 1,
                            datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                            , contextinfo
                        )
                    elif volume - current < 0:
                        passorder(
                            3, 1101, account
                            , future_code, 5 if price == -1 else 11, price, abs(volume - current)
                            , 'order_target_contract', 1,
                            datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                            , contextinfo
                        )

        else:
            if volume > 0:
                passorder(
                    0, 1101, account
                    , future_code, 5 if price == -1 else 11, price, volume
                    , 'order_target_contract', 1,
                    datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                    , contextinfo
                )
            elif volume < 0:
                passorder(
                    3, 1101, account
                    , future_code, 5 if price == -1 else 11, price, abs(volume)
                    , 'order_target_contract', 1,
                    datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                    , contextinfo
                )
    return


@try_except
def buy_contract(future_code: str, volume: int, account: Union[str, StockAccount], contextinfo: ContextInfo,
                 order_id: str = '',
                 price=-1, xt_trader: Union[None, xttrader.XtQuantTrader] = None,
                 quote_mode: str = 'backtest'):
    """
    买入合约，正数开多，负数开空
    :param future_code: 标的代码
    :param volume: 下单数量（手）
    :param account: 账户
    :param contextinfo: 含有k线信息和接口的上下文对象
    :param order_id: 订单号
    :param price: 委托价格
    :param xt_trader: API实例对象
    :param quote_mode: 模式（回测/模拟盘/实盘）
    :return: None
    """
    if quote_mode in ['realtime', 'all']:
        if type(account) is not StockAccount: raise TypeError("实盘/模拟盘传入账户应当为StockAccount类型")
        if type(xt_trader) is None: raise TypeError("实盘/模拟盘应当传入xt_trader参数，且类型为XtQuantTrader")
        if volume > 0:
            xt_trader.order_stock_async(account, future_code, 0, volume, 5 if price == -1 else 11, price, 'buy_volume',
                                        datetime.datetime.now().strftime(
                                            '%Y%m%d%H%M%S委托单') if order_id == '' else order_id)
        elif volume < 0:
            xt_trader.order_stock_async(account, future_code, 3, abs(volume), 5 if price == -1 else 11, price,
                                        'buy_volume',
                                        datetime.datetime.now().strftime(
                                            '%Y%m%d%H%M%S委托单') if order_id == '' else order_id)
    else:
        if type(account) is not str: raise TypeError('回测传入账户应当为str类型')
        if volume > 0:
            passorder(
                0, 1101, account
                , future_code, 5 if price == -1 else 11, price, volume
                , 'buy_volume', 1,
                datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                , contextinfo
            )
        elif volume < 0:
            passorder(
                3, 1101, account
                , future_code, 5 if price == -1 else 11, price, abs(volume)
                , 'buy_volume', 1,
                datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                , contextinfo
            )
    return


@try_except
def sell_contract(future_code: str, volume: int, account: Union[str, StockAccount], contextinfo: ContextInfo,
                  order_id: str = '',
                  price=-1, xt_trader: Union[None, xttrader.XtQuantTrader] = None,
                  quote_mode: str = 'backtest'):
    """
    卖出合约，正数平多，负数平空
    :param future_code: 标的代码
    :param volume: 下单数量（手）
    :param account: 账户
    :param contextinfo: 含有k线信息和接口的上下文对象
    :param order_id: 订单号
    :param price: 委托价格
    :param xt_trader: API实例对象
    :param quote_mode: 模式（回测/模拟盘/实盘）
    :return: None
    """
    if quote_mode in ['realtime', 'all']:
        if type(account) is not StockAccount: raise TypeError("实盘/模拟盘传入账户应当为StockAccount类型")
        if type(xt_trader) is None: raise TypeError("实盘/模拟盘应当传入xt_trader参数，且类型为XtQuantTrader")
        if volume > 0:
            xt_trader.order_stock_async(account, future_code, 7, volume, 5 if price == -1 else 11, price, 'buy_volume',
                                        datetime.datetime.now().strftime(
                                            '%Y%m%d%H%M%S委托单') if order_id == '' else order_id)
        elif volume < 0:
            xt_trader.order_stock_async(account, future_code, 9, abs(volume), 5 if price == -1 else 11, price,
                                        'buy_volume',
                                        datetime.datetime.now().strftime(
                                            '%Y%m%d%H%M%S委托单') if order_id == '' else order_id)
    else:
        if type(account) is not str: raise TypeError('回测传入账户应当为str类型')
        if volume > 0:
            passorder(
                7, 1101, account
                , future_code, 5 if price == -1 else 11, price, volume
                , 'buy_volume', 1,
                datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                , contextinfo
            )
        elif volume < 0:
            passorder(
                9, 1101, account
                , future_code, 5 if price == -1 else 11, price, abs(volume)
                , 'buy_volume', 1,
                datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                , contextinfo
            )
    return


@try_except
def buy_option(option_code: str, volume: int, account: Union[str, StockAccount], contextinfo: ContextInfo,
               order_id: str = '', price=-1, xt_trader: Union[None, xttrader.XtQuantTrader] = None,
               quote_mode: str = 'backtest'):
    """
    买入期权
    """
    if volume < 0: raise ValueError('买入期权数量应大于0')
    if quote_mode in ['realtime', 'all']:
        if type(account) is not StockAccount: raise TypeError("实盘/模拟盘传入账户应当为StockAccount类型")
        if type(xt_trader) is None: raise TypeError("实盘/模拟盘应当传入xt_trader参数，且类型为XtQuantTrader")
        if option_code.upper().split('.')[1] in ['IF', 'SF', 'DF', 'INE', 'GF']:
            xt_trader.order_stock_async(account, option_code, xtconstant.FUTURE_OPEN_LONG, volume,
                                        5 if price == -1 else 11, price, 'buy_option',
                                        datetime.datetime.now().strftime(
                                            '%Y%m%d%H%M%S委托单') if order_id == '' else order_id)
        else:
            xt_trader.order_stock_async(account, option_code, xtconstant.STOCK_OPTION_BUY_OPEN, volume,
                                        5 if price == -1 else 11, price, 'buy_option',
                                        datetime.datetime.now().strftime(
                                            '%Y%m%d%H%M%S委托单') if order_id == '' else order_id)
    else:
        if type(account) is not str: raise TypeError('回测传入账户应当为str类型')
        if option_code.upper().split('.')[1] in ['IF', 'SF', 'DF', 'INE', 'GF']:
            passorder(xtconstant.FUTURE_OPEN_LONG, 1101, account, option_code, 5 if price == -1 else 11, price, volume,
                      'buy_option', 1,
                      datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                      , contextinfo)
        else:
            passorder(xtconstant.STOCK_OPTION_BUY_OPEN, 1101, account, option_code, 5 if price == -1 else 11, price,
                      volume,
                      'buy_option', 1,
                      datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                      , contextinfo)


def sell_option(option_code: str, volume: int, account: Union[str, StockAccount], contextinfo: ContextInfo,
                order_id: str = '', price=-1, xt_trader: Union[None, xttrader.XtQuantTrader] = None,
                quote_mode: str = 'backtest'):
    """
    卖出期权
    """
    if volume < 0: raise ValueError('卖出期权数量应大于0')
    if quote_mode in ['realtime', 'all']:
        if type(account) is not StockAccount: raise TypeError("实盘/模拟盘传入账户应当为StockAccount类型")
        if type(xt_trader) is None: raise TypeError("实盘/模拟盘应当传入xt_trader参数，且类型为XtQuantTrader")
        if option_code.upper().split('.')[1] in ['IF', 'SF', 'DF', 'INE', 'GF']:
            xt_trader.order_stock_async(account, option_code, xtconstant.FUTURE_OPEN_SHORT, volume,
                                        5 if price == -1 else 11, price, 'sell_option',
                                        datetime.datetime.now().strftime(
                                            '%Y%m%d%H%M%S委托单') if order_id == '' else order_id)
        else:
            xt_trader.order_stock_async(account, option_code, xtconstant.STOCK_OPTION_SELL_OPEN, volume,
                                        5 if price == -1 else 11, price, 'sell_option',
                                        datetime.datetime.now().strftime(
                                            '%Y%m%d%H%M%S委托单') if order_id == '' else order_id)
    else:
        if type(account) is not str: raise TypeError('回测传入账户应当为str类型')
        if option_code.upper().split('.')[1] in ['IF', 'SF', 'DF', 'INE', 'GF']:
            passorder(xtconstant.FUTURE_OPEN_SHORT, 1101, account, option_code, 5 if price == -1 else 11, price, volume,
                      'sell_option', 1,
                      datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                      , contextinfo)
        else:
            passorder(xtconstant.STOCK_OPTION_SELL_OPEN, 1101, account, option_code, 5 if price == -1 else 11, price,
                      volume,
                      'sell_option', 1,
                      datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                      , contextinfo)


def exercise_option(option_code: str, option_type: str, volume: int, account: Union[str, StockAccount],
                    contextinfo: ContextInfo,
                    order_id: str = '', price=-1, xt_trader: Union[None, xttrader.XtQuantTrader] = None,
                    quote_mode: str = 'backtest'):
    """
    执行期权
    """
    if volume <= 0: raise ValueError('行权数量应大于0')
    option_type = option_type.upper()
    if option_type not in ['PUT', 'CALL']: raise ValueError('期权类型应为CALL(认购)或PUT(认沽)，不区分大小写。')
    if quote_mode in ['realtime', 'all']:
        if type(account) is not StockAccount: raise TypeError("实盘/模拟盘传入账户应当为StockAccount类型")
        if type(xt_trader) is None: raise TypeError("实盘/模拟盘应当传入xt_trader参数，且类型为XtQuantTrader")
        if option_code.upper().split('.')[1] in ['IF', 'SF', 'DF', 'INE', 'GF']:
            xt_trader.order_stock_async(account, option_code, xtconstant.OPTION_FUTURE_OPTION_EXERCISE, volume,
                                        5 if price == -1 else 11, price, 'exercise_option',
                                        datetime.datetime.now().strftime(
                                            '%Y%m%d%H%M%S委托单') if order_id == '' else order_id)
        else:
            xt_trader.order_stock_async(account, option_code,
                                        xtconstant.STOCK_OPTION_CALL_EXERCISE if option_type == 'CALL' else xtconstant.STOCK_OPTION_PUT_EXERCISE,
                                        volume,
                                        5 if price == -1 else 11, price, 'exercise_option',
                                        datetime.datetime.now().strftime(
                                            '%Y%m%d%H%M%S委托单') if order_id == '' else order_id)
    else:
        if type(account) is not str: raise TypeError('回测传入账户应当为str类型')
        if option_code.upper().split('.')[1] in ['IF', 'SF', 'DF', 'INE', 'GF']:
            passorder(xtconstant.OPTION_FUTURE_OPTION_EXERCISE, 1101, account, option_code, 5 if price == -1 else 11,
                      price, volume,
                      'exercise_option', 1,
                      datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                      , contextinfo)
        else:
            passorder(
                xtconstant.STOCK_OPTION_CALL_EXERCISE if option_type == 'CALL' else xtconstant.STOCK_OPTION_PUT_EXERCISE,
                1101, account, option_code, 5 if price == -1 else 11, price,
                volume,
                'exercise_option', 1,
                datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                , contextinfo)


def stock_clearance(account: Union[str, StockAccount], contextinfo: ContextInfo,
                       order_id: str = '', price: Union[int, float] = 0, xt_trader: Union[None, xttrader.XtQuantTrader] = None,
                       quote_mode: str = 'realtime', quick_trade=True) -> None:
    '''
    模拟盘输入stock_clearance(C.acc_s, C, xt_trader=C.xt_trader)，清仓
    '''
    holding_dict = {position.stock_code: position.market_value for position in
                    xt_trader.query_stock_positions(account) if position.market_value != 0}
    for stock in holding_dict.keys():
        try:
            current_price = xtdata.get_full_tick([stock])[stock]['lastPrice']
            p = current_price * 0.98 if price == 0 else price
            order_target_value(stock, 0, account, contextinfo, order_id=order_id, price=p, xt_trader=xt_trader,
                               quote_mode=quote_mode, quick_trade=quick_trade)
        except:
            print(f'{stock}清仓失败')
            continue
    return


"""
def cancel_reorder_entrustment(account: Union[str, StockAccount], contextinfo: ContextInfo,
                               xt_trader: Union[None, xttrader.XtQuantTrader] = None,) -> None:
    '''
    委托撤单后重新下单，以市价偏离0.1%的价格
    '''
    if type(account) is not StockAccount: raise TypeError("实盘/模拟盘传入账户应当为StockAccount类型")
    if type(xt_trader) is None: raise TypeError("实盘/模拟盘应当传入xt_trader参数，且类型为XtQuantTrader")
    orders = [
        {'status': order.order_status, 'remark': order.order_remark, 'time': order.order_time, 'sysid': order.order_sysid,
         'flag': order.offset_flag, 'code': order.stock_code, 'order_volume': order.order_volume,
         'traded_volume': order.traded_volume} for order in xt_trader.query_stock_orders(account)]
    cancel_dict = {}
    for order in orders:
        if order['status'] != 56:
            code = order['code']
            o_remark = order['remark']
            if order['flag'] == 48:
                cancel_dict[code] = order['order_volume'] - order['traded_volume']
            elif order['flag'] == 49:
                cancel_dict[code] = -(order['order_volume'] - order['traded_volume'])
            cancel_result = xt_trader.cancel_order_stock_sysid_async(account, 0 if 'SH' in code else 1, order['sysid'])
            if cancel_result >= 0:
                print(f'{code}撤单成功，所撤委托备注{o_remark}')
            else:
                print(f'{code}撤单失败，失败撤单委托备注{o_remark}')
    time.sleep(1)
    for code, volume in cancel_dict.items():
        current_price = 0
        current_price = xtdata.get_full_tick([code])[code]['lastPrice']
        available_cash = xt_trader.query_stock_asset(account).cash
        remark = datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单')
        # if volume % 100 != 0:
        #     volume = volume // 100 * 100
        if volume % 10 != 0:
            print(f'{code}数量不为整手，向下取整')
            volume = volume // 10 * 10
        if volume > 0:
            buy_price = current_price * 1.001
            if code[:2] in ['00', '60', '30']:
                can_buy_volume = int(available_cash / current_price) // 100 * 100
            elif code[:2] == '68':
                can_buy_volume = int(available_cash / current_price)
                can_buy_volume = can_buy_volume if can_buy_volume >= 200 else 0
            elif code[0] == '1':
                can_buy_volume = int(available_cash / current_price) // 10 * 10
            else:
                can_buy_volume = int(available_cash / current_price) // 100 * 100
            if can_buy_volume == 0:
                warnings.warn('资金可买数量为0')
                return
            if volume <= can_buy_volume:
                order_result = xt_trader.order_stock_async(account, code, order_type=23, order_volume=volume,
                                                           price_type=11, price=buy_price,
                                                           strategy_name='cancel_reorder_entrustment', order_remark=remark)
            else:
                warnings.warn(f'原下单数量{volume}，可用资金不足，将调整下单数量为{can_buy_volume}。')
                order_result = xt_trader.order_stock_async(account, code, order_type=23, order_volume=can_buy_volume,
                                                           price_type=11, price=buy_price,
                                                           strategy_name='cancel_reorder_entrustment', order_remark=remark)
        elif volume < 0:
            sell_price = current_price * 0.999
            volume = abs(volume)
            usable_vol = 0
            position_list = xt_trader.query_stock_positions(account)
            for position in position_list:
                if position.stock_code == code and position.volume > 0:
                    usable_vol = position.can_use_volume
                    break
            if usable_vol < volume:
                warnings.warn(f'{code}可用数量不足，将卖出所有持仓')
                volume = usable_vol
            order_result = xt_trader.order_stock_async(account, code, order_type=24, order_volume=volume,
                                                       price_type=11, price=sell_price,
                                                       strategy_name='cancel_reorder_entrustment', order_remark=remark)
    return
"""


def cancel_reorder_entrustment(account: Union[str, StockAccount],
                                     contextinfo: ContextInfo,
                                     xt_trader: Union[None, xttrader.XtQuantTrader] = None,
                                     order_cancel_interval: int = 30,
                                     buy_price_deviation: float = 0.001,
                                     sell_price_deviation: float = 0.001,
                                     cancel_execute_interval: int = 0.2,
                                     ) -> None:
    '''
    委托撤单后重新下单，以市价偏离0.1%的价格
    '''
    def custom_round(value, ndigits):
        if value >= 0:
            return math.floor(value * (10 ** ndigits) + 0.5) / (10 ** ndigits)
        else:
            return math.ceil(value * (10 ** ndigits) - 0.5) / (10 ** ndigits)
    now_datetime = datetime.datetime.now()
    if type(account) is not StockAccount: raise TypeError("实盘/模拟盘传入账户应当为StockAccount类型")
    if type(xt_trader) is None: raise TypeError("实盘/模拟盘应当传入xt_trader参数，且类型为XtQuantTrader")
    orders = [
        {'status': order.order_status, 'remark': order.order_remark, 'time': order.order_time,
         'sysid': order.order_sysid, 'id': order.order_id,
         'order_type': order.order_type, 'code': order.stock_code, 'order_volume': order.order_volume,
         'order_price': order.price,
         'traded_volume': order.traded_volume} for order in xt_trader.query_stock_orders(account) \
        if (now_datetime > datetime.datetime.fromtimestamp(order.order_time) + datetime.timedelta(
            seconds=order_cancel_interval)) and (
                       order.order_status == 48 or
                       order.order_status == 49 or
                       order.order_status == 50 or
                       order.order_status == 55)]
    cancel_dict = {}

    if orders is not None:
        for order in orders:
            code = order['code']
            if code == '511990.SH':
                print(f'當前標的{code},不撤單')
                return
            else:
                print(f'當前標的{code},可撤單')
            o_remark = order['remark']
            order['order_price'] = custom_round(order['order_price'], 2)
            if (order['order_price'] == xtdata.get_instrument_detail(code)['UpStopPrice'] and order['order_type'] == 23) \
                    or (order['order_price'] == xtdata.get_instrument_detail(code)['DownStopPrice'] and order[
                'order_type'] == 24):
                print(code, '------', '挂涨停的买单和挂跌停的卖单不撤！')
                # continue
            elif order['order_type'] == 23:
                cancel_order_volume = order['order_volume'] - order['traded_volume']
                print(code, '------', f'买单还有{cancel_order_volume}股未成交，准备撤单！')
            elif order['order_type'] == 24:
                cancel_order_volume = -(order['order_volume'] - order['traded_volume'])
                print(code, '------', f'卖单还有{-cancel_order_volume}股未成交，准备撤单！')
            else:
                continue

            if order['sysid'] is not None:
                cancel_result = xt_trader.cancel_order_stock_sysid_async(account, 0 if 'SH' in code else 1,
                                                                         order['sysid'])
                print(code, '正在撤单，方式1')

            elif order['id'] is not None:
                cancel_result = xt_trader.cancel_order_stock_async(account, order['id'])
                print(code, '正在撤单，方式2')

            time.sleep(cancel_execute_interval)

            if cancel_result >= 0:
                print(f'{code}撤单成功，回调{cancel_result}，所撤委托备注{o_remark}')
                cancel_dict[code] = cancel_order_volume
            else:
                print(f'{code}撤单失败，回调{cancel_result}，失败撤单委托备注{o_remark}')

        # order_stock_code_list = [order.stock_code for order in xt_trader.query_stock_orders(account) \
        #             if order.order_status== 48 or \
        #             order.order_status== 49 or \
        #             order.order_status== 50 or \
        #             order.order_status== 55]

        # position_list = [dt for dt in xt_trader.query_stock_positions(account) if dt.volume!=0.0]

        for code, volume in cancel_dict.items():
            current_price = 0
            current_price = xtdata.get_full_tick([code])[code]['lastPrice']
            available_cash = xt_trader.query_stock_asset(account).cash
            remark = datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单')
            if volume % 100 != 0:
                volume = volume // 100 * 100
                print(f'{code}数量不为整手，向下取整')
            if volume > 0:
                buy_price = min(current_price * (1.00 + buy_price_deviation),
                                xtdata.get_instrument_detail(code)['UpStopPrice'])
                can_buy_volume = int((available_cash / buy_price)) // 100 * 100
                if can_buy_volume == 0:
                    warnings.warn('资金可买数量为0')
                    return
                if volume <= can_buy_volume:
                    order_result = xt_trader.order_stock_async(account, code, order_type=23, order_volume=volume,
                                                               price_type=11, price=buy_price,
                                                               strategy_name='cancel_reorder_entrustment',
                                                               order_remark=remark)
                else:
                    warnings.warn(f'原下单数量{volume}，可用资金不足，将调整下单数量为{can_buy_volume}。')
                    order_result = xt_trader.order_stock_async(account, code, order_type=23,
                                                               order_volume=can_buy_volume,
                                                               price_type=11, price=buy_price,
                                                               strategy_name='cancel_reorder_entrustment',
                                                               order_remark=remark)
            elif volume < 0:
                sell_price = max(current_price * (1.00 - sell_price_deviation),
                                 xtdata.get_instrument_detail(code)['DownStopPrice'])
                volume = abs(volume)
                usable_vol = 0
                position_list = xt_trader.query_stock_positions(account)
                for position in position_list:
                    if position.stock_code == code and position.volume > 0:
                        usable_vol = position.can_use_volume
                        break
                if usable_vol < volume:
                    warnings.warn(f'{code}可用数量不足，将卖出所有持仓')
                    volume = usable_vol
                order_result = xt_trader.order_stock_async(account, code, order_type=24, order_volume=volume,
                                                           price_type=11, price=sell_price,
                                                           strategy_name='cancel_reorder_entrustment',
                                                           order_remark=remark)
    return

def cancel_reorder_entrustment_1(account: Union[str, StockAccount],
                                     contextinfo: ContextInfo,
                                     xt_trader: Union[None, xttrader.XtQuantTrader] = None,
                                     order_cancel_interval: int = 30,
                                     buy_price_deviation: float = 0.001,
                                     sell_price_deviation: float = 0.001,
                                     cancel_execute_interval: int = 0.2,
                                     ) -> None:
    '''
    委托撤单后重新下单，以市价偏离0.1%的价格
    '''
    def custom_round(value, ndigits):
        if value >= 0:
            return math.floor(value * (10 ** ndigits) + 0.5) / (10 ** ndigits)
        else:
            return math.ceil(value * (10 ** ndigits) - 0.5) / (10 ** ndigits)
    now_datetime = datetime.datetime.now()
    if type(account) is not StockAccount: raise TypeError("实盘/模拟盘传入账户应当为StockAccount类型")
    if type(xt_trader) is None: raise TypeError("实盘/模拟盘应当传入xt_trader参数，且类型为XtQuantTrader")
    orders = [
        {'status': order.order_status, 'remark': order.order_remark, 'time': order.order_time,
         'sysid': order.order_sysid, 'id': order.order_id,
         'order_type': order.order_type, 'code': order.stock_code, 'order_volume': order.order_volume,
         'order_price': order.price,
         'traded_volume': order.traded_volume} for order in xt_trader.query_stock_orders(account) \
        if (now_datetime > datetime.datetime.fromtimestamp(order.order_time) + datetime.timedelta(
            seconds=order_cancel_interval)) and (
                       order.order_status == 48 or
                       order.order_status == 49 or
                       order.order_status == 50 or
                       order.order_status == 55)]
    cancel_dict = {}

    if orders is not None:
        for order in orders:
            code = order['code']
            if code == '511990.SH':
                print(f'當前標的{code},不撤單')
                return
            else:
                print(f'當前標的{code},可撤單')
            o_remark = order['remark']
            order['order_price'] = custom_round(order['order_price'], 2)
            if (order['order_price'] == xtdata.get_instrument_detail(code)['UpStopPrice'] and order['order_type'] == 23) \
                    or (order['order_price'] == xtdata.get_instrument_detail(code)['DownStopPrice'] and order[
                'order_type'] == 24):
                print(code, '------', '挂涨停的买单和挂跌停的卖单不撤！')
                # continue
            elif order['order_type'] == 23:
                cancel_order_volume = order['order_volume'] - order['traded_volume']
                print(code, '------', f'买单还有{cancel_order_volume}股未成交，准备撤单！')
            elif order['order_type'] == 24:
                cancel_order_volume = -(order['order_volume'] - order['traded_volume'])
                print(code, '------', f'卖单还有{-cancel_order_volume}股未成交，准备撤单！')
            else:
                continue

            if order['sysid'] is not None:
                cancel_result = xt_trader.cancel_order_stock_sysid_async(account, 0 if 'SH' in code else 1,
                                                                         order['sysid'])
                print(code, '正在撤单，方式1')

            elif order['id'] is not None:
                cancel_result = xt_trader.cancel_order_stock_async(account, order['id'])
                print(code, '正在撤单，方式2')

            time.sleep(cancel_execute_interval)

            if cancel_result >= 0:
                print(f'{code}撤单成功，回调{cancel_result}，所撤委托备注{o_remark}')
                cancel_dict[code] = cancel_order_volume
            else:
                print(f'{code}撤单失败，回调{cancel_result}，失败撤单委托备注{o_remark}')

        # order_stock_code_list = [order.stock_code for order in xt_trader.query_stock_orders(account) \
        #             if order.order_status== 48 or \
        #             order.order_status== 49 or \
        #             order.order_status== 50 or \
        #             order.order_status== 55]

        # position_list = [dt for dt in xt_trader.query_stock_positions(account) if dt.volume!=0.0]

        for code, volume in cancel_dict.items():
            current_price = 0
            current_price = xtdata.get_full_tick([code])[code]['lastPrice']
            available_cash = xt_trader.query_stock_asset(account).cash
            remark = datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单')
            if volume % 100 != 0:
                volume = volume // 100 * 100
                print(f'{code}数量不为整手，向下取整')
            if volume > 0:
                buy_price = min((current_price + 0.1),
                                xtdata.get_instrument_detail(code)['UpStopPrice'])
                can_buy_volume = int((available_cash / buy_price)) // 100 * 100
                if can_buy_volume == 0:
                    warnings.warn('资金可买数量为0')
                    return
                if volume <= can_buy_volume:
                    order_result = xt_trader.order_stock_async(account, code, order_type=23, order_volume=volume,
                                                               price_type=11, price=buy_price,
                                                               strategy_name='cancel_reorder_entrustment',
                                                               order_remark=remark)
                else:
                    warnings.warn(f'原下单数量{volume}，可用资金不足，将调整下单数量为{can_buy_volume}。')
                    order_result = xt_trader.order_stock_async(account, code, order_type=23,
                                                               order_volume=can_buy_volume,
                                                               price_type=11, price=buy_price,
                                                               strategy_name='cancel_reorder_entrustment',
                                                               order_remark=remark)
            elif volume < 0:
                sell_price = max((current_price - 0.1),
                                 xtdata.get_instrument_detail(code)['DownStopPrice'])
                volume = abs(volume)
                usable_vol = 0
                position_list = xt_trader.query_stock_positions(account)
                for position in position_list:
                    if position.stock_code == code and position.volume > 0:
                        usable_vol = position.can_use_volume
                        break
                if usable_vol < volume:
                    warnings.warn(f'{code}可用数量不足，将卖出所有持仓')
                    volume = usable_vol
                order_result = xt_trader.order_stock_async(account, code, order_type=24, order_volume=volume,
                                                           price_type=11, price=sell_price,
                                                           strategy_name='cancel_reorder_entrustment',
                                                           order_remark=remark)
    return


def cancel_buy_order(account: Union[str, StockAccount],
                     contextinfo: ContextInfo,
                     xt_trader: Union[None, xttrader.XtQuantTrader] = None,
                     order_cancel_interval: int = 30,
                     cancel_execute_interval: int = 1,
                     ) -> None:
    def custom_round(value, ndigits):
        if value >= 0:
            return math.floor(value * (10 ** ndigits) + 0.5) / (10 ** ndigits)
        else:
            return math.ceil(value * (10 ** ndigits) - 0.5) / (10 ** ndigits)
    now_datetime = datetime.datetime.now()
    if type(account) is not StockAccount: raise TypeError("实盘/模拟盘传入账户应当为StockAccount类型")
    if type(xt_trader) is None: raise TypeError("实盘/模拟盘应当传入xt_trader参数，且类型为XtQuantTrader")
    orders = [
        {'status': order.order_status, 'remark': order.order_remark, 'time': order.order_time,
         'sysid': order.order_sysid, 'id': order.order_id,
         'order_type': order.order_type, 'code': order.stock_code, 'order_volume': order.order_volume,
         'order_price': order.price,
         'traded_volume': order.traded_volume} for order in xt_trader.query_stock_orders(account) \
        if (now_datetime > datetime.datetime.fromtimestamp(order.order_time) + datetime.timedelta(
            seconds=order_cancel_interval)) and (
                       order.order_status == 48 or
                       order.order_status == 49 or
                       order.order_status == 50 or
                       order.order_status == 55)]

    if orders is not None:
        for order in orders:
            code = order['code']
            o_remark = order['remark']
            order['order_price'] = custom_round(order['order_price'], 2)
            if (order['order_price'] == xtdata.get_instrument_detail(code)['DownStopPrice'] and order[
                'order_type'] == 24):
                print(code, '------', '挂跌停的卖单不撤！')
                continue
            elif order['order_type'] == 23:
                cancel_order_volume = order['order_volume'] - order['traded_volume']
                print(code, '------', f'买单还有{cancel_order_volume}股未成交，准备撤单')
            else:
                continue

            if order['sysid'] is not None:
                cancel_result = xt_trader.cancel_order_stock_sysid_async(account, 0 if 'SH' in code else 1,
                                                                         order['sysid'])
                print(code, '正在撤单，方式1')
            elif order['id'] is not None:
                cancel_result = xt_trader.cancel_order_stock_async(account, order['id'])
                print(code, '正在撤单，方式2')
            if cancel_result >= 0:
                print(f'{code}撤单成功，所撤委托备注{o_remark}')
            else:
                print(f'{code}撤单失败，失败撤单委托备注{o_remark}')

        # time.sleep(cancel_execute_interval)

    return


def cancel_reorder_entrustment_stock_final(account: Union[str, StockAccount],
                                           contextinfo: ContextInfo,
                                           xt_trader: Union[None, xttrader.XtQuantTrader] = None,
                                           order_cancel_interval: int = 30,
                                           buy_price_deviation: float = 0.001,
                                           sell_price_deviation: float = 0.001,
                                           cancel_execute_interval: int = 1,
                                           ) -> None:
    '''
    委托撤单后重新下单，以市价偏离0.1%的价格
    '''
    def custom_round(value, ndigits):
        if value >= 0:
            return math.floor(value * (10 ** ndigits) + 0.5) / (10 ** ndigits)
        else:
            return math.ceil(value * (10 ** ndigits) - 0.5) / (10 ** ndigits)
    now_datetime = datetime.datetime.now()
    now = now_datetime.strftime("%H:%M:%S")
    if type(account) is not StockAccount: raise TypeError("实盘/模拟盘传入账户应当为StockAccount类型")
    if type(xt_trader) is None: raise TypeError("实盘/模拟盘应当传入xt_trader参数，且类型为XtQuantTrader")
    orders = [
        {'status': order.order_status, 'remark': order.order_remark, 'time': order.order_time,
         'sysid': order.order_sysid, 'id': order.order_id,
         'order_type': order.order_type, 'code': order.stock_code, 'order_volume': order.order_volume,
         'order_price': order.price,
         'traded_volume': order.traded_volume} for order in xt_trader.query_stock_orders(account) \
        if (now_datetime > datetime.datetime.fromtimestamp(order.order_time) + datetime.timedelta(
            seconds=order_cancel_interval)) and ( \
                       order.order_status == 48 or \
                       order.order_status == 49 or \
                       order.order_status == 50 or \
                       order.order_status == 55)]
    cancel_dict = {}

    if orders is not None:
        for order in orders:
            code = order['code']
            no_cancel_codes = {'511990.SH', '511880.SH'}
            if code in no_cancel_codes:
                print(f'当前标的{code},不撤单')
                return
            else:
                print(f'当前标的{code},可撤单')
    # if orders is not None:
    #     for order in orders:
    #         code = order['code']
                o_remark = order['remark']
                order['order_price'] = custom_round(order['order_price'], 2)
                if (order['order_price'] == xtdata.get_instrument_detail(code)['UpStopPrice'] and order['order_type'] == 23) \
                        or (order['order_price'] == xtdata.get_instrument_detail(code)['DownStopPrice'] and order[
                    'order_type'] == 24):
                    print(code, '------', '挂涨停的买单和挂跌停的卖单不撤！')
                    continue
                elif order['order_type'] == 23:
                    cancel_order_volume = order['order_volume'] - order['traded_volume']
                    print(code, '------', f'买单还有{cancel_order_volume}股未成交，准备撤单！')
                elif order['order_type'] == 24:
                    cancel_order_volume = -(order['order_volume'] - order['traded_volume'])
                    print(code, '------', f'卖单还有{-cancel_order_volume}股未成交，准备撤单！')
                else:
                    continue

                cancel_result = -1
                if order['sysid'] is not None:
                    cancel_result = xt_trader.cancel_order_stock_sysid_async(account, 0 if 'SH' in code else 1,
                                                                             order['sysid'])
                    print(code, '正在撤单，方式1')

                elif order['id'] is not None:
                    cancel_result = xt_trader.cancel_order_stock_async(account, order['id'])
                    print(code, '正在撤单，方式2')

                time.sleep(cancel_execute_interval)

                if cancel_result >= 0:
                    print(f'{code}撤单成功，所撤委托备注{o_remark}')
                    cancel_dict[code] = cancel_order_volume
                else:
                    print(f'{code}撤单失败，失败撤单委托备注{o_remark}')

        if now <= '14:56:30':
            for stock_code, volume in cancel_dict.items():
                print(f'{stock_code}正在尝试重新下单')
                total_value = xt_trader.query_stock_asset(account).total_asset
                current_price = xtdata.get_full_tick([stock_code])[stock_code]['lastPrice']
                available_cash = xt_trader.query_stock_asset(account).cash
                remark = datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单')
                print('当下数量', volume)
                if volume > 0:
                    if available_cash > total_value * 0.0005:
                        buy_price = min(current_price * (1.00 + buy_price_deviation),
                                        xtdata.get_instrument_detail(stock_code)['UpStopPrice'])
                        can_buy_volume = available_cash / buy_price
                        buy_volume = min(volume, can_buy_volume)
                        if stock_code[:2] in ['00', '60', '30']:
                            buy_volume = int(buy_volume // 100) * 100
                        elif stock_code[:2] == '68':
                            buy_volume = buy_volume if buy_volume >= 200 else 0
                        elif stock_code[0] == '1':
                            buy_volume = int(buy_volume // 10) * 10
                        elif stock_code[0] in ['4', '8', '9']:
                            buy_volume = buy_volume if buy_volume >= 100 else 0
                        else:
                            buy_volume = int(buy_volume // 100) * 100
                        print('当下买入数量', buy_volume)
                        if buy_volume > can_buy_volume:
                            warnings.warn(f'{stock_code}可用现金不足，用剩余现金全部买入！')

                        if buy_volume > 0:
                            resp = xt_trader.order_stock_async(account, stock_code, 23, buy_volume, 11,
                                                               buy_price,
                                                               'cancel_reorder_entrustment_stock', remark)
                            print(f'已重新下单买入成功')
                    else:
                        warnings.warn(f'{stock_code}无可用现金！')
                        return
                elif volume < 0:
                    usable_volume = 0
                    position_list = xt_trader.query_stock_positions(account)
                    for position in position_list:
                        if position.stock_code == stock_code and position.volume > 0:
                            usable_volume = position.can_use_volume
                            break
                    print('当下可用数量', usable_volume)
                    if usable_volume > 0:
                        sell_price = max(current_price * (1.00 - sell_price_deviation),
                                         xtdata.get_instrument_detail(code)['DownStopPrice'])
                        volume = abs(volume)
                        print('当下绝对数量', volume)
                        sell_volume = min(volume, usable_volume)
                        print('当下可卖数量1', sell_volume)
                        if stock_code[:2] in ['00', '60', '30']:
                            sell_volume = int(sell_volume // 100) * 100
                        elif stock_code[:2] == '68':
                            sell_volume = sell_volume if sell_volume >= 200 else usable_volume
                        elif stock_code[0] == '1':
                            sell_volume = int(sell_volume // 10) * 10
                        elif stock_code[0] in ['4', '8', '9']:
                            sell_volume = sell_volume if sell_volume >= 100 else usable_volume
                        else:
                            sell_volume = int(sell_volume // 100) * 100
                        print('当下可卖数量2', sell_volume)
                        if sell_volume > usable_volume:
                            warnings.warn(f'{stock_code}可用数量不足，将卖出所有可用持仓！')

                        if sell_volume > 0:
                            resp = xt_trader.order_stock_async(account, stock_code, 24, sell_volume, 11,
                                                               sell_price,
                                                               'order_target_weight', remark)
                            print(f'已重新下单卖出成功')
                    else:
                        warnings.warn(f'{stock_code}无可用持仓！')
                        return
        else:
            print('尾盘不重新下单，只撤单')
    return



@try_except
def order_target_weight_fyx(stock_code: str, target_weight, account: Union[str, StockAccount], contextinfo: ContextInfo,
                        order_id: str = '', price=-1, xt_trader: Union[None, xttrader.XtQuantTrader] = None,
                        quote_mode: str = 'backtest', quick_trade=True, order_count=1) -> None:
    """
    将持仓调整至目标权重，没有该持仓会买入；权重为0时卖出全部持仓；可指定price参数，默认-1为市价单，只支持股票（价格轮子版）
    """
    if 1 < target_weight or target_weight < 0: raise ValueError("目标权重应当位于0到1之间（闭区间）")
    if quote_mode in ['realtime', 'all']:
        if type(account) is not StockAccount: raise TypeError("实盘/模拟盘传入账户应当为StockAccount类型")
        if type(xt_trader) is None: raise TypeError("实盘/模拟盘应当传入xt_trader参数，且类型为XtQuantTrader")
        remark = datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
        for i in range(1, order_count + 1):
            print(f'尝试下单-{i}代码:{stock_code}')

            current_value = 0
            usable_value = 0
            usable_volume = 0
            current_price = \
                xtdata.get_full_tick([stock_code])[stock_code]['lastPrice']
            total_value = xt_trader.query_stock_asset(account).total_asset
            position_list = xt_trader.query_stock_positions(account)
            available_cash = xt_trader.query_stock_asset(account).cash

            for position in position_list:
                if position.stock_code == stock_code and position.volume > 0:
                    current_value = position.volume * current_price
                    usable_value = position.can_use_volume / position.volume * current_value
                    usable_volume = position.can_use_volume
                    usable_ratio = position.can_use_volume / position.volume
                    break

            adjust_value = (target_weight - current_value / total_value) * total_value

            if adjust_value < 0 and usable_ratio > 0:
                adjust_value = usable_ratio * (target_weight - current_value / total_value) * total_value
                if usable_value < abs(adjust_value):
                    warnings.warn(f'{stock_code}可用数量不足，将卖出所有可用持仓。')
                    adjust_value = -usable_value

                current_price = xtdata.get_full_tick([stock_code])[stock_code]['lastPrice']

                if price == -1:
                    order_price = current_price
                else:
                    order_price = max(current_price * (1 - price),
                                      xtdata.get_instrument_detail(stock_code)['DownStopPrice'])

                sell_volume = abs(adjust_value) / order_price
                sell_volume = max(int(sell_volume // 100) * 100, 100)
                if sell_volume > usable_volume:
                    warnings.warn(f'{stock_code}可用数量不足，将卖出所有可用持仓。')
                    sell_volume = usable_volume

                resp = xt_trader.order_stock_async(account, stock_code, 24, sell_volume, 11,
                                                   order_price,
                                                   'order_target_weight', remark)

            elif adjust_value == 0 or (adjust_value < 0 and usable_ratio == 0):
                return

            else:

                current_price = xtdata.get_full_tick([stock_code])[stock_code]['lastPrice']
                if price == -1:
                    order_price = current_price
                else:
                    order_price = min(current_price * (1 + price),
                                      xtdata.get_instrument_detail(stock_code)['UpStopPrice'])

                buy_volume = adjust_value / order_price
                buy_volume = int(buy_volume // 100) * 100

                can_buy_volume = int(
                    (available_cash / order_price)) // 100 * 100
                if can_buy_volume < 200:
                    warnings.warn('可买数量小于200股')
                    return

                elif buy_volume <= can_buy_volume and buy_volume >= 200:
                    resp = xt_trader.order_stock_async(account, stock_code, 23, buy_volume, 11,
                                                       order_price,
                                                       'order_target_weight', remark)
                elif buy_volume <= can_buy_volume and buy_volume < 200 and can_buy_volume >= 200:
                    resp = xt_trader.order_stock_async(account, stock_code, 23, 200, 11,
                                                       order_price,
                                                       'order_target_weight', remark)
                elif buy_volume > can_buy_volume and can_buy_volume >= 200:
                    warnings.warn(f'原下单数量{buy_volume}，可用资金不足，将调整下单数量为{can_buy_volume}。')
                    resp = xt_trader.order_stock_async(account, stock_code, 23, can_buy_volume,
                                                       11,
                                                       order_price,
                                                       'order_target_weight', remark)
                else:
                    warnings.warn('可买数量未知不足-------')
                    return

            if not quick_trade:
                break
            # if i == 10:
            #     print(f'{stock_code}暂未成交，维持最后委托')
            #     break
            time.sleep(1)
            orders = [
                {'status': order.order_status, 'remark': order.order_remark, 'time': order.order_time,
                 'sysid': order.order_sysid, 'id': order.order_id}
                for order in
                xt_trader.query_stock_orders(account) if order.order_remark == remark]
            if len(orders) == 0:
                print(f'{stock_code}今日无委托任务')
                break
            orders = sorted(orders, key=lambda x: x['time'])
            print(orders)
            latest_order = orders[-1]
            if latest_order['status'] == 56:
                break
            else:
                resp = None
                if latest_order['sysid'] is not None:
                    resp = xt_trader.cancel_order_stock_sysid_async(account, 0 if 'SH' in stock_code else 1,
                                                                    latest_order['sysid'])
                elif latest_order['id'] is not None:
                    resp = xt_trader.cancel_order_stock_async(account, latest_order['id'])
                else:
                    print(f'{stock_code}查询不到委托，无法进行撤单重下')
                    break
                for i in range(1, 6):
                    if resp == -1:
                        print(f'{stock_code}撤单暂未成功_{i}')
                        time.sleep(0.2)
                    elif resp is None:
                        print(f'{stock_code}撤单暂未响应_{i}')
                        time.sleep(0.2)
                    else:
                        print(f'{stock_code}撤单成功')
                        break
                if resp == -1:
                    print(f'{stock_code}撤单失败, 无法进行重下，维持原委托')
                    break
                elif resp is None:
                    print(f'{stock_code}撤单无响应，无法进行重下，维持原委托')
                    break
                else:
                    print(f'{stock_code}委托价调整为市价，准备重新下单')
                    price = -1
    else:
        if type(account) is not str: raise TypeError('回测传入账户应当为str类型')
        position_value = {dt.m_strInstrumentID: dt.m_dMarketValue for dt in
                          get_trade_detail_data(account, 'stock', 'position')}
        total_value = get_trade_detail_data(account, 'stock', 'ACCOUNT')[0].m_dBalance
        if stock_code[:-3] in position_value.keys():
            current_weight = position_value[stock_code[:-3]] / total_value
        else:
            current_weight = 0
        if current_weight < target_weight:
            passorder(
                23, 1113, account
                , stock_code, 5 if price == -1 else 11, price, target_weight - current_weight
                , 'order_target_weight', 1,
                datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                , contextinfo
            )
        else:
            passorder(
                24, 1113, account
                , stock_code, 5 if price == -1 else 11, price, current_weight - target_weight
                , 'order_target_weight', 1,
                datetime.datetime.now().strftime('%Y%m%d%H%M%S委托单') if order_id == '' else order_id
                , contextinfo
            )
    return


if __name__ == "__main__":
    from trade import get_ty_trader

    xt_trader = get_ty_trader(999)
    orders = [order.order_id for order in xt_trader.query_stock_orders(StockAccount('1004461', 'future'))]
    print(orders)
