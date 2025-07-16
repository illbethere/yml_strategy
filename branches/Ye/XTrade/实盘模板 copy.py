# coding:gbk
"""
�������֣�
���԰汾��v1
�������ߣ�kiki
�������ڣ�20250423
---���Ի�������---

"""

import traceback
import pandas as pd
import numpy as np
import statsmodels.api as sm
from xtquant import xtdata
from xtquant.qmttools.contextinfo import ContextInfo
import multiprocessing as mp
from tools.Order import *
import concurrent.futures as con
from tools.MultiTask import run_strategy
import time
# from datetime import datetime, timedelta
import datetime as dt
from tools.Reconnect import connect_xttrader, reconnect_xttrader
from xtquant_gt import xtconstant
from xtquant_gt.xttype import StockAccount
import math
import csv
import pickle


xtdata.reconnect(port=58614)  # ��Ҫ�Ľӿ�
xtdata.enable_hello = True


class G: pass


g = G()


def contract_change(datestr: str):
    """
    ����¸�������������Լ�Ƿ�������ÿ�µ�����������������Լ�����
    :param datestr: ʱ���ַ�������Ҫ��YYYY-MM-DD��ʽ��ͷ
    """
    year_month = datestr[:7]
    first_day_of_the_month = pd.to_datetime(year_month).weekday()
    year_month_day = datestr[:10]
    date = pd.to_datetime(year_month_day)
    if first_day_of_the_month == 6:
        week_num = (date.day - 1 + first_day_of_the_month) // 7 + 1
    else:
        week_num = (date.day + first_day_of_the_month) // 7 + 1
    if week_num != 3:
        return False
    else:
        if date.weekday() == 3:
            return True
        else:
            return False


def next_contract(future_code):
    """
    ���ݵ�ǰ��Լ�����ȡ���º�Լ
    """
    date = pd.to_datetime(''.join([s for s in future_code if s.isdigit()]) + '01', yearfirst=True)
    head = ''.join([s for s in future_code.split('.')[0] if s.isalpha()])
    tail = '.' + future_code.split('.')[1]
    year = date.year
    month = date.month
    next_month = (month + 1) % 12
    if next_month == 1:
        year += 1
    new_date = dt.datetime(year, next_month, 1).strftime("%y%m")
    return head + new_date + tail


def get_delayed_signal(delayed_signal_series: Union[bool, pd.Series],
                       origin_signal: bool,
                       data: pd.DataFrame,
                       period: str,
                       signal_type: str,
                       price_type: str):
    final_signal = False
    if origin_signal and delayed_signal_series is not False:
        if period == '1m' and data['time'].iloc[-1] > delayed_signal_series['time'] and len(data) >= 3:
            if signal_type == '>':
                confirm_signal = data[price_type].iloc[-2] > delayed_signal_series[price_type]
            elif signal_type == '<':
                confirm_signal = data[price_type].iloc[-2] < delayed_signal_series[price_type]
            else:
                confirm_signal = False
        elif period == '5m' and data['time'].iloc[-1] > delayed_signal_series['time'] and len(data) >= 2:
            if signal_type == '>':
                confirm_signal = data[price_type].iloc[-1] > delayed_signal_series[price_type]
            elif signal_type == '<':
                confirm_signal = data[price_type].iloc[-1] < delayed_signal_series[price_type]
            else:
                confirm_signal = False
        elif period == '1h' and data['time'].iloc[-1] > delayed_signal_series['time'] and len(data) >= 2:
            if signal_type == '>':
                confirm_signal = data[price_type].iloc[-1] > delayed_signal_series[price_type]
            elif signal_type == '<':
                confirm_signal = data[price_type].iloc[-1] < delayed_signal_series[price_type]
            else:
                confirm_signal = False
        else:
            confirm_signal = False

        final_signal = confirm_signal

    if origin_signal and delayed_signal_series is False:
        delayed_signal_series = data.iloc[-1]
    elif origin_signal and delayed_signal_series['time'] == data['time'].iloc[-1]:
        delayed_signal_series = data.iloc[-1]
    elif period != '1m' and origin_signal and delayed_signal_series['time'] == data['time'].iloc[-2]:
        delayed_signal_series = data.iloc[-2]

    return delayed_signal_series, final_signal


def init(C):
    try:
        print('init')
        log = C._param['logger']
        log.info(f'����ģʽ:{C.trade_mode}')
        C.accountid = C._param['account']
        # C.accountid2 = C._param['account2']
        C.accountid_f = C._param['account_f']
        # C.acc = C._param['acc']
        # C.acc2 = C._param['acc2']
        # C.celian = C._param['strategy_name']
        print(C.accountid)
        C.acc_s = StockAccount(C.accountid, 'STOCK')
        C.acc_f = StockAccount(C.accountid_f, 'FUTURE')
        print(C.acc_s)
        g.miniQuote_path = r'D:\ѸͶͶ�ʽ���ϵͳ�����ն� ������˽ļģ��\miniQuote\userdata_mini' # ��Ҫ��·��
        C.xt_trader = None
        C.xt_trader = connect_xttrader(C.acc_s, g.miniQuote_path, log)
        print(C.xt_trader)
        try:
            xtdata.subscribe_quote('000300.SH', period='1m', count=60, callback=None)
            xtdata.subscribe_quote('200024.BKZS', period='5m', count=60, callback=None)
            xtdata.subscribe_quote('200024.BKZS', period='1m', count=60, callback=None)
            xtdata.subscribe_quote('200024.BKZS', period='1d', count=60, callback=None)
            # for bond in df.index:
            #     stock = df.loc[bond, 'stockCode']
            #     r_s_day = xtdata.subscribe_quote(stock, period='1d', count=200)
            #     r_b_day = xtdata.subscribe_quote(bond, period='1d', count=200)
            #     # r_s_5min = xtdata.subscribe_quote(stock, period='5m', count=500)
            #     r_b_5min = xtdata.subscribe_quote(bond, period='5m', count=500)
            #     # r_s_1min = xtdata.subscribe_quote(stock, period='1m', count=300)
            #     r_b_1min = xtdata.subscribe_quote(bond, period='1m', count=300)
            #     print(r_s_day, r_b_day, r_b_5min, r_b_1min)
            # bond_list = df.index.tolist()
            # stock_list = df['stockCode'].tolist()
            # r_ss = xtdata.subscribe_whole_quote(stock_list)
            # r_bb = xtdata.subscribe_whole_quote(bond_list)
            # print(r_ss, r_bb)
        except Exception as e:
            df = None
    except Exception as e:
        df = None
    g.trade_time = []
    g.pre_pos = 99
    future_code = xtdata.get_main_contract('IM00.IF')

    print(C.xt_trader)
    pd.set_option('display.max_rows', 50)
    pd.set_option('display.max_columns', 10)
    return


def after_init(C):
    try:
        print('after_init')
        log = C._param['logger']
        C.xt_trader = connect_xttrader(C.acc_s, g.miniQuote_path, log)
        # ����ÿ����ʮ���ӵĽ���ʱ���
        time_list = []
        time_interval = dt.timedelta(minutes=30)
        now = xtdata.timetag_to_datetime(C.get_bar_timetag(C.barpos), "%Y-%m-%d")
        start_time_am = dt.datetime.strptime('9:31:00', '%H:%M:%S')
        end_time_am = dt.datetime.strptime('11:30:00', '%H:%M:%S')
        current_time_am = start_time_am
    except Exception as e:
        print(e)
        traceback.print_exc()
    return


def handlebar(C):
    log = C._param['logger']
    trade_time = g.trade_time
    # now_date = now[:10].replace('-', '')
    # now_time = xtdata.timetag_to_datetime(C.get_bar_timetag(C.barpos), "%Y%m%d%H%M%S")

    # if g.pre_pos is not None:
    #     # K�����������
    #     if g.pre_pos == C.barpos or now[-8:] == '09:30:00':
    #         return
    #     now_kline_time = xtdata.get_market_data_ex(['time'], ['000300.SH'],
    #                                                period='1m', count=1)['000300.SH']['time'].iloc[-1]
    #     str_now_kline_time = xtdata.timetag_to_datetime(now_kline_time, "%Y-%m-%d %H:%M:%S")
    #     print(now, str_now_kline_time)
    #     if now < str_now_kline_time:
    #         print(f'K������������{now}��K��')
    #         log.info(f'K������������{now}��K��')
    #         g.pre_pos = C.barpos
    #         return

    now = xtdata.timetag_to_datetime(C.get_bar_timetag(C.barpos), "%Y-%m-%d %H:%M:%S")
    now_kline_time = xtdata.get_market_data_ex(['time'],['000300.SH'],period='1m',count=1)['000300.SH']['time'].iloc[0]
    str_now_kline_time = xtdata.timetag_to_datetime(now_kline_time, "%Y-%m-%d %H:%M:%S")

    if g.last_kline_time is None:
        g.last_kline_time = now_kline_time
        log.info(f'pass--C_barpos time:{now}--K_lines time:{str_now_kline_time}......')
        return
    elif now_kline_time > g.last_kline_time:
        g.last_kline_time = now_kline_time
        # ת��Ϊdatetime����
        c_barpos_time = dt.datetime.strptime(now, "%Y-%m-%d %H:%M:%S")
        k_lines_time = dt.datetime.strptime(str_now_kline_time, "%Y-%m-%d %H:%M:%S")
        # ����ʱ������ֵ��
        delta = k_lines_time - c_barpos_time
        # ת��Ϊ���Ӳ������ �� 60��
        minutes_diff = delta.total_seconds() / 60
        if minutes_diff>1.0:
            log.info(f'!!!Kline_blocking!!!--C_barpos time:{now}--K_lines time:{str_now_kline_time}......')
            return
        else:
            # log.info(f'enter--C_barpos time:{now}--K_lines time:{str_now_kline_time}......')
            # log.info(f'enter--C.xt_trader--{C.xt_trader}')
            C.xt_trader = reconnect_xttrader(C.xt_trader,C.acc_s,g.miniQuote_path,log)
            # log.info(f'enter--C.xt_trader--{C.xt_trader}')
    else:
        # log.info(f'pass--C_barpos time:{now}--K_lines time:{str_now_kline_time}......')
        return

    # δ�ɽ���������
    cancel_reorder_entrustment_stock_final(C.acc_s, C, C.xt_trader)

    # ��¼��ĳؿ������
    if now[-8:] == '09:31:00':
        bond_sector = xtdata.get_stock_list_in_sector('��תծ���')
        pct_list = []
        for bond in bond_sector:
            data = xtdata.get_market_data_ex(['close'], [bond], '1d', count=5)[bond]
            pct = data['close'].pct_change().iloc[-1]
            pct_list.append(pct)
        average_pct = np.mean(pct_list) * 100
        index_data = xtdata.get_market_data_ex(['close'], ['200024.BKZS'], '1d', count=5)['200024.BKZS']
        index_pct = index_data['close'].pct_change().iloc[-1] * 100
        log.info(f'bar_time {now} ԭ��ĳ�ƽ���Ƿ�Ϊ{average_pct}%�� ��Ȩָ���Ƿ�Ϊ{index_pct}%')  # ��¼��Ϊ���ձ�ĳؽ��쾺�����

    # ���ñ�ĳأ���������ѡ��
    if now[-8:] in ['09:31:00']:
        print(now)
        stock_total_value = C.xt_trader.query_stock_asset(C.acc_s).total_asset
        stock_market_value = C.xt_trader.query_stock_asset(C.acc_s).market_value
        log.info(f'{now} ��Ʊ�˻�{C.accountid}���ʲ�: {stock_total_value}')
        log.info(f'{now} ��Ʊ�˻�{C.accountid}�ֲ���ֵ: {stock_market_value}')
        holding_dict = {position.stock_code: position.market_value / stock_total_value for position in
                        C.xt_trader.query_stock_positions(C.acc_s) if position.market_value != 0}
        try:
            if len(g.buy_dict) > 0:
                g.buy_dict = {}  # �ɽ��ױ�����

            if len(holding_dict) > 0:
                bond_list = list(holding_dict.keys())
                for bond in bond_list:
                    try:
                        current_price = xtdata.get_full_tick([bond])[bond]['lastPrice']
                        if bond in excluded:  # ���ǿ�굽��st
                            print('������޳����')
                            log.info(f'������޳����{bond}��λ')
                            order_target_weight_final(bond, 0, C.acc_s, C, price=current_price - 0.1,
                                                xt_trader=C.xt_trader, quote_mode='realtime', quick_trade=False, order_price_type='limit_order',
                                                order_id='����ѱ��޳�')
                            profit = {position.stock_code: (current_price - position.avg_price) / position.avg_price
                                      for position in C.xt_trader.query_stock_positions(C.acc_s) if
                                      position.stock_code == bond}[bond]
                            log.info(f'�ֱֲ��{bond}��֣�ӯ������Ϊ��{profit}')
                        if pd.isna(factor_df.loc[bond, 'rank']) or factor_df.loc[bond, 'rank'] > 50:
                            print('��ղ������������')
                            log.info(f'��ղ������������߲������{bond}��λ')
                            order_target_weight_final(bond, 0, C.acc_s, C, price=current_price - 0.1,
                                                xt_trader=C.xt_trader, quote_mode='realtime', quick_trade=False, order_price_type='limit_order',
                                                order_id='��ձ��')
                            profit = {position.stock_code: (current_price - position.avg_price) / position.avg_price
                                      for position in C.xt_trader.query_stock_positions(C.acc_s) if
                                      position.stock_code == bond}[bond]
                            log.info(f'�ֱֲ��{bond}��֣�ӯ������Ϊ��{profit}')
                    except Exception:
                        print(f'{bond}���ɽ���')
                        log.info(f'{bond}���ɽ���')  # һ����ͣ��״̬
                        continue

            holding_dict = {position.stock_code: position.market_value / stock_total_value for position in
                            C.xt_trader.query_stock_positions(C.acc_s) if position.market_value != 0}
            for bond in factor_df.index:
                try:
                    rank = factor_df.loc[bond, 'rank']
                    if bond in holding_dict.keys():
                        pre_weight = holding_dict[bond]
                    else:
                        pre_weight = 0
                    if pre_weight < 0.001:
                        if rank <= 50:
                            weight = 0.02
                            log.info(f'��{rank}����{bond}���뿪���ֵ䣬Ȩ��:{weight}')
                            g.buy_dict[bond] = weight
                except Exception as e:
                    print(e)
                    continue
            log.info(f'{now} �����ֵ䣺{g.buy_dict}')
            log.info(f'{now} �ֲ��ֵ䣺{holding_dict}')
            print(f'{now} �����ֵ䣺{g.buy_dict}')
            print(f'{now} �ֲ��ֵ䣺{holding_dict}')

            all_bonds = set(g.buy_dict) | set(holding_dict)
            print(f'���ı�ģ�{len(all_bonds)}, {all_bonds}')
            for bond in all_bonds:
                r_b_day = xtdata.subscribe_quote(bond, period='1d', count=200)
                r_b_5min = xtdata.subscribe_quote(bond, period='5m', count=500)
                r_b_1min = xtdata.subscribe_quote(bond, period='1m', count=300)
                print(r_b_day, r_b_5min, r_b_1min)
                data_1min = xtdata.get_market_data_ex(['open', 'high', 'low', 'close', 'time'], [bond],
                                                      period='1m', count=300, dividend_type='front')
                print(bond, data_1min[bond]['close'].tail(1))

        except Exception as e:
            print(e)
            traceback.print_exc()

    # ���彻���߼�
    if now[-8:] not in ['14:58:00', '14:59:00', '15:00:00']:
        try:
            stock_total_value = C.xt_trader.query_stock_asset(C.acc_s).total_asset
            stock_market_value = C.xt_trader.query_stock_asset(C.acc_s).market_value
            holding_dict = {position.stock_code: position.market_value / stock_total_value for position in
                            C.xt_trader.query_stock_positions(C.acc_s) if position.market_value != 0}

            print(f'�ȴ����֣�{g.buy_dict}')
            # �����߼�
            total_weight = stock_market_value / stock_total_value
            holding_dict = {position.stock_code: position.market_value / stock_total_value for position in
                            C.xt_trader.query_stock_positions(C.acc_s) if position.market_value != 0}
            buy_list = list(g.buy_dict.keys())

            if len(buy_list) == 0 or total_weight > 0.98:
                print('���ձ���������������')
                pass
            else:
                buy_data_dict_hour = xtdata.get_market_data_ex(['open', 'high', 'low', 'close', 'time'], buy_list,
                                                               period='1h', count=300, dividend_type='front')
                buy_data_dict_5min = xtdata.get_market_data_ex(['open', 'high', 'low', 'close', 'time'], buy_list,
                                                              period='5m', count=300, dividend_type='front')
                buy_data_dict_1min = xtdata.get_market_data_ex(['open', 'high', 'low', 'close', 'time'], buy_list,
                                                               period='1m', count=300, dividend_type='front')

                for bond in buy_list:  # Ŀǰ�����ź�1
                    try:
                        current_price = xtdata.get_full_tick([bond])[bond]['lastPrice']
                        # prebar_high_1m = buy_data_dict_1min[bond]['high'].iloc[-2]
                        # print(bond, current_price, prebar_high_1m)
                        stock = g.bond_to_stock[bond]
                        p1 = xtdata.get_full_tick([stock])[stock]['lastPrice']
                        p2 = xtdata.get_instrument_detail(stock)['DownStopPrice']
                        down_limit_flag = (p1 == p2)
                        if down_limit_flag:
                            print(f'{bond}���ɵ�ͣ')
                            continue
                        else:
                            weight = 0.02  # ��λƫ�ƣ�δ�����������޸�
                            log.info(f'���������ź�, {bond}������{weight}����ǰ�۸�{current_price}')
                            order_target_weight_final(bond, weight, C.acc_s, C, price=current_price + 0.1,
                                                xt_trader=C.xt_trader, quote_mode='realtime', quick_trade=False, order_price_type='limit_order',
                                                order_id=f'��������')
                            g.buy_dict.pop(bond)
                            print(f'{bond}�������ݣ�{buy_data_dict_1min[bond].tail(3)}')
                            log.info(f'{bond}�������ݣ�{buy_data_dict_1min[bond].tail(3)}')

                    except Exception:
                        print(f'{bond}���뽻���쳣')
                        traceback.print_exc()
                        continue

            print(f'{now} ɨ�����')

        except Exception as e:
            print(e)
            traceback.print_exc()

    # ÿ��ʮ���Ӽ�¼һ���˻�״̬
    if int(now[-5:-3]) % 30 == 1:
        stock_total_value = C.xt_trader.query_stock_asset(C.acc_s).total_asset
        stock_market_value = C.xt_trader.query_stock_asset(C.acc_s).market_value
        log.info(f'{now} ��Ʊ�˻�{C.accountid}���ʲ�: {stock_total_value}')
        log.info(f'{now} ��Ʊ�˻�{C.accountid}�ֲ���ֵ: {stock_market_value}')

    # β���ʲ���������������
    if now[-8:] >= '14:59:00':
        stock_total_value = C.xt_trader.query_stock_asset(C.acc_s).total_asset
        stock_market_value = C.xt_trader.query_stock_asset(C.acc_s).market_value
        log.info(f'{now} ��Ʊ�˻�{C.accountid}���ʲ�: {stock_total_value}���ֲ���ֵ��{stock_market_value}')

        print('90������β���ʲ�����')
        time.sleep(90)

        bond_sector = xtdata.get_stock_list_in_sector('��תծ���')
        pct_list = []
        for bond in bond_sector:
            data = xtdata.get_market_data_ex(['close'], [bond], '1d', count=5)[bond]
            pct = data['close'].pct_change().iloc[-1]
            pct_list.append(pct)
        average_pct = np.mean(pct_list) * 100
        index_data = xtdata.get_market_data_ex(['close'], ['200024.BKZS'], '1d', count=5)['200024.BKZS']
        index_pct = index_data['close'].pct_change().iloc[-1] * 100
        log.info(f'bar_time {now} �±�ĳ�ƽ���Ƿ�Ϊ{average_pct}%�� ��Ȩָ���Ƿ�Ϊ{index_pct}%')

        stock_total_value = C.xt_trader.query_stock_asset(C.acc_s).total_asset
        stock_market_value = C.xt_trader.query_stock_asset(C.acc_s).market_value
        # future_total_value = C.xt_trader.query_stock_asset(C.acc_f).total_asset
        log.info(f'{now} ��Ʊ�˻�{C.accountid}���ʲ�: {stock_total_value}���ֲ���ֵ��{stock_market_value}')
        # log.info(f'{now} �ڻ��˻�{C.accountid_f}���ʲ�: {future_total_value}')

        holding_dict = {position.stock_code: position.market_value / stock_total_value for position in
                        C.xt_trader.query_stock_positions(C.acc_s)}
        holding_data = xtdata.get_market_data_ex(['close'], list(holding_dict.keys()), period='1d', count=5)
        yesterday_vol = {position.stock_code: position.yesterday_volume for position in
                         C.xt_trader.query_stock_positions(C.acc_s)}
        cost_price = {position.stock_code: position.avg_price for position in
                      C.xt_trader.query_stock_positions(C.acc_s)}
        trade_price = {xttrade.stock_code: xttrade.traded_price for xttrade in
                       C.xt_trader.query_stock_trades(C.acc_s)}
        winrate = win_rate(holding_data, holding_dict, yesterday_vol, cost_price, trade_price)
        log.info(f'{now} ��Ʊ�˻�����ʤ�ʣ�{winrate}')

        # ��������
        print('--------��ʼ��������--------')

        # def download_data(code, startday):
        #     xtdata.download_history_data(code, '5m', startday, '', incrementally=True)
        #     xtdata.download_history_data(code, '1d', startday, '', incrementally=True)
        #     stock_code = xtdata.get_cb_info(code)['stockCode']
        #     xtdata.download_history_data(stock_code, '5m', startday, '', incrementally=True)
        #     xtdata.download_history_data(stock_code, '1d', startday, '', incrementally=True)

        bond_list = xtdata.get_stock_list_in_sector('����תծ')
        today = dt.date.today()
        startday = (today - dt.timedelta(weeks=1)).strftime("%Y%m%d")
        xtdata.download_history_data2(bond_list, '5m', startday, '', incrementally=True)
        xtdata.download_history_data2(bond_list, '1d', startday, '', incrementally=True)
        # timeout_list = []
        # with con.ThreadPoolExecutor(max_workers=2) as executor:
        #     for code in bond_list:
        #         future = executor.submit(download_data, code, startday)
        #         try:
        #             future.result(timeout=20)  # ���ó�ʱʱ��Ϊ20��
        #         except con.TimeoutError:
        #             print(f"���� {code} ��ʱ�������ñ������")
        #             timeout_list.append(code)
        #             continue
        #         except Exception as e:
        #             print(f"���� {code} �����쳣: {e}�������ñ������")
        #             continue
        # print('--------���س�ʱ��ĳ�����������--------')
        # print(f'��ʱ���������{len(timeout_list)}')
        # with con.ThreadPoolExecutor(max_workers=2) as executor:
        #     for code in timeout_list:
        #         future = executor.submit(download_data, code, startday)
        #         try:
        #             future.result(timeout=20)  # ���ó�ʱʱ��Ϊ20��
        #         except con.TimeoutError:
        #             print(f"���� {code} ��ʱ�������ñ������")
        #             continue
        #         except Exception as e:
        #             print(f"���� {code} �����쳣: {e}�������ñ������")
        #             continue
        print('--------�����������--------')

        print('���ղ����������')

    # g.pre_pos = C.barpos


if __name__ == '__main__':
    import sys
    import os

    user_script = sys.argv[0]  # ��ǰ�ű�·�������·��������·�����ɣ��˴�Ϊ����·���ķ���
    param_list = [{
        'stock_code': '000300.SH',  # ����handlebar�Ĵ���,
        'period': '1m',  # ����ִ������ ����ͼ����
        'start_time': '2022-01-01 00:00:00',  # ע���ʽ����Ҫд��
        'end_time': '2026-06-20 00:00:00',  # ע���ʽ����Ҫд��
        'trade_mode': 'simulation',  # simulation': ģ��, 'trading':ʵ��, 'backtest':�ز�
        'quote_mode': 'realtime',
        'dividend_type': 'front',
        'asset': 10000000,
        'strategy_name': '',
        'log_path': f'../log/{os.path.basename(user_script)[:-3]}.log',
        'account': '',# ��д�˺�
        # 'account2': '2006740[8]',
        'account_f': ''# ��д�˺�
        # handlebarģʽ��'realtime':��ʵʱ���飨��������ʷ�����handlebar��,'history':����ʷ����, 'all'�����У���history+realtime
    }]
    lock = mp.Manager().Lock()
    with con.ProcessPoolExecutor(max_workers=60) as executor:
        futures = {executor.submit(run_strategy, lock, user_script, param_list[i]): i for i in range(len(param_list))}

