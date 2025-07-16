# -*- coding: utf-8 -*-
# 监控的期货代码存放于 ./data/code.txt
from xtquant import xtdatacenter as xtdc
from xtquant import xtdata
import pandas as pd
from datetime import datetime, timedelta
import time
import tkinter as tk
from tkinter import ttk, messagebox
import asyncio
import concurrent.futures
import threading

xtdc.set_token("4065054877ce5724155dbc5bcba200381ce5eb35")
xtdc.init()


class TradingMonitorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("期货监控系统")
        self.root.geometry("1600x1000")

        # 数据存储
        self.contract_deal = ["ag2508.SF", "cu2507.SF"]  # 已成交的合约的标的
        # self.contract_deal = ['sh509.ZF']
        self.option_codes = [
            "ag2508P7800.SF",
            "cu2507P73000.SF",
            "SH509C2560.ZF",
            "SR509C6200.ZF",
            "a2509-C-4450.DF",
            "ps2508-C-36000.GF",
            "ag2508P8000.SF",
        ]  # 已成交合约
        self.main_contract = []
        self.dict_history = {}
        self.dict_history_all = {}
        self.df_results = None
        self.df_results_all = None
        self.n = 0.08  # 信号阈值
        # self.alarm_price = 8400
        # self.contract_price = 70.5 # 合约成交价格
        # self.contract_price_2 = 48
        self.alarm_threshold_put = 0.97  # 预警系数
        self.alarm_threshold_call = 1.05

        self.option_positions = {
            "ag2508P7800.SF": {"cost_price": 70.5, "position": 1, "multiplier": 15},
            "cu2507P73000.SF": {"cost_price": 48, "position": 1, "multiplier": 5},
            "ps2508-C-36000.GF": {"cost_price": 206, "position": 2, "multiplier": 3},
            "ag2508P8000.SF": {"cost_price": 75, "position": 2, "multiplier": 15},
        }  # 此处添加期权代码，成交价格 -> cost-price，手数 -> position以及每手交易单位 -> multiplier,添加完后需要再self.option_codes中添加对应的期权代码

        self.alarm_price = {
            "ag2508.SF": 8478.261 * self.alarm_threshold_put,
            "cu2507.SF": 79060 * self.alarm_threshold_put,
        }  # 合约成交时标的的价格 * 预警系数

        # 修正：初始化为过去时间，确保第一次更新
        self.last_1min_update = datetime.now() - timedelta(minutes=2)

        self.setup_ui()
        self.setup_data()

    def setup_ui(self):
        # 主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 标题
        title_label = ttk.Label(
            main_frame, text="期货监控系统", font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 10))

        # # 状态栏
        # self.status_frame = ttk.Frame(main_frame)
        # self.status_frame.pack(fill=tk.X, pady=(0, 10))

        # self.time_label = ttk.Label(self.status_frame, text="当前时间: ", font=("Arial", 10))
        # self.time_label.pack(side=tk.LEFT)

        # self.option_now = ttk.Label(self.status_frame, text="当前合约: ", font=("Arial", 10))
        # self.option_now.pack(side=tk.LEFT, padx=(20, 0))

        # self.option_label = ttk.Label(self.status_frame, text="期权价格: ", font=("Arial", 10))
        # self.option_label.pack(side=tk.LEFT, padx=(20, 0))

        # self.gain_label = ttk.Label(self.status_frame, text="盈亏: ", font=("Arial", 10))
        # self.gain_label.pack(side=tk.LEFT, padx=(20, 0))

        option_frame = ttk.LabelFrame(main_frame, text="期权持仓盈亏", padding="5")
        option_frame.pack(fill=tk.X, pady=(0, 10))

        self.option_update_label = ttk.Label(
            option_frame, text="上次更新: ", font=("Arial", 9)
        )
        self.option_update_label.pack(anchor=tk.W)

        self.option_tree = ttk.Treeview(
            option_frame,
            columns=(
                "current_price",
                "gain_loss",
                "gain_percent",
                "position",
                "total_gain",
            ),
            show="tree headings",
            height=4,
        )
        self.option_tree.heading("#0", text="期权合约")
        self.option_tree.heading("current_price", text="当前价格")
        self.option_tree.heading("gain_loss", text="单位盈亏")
        self.option_tree.heading("gain_percent", text="盈亏百分比")
        self.option_tree.heading("position", text="持仓数量")
        self.option_tree.heading("total_gain", text="总盈亏")

        self.option_tree.column("#0", width=120)
        for col in (
            "current_price",
            "gain_loss",
            "gain_percent",
            "position",
            "total_gain",
        ):
            self.option_tree.column(col, width=100)

        option_scrollbar = ttk.Scrollbar(
            option_frame, orient=tk.VERTICAL, command=self.option_tree.yview
        )
        self.option_tree.configure(yscrollcommand=option_scrollbar.set)

        self.option_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        option_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 主要内容区域
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # 左侧 - 1分钟数据
        left_frame = ttk.LabelFrame(
            content_frame,
            text="1分钟数据 (所有期货) 红色 -> sell call | 绿色 -> sell put | 黄色 -> 现价接近最高最低价1%范围内",
            padding="5",
        )
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        # 1分钟数据更新时间
        self.min1_update_label = ttk.Label(
            left_frame, text="上次更新: ", font=("Arial", 9)
        )
        self.min1_update_label.pack(anchor=tk.W)

        # 1分钟数据表格
        self.min1_tree = ttk.Treeview(
            left_frame,
            columns=("signal", "pos", "neg", "strike", "min", "max", "price"),
            show="tree headings",
        )
        self.min1_tree.heading("#0", text="合约")
        self.min1_tree.heading("signal", text="信号")
        self.min1_tree.heading("pos", text="正向")
        self.min1_tree.heading("neg", text="负向")
        self.min1_tree.heading("strike", text="行权价")
        self.min1_tree.heading("min", text="最低价")
        self.min1_tree.heading("max", text="最高价")
        self.min1_tree.heading("price", text="当前价")

        # 设置列宽
        self.min1_tree.column("#0", width=100)
        for col in ("signal", "pos", "neg", "strike", "min", "max", "price"):
            self.min1_tree.column(col, width=80)

        # 1分钟数据滚动条
        min1_scrollbar = ttk.Scrollbar(
            left_frame, orient=tk.VERTICAL, command=self.min1_tree.yview
        )
        self.min1_tree.configure(yscrollcommand=min1_scrollbar.set)

        self.min1_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        min1_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 右侧 - tick数据
        right_frame = ttk.LabelFrame(
            content_frame, text="Tick数据 (指定期货)", padding="5"
        )
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # tick数据更新时间
        self.tick_update_label = ttk.Label(
            right_frame, text="上次更新: ", font=("Arial", 9)
        )
        self.tick_update_label.pack(anchor=tk.W)

        # tick数据表格
        self.tick_tree = ttk.Treeview(
            right_frame,
            columns=(
                "signal",
                "pos",
                "neg",
                "strike",
                "min",
                "max",
                "price",
                "alarm_price",
            ),
            show="tree headings",
        )
        self.tick_tree.heading("#0", text="合约")
        self.tick_tree.heading("signal", text="信号")
        self.tick_tree.heading("pos", text="正向持仓信号")
        self.tick_tree.heading("neg", text="负向持仓信号")
        self.tick_tree.heading("strike", text="行权价")
        self.tick_tree.heading("min", text="最低价")
        self.tick_tree.heading("max", text="最高价")
        self.tick_tree.heading("price", text="当前价")
        self.tick_tree.heading("alarm_price", text="预警价格")

        # 设置列宽
        self.tick_tree.column("#0", width=100)
        for col in (
            "signal",
            "pos",
            "neg",
            "strike",
            "min",
            "max",
            "price",
            "alarm_price",
        ):
            self.tick_tree.column(col, width=80)

        # tick数据滚动条
        tick_scrollbar = ttk.Scrollbar(
            right_frame, orient=tk.VERTICAL, command=self.tick_tree.yview
        )
        self.tick_tree.configure(yscrollcommand=tick_scrollbar.set)

        self.tick_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tick_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 日志区域
        log_frame = ttk.LabelFrame(main_frame, text="日志信息", padding="5")
        log_frame.pack(fill=tk.X, pady=(10, 0))

        self.log_text = tk.Text(log_frame, height=8, wrap=tk.WORD)
        log_scrollbar = ttk.Scrollbar(
            log_frame, orient=tk.VERTICAL, command=self.log_text.yview
        )
        self.log_text.configure(yscrollcommand=log_scrollbar.set)

        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def log_message(self, message):
        """添加日志消息"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)

    def setup_data(self):
        """初始化数据"""
        try:
            with open("./data/code.txt", "r") as f:
                codes = f.read().splitlines()

            for code in codes:
                data = xtdata.get_main_contract(code)
                if data:
                    self.main_contract.append(data)
                else:
                    self.log_message(f"未找到主力合约: {code}")

            today = datetime.now().date()
            yesterday = (today - timedelta(days=1)).strftime("%Y%m%d")
            today = datetime.now().date().strftime("%Y%m%d")

            dict_data = self.get_market_data(
                self.contract_deal, "1d", "20250407", yesterday, 20
            )
            dict_data_all = self.get_market_data(
                self.main_contract, "1d", "20250407", yesterday, 20
            )

            for contract in self.contract_deal:
                if contract in dict_data and not dict_data[contract].empty:
                    close_min = dict_data[contract]["close"].min()
                    close_max = dict_data[contract]["close"].max()
                    self.dict_history[contract] = {
                        "close_min": close_min,
                        "close_max": close_max,
                    }
                    # self.log_message(f"✓ {contract} 历史数据初始化成功: min={close_min:.2f}, max={close_max:.2f}")
                else:
                    self.log_message(f"✗ {contract} 历史数据获取失败或无数据！")

            for contract in self.main_contract:
                close_min = dict_data_all[contract]["close"].min()
                close_max = dict_data_all[contract]["close"].max()
                self.dict_history_all[contract] = {
                    "close_min": close_min,
                    "close_max": close_max,
                }

            columns = [
                "signal",
                "pos",
                "neg",
                "strike",
                "min",
                "max",
                "price",
                "alarm_price",
            ]
            self.df_results = pd.DataFrame(index=self.contract_deal, columns=columns)

            columns_1m = ["signal", "pos", "neg", "strike", "min", "max", "price"]
            self.df_results_all = pd.DataFrame(
                index=self.main_contract, columns=columns_1m
            )

            # 添加：使用当天历史数据初始化计数
            morning_start = today + "090000"

            # 初始化tick数据的计数
            tick_stats = self.init_signal_stats(
                self.contract_deal, self.dict_history, morning_start, today
            )
            self.df_results["pos"] = [tick_stats[c]["pos"] for c in self.contract_deal]
            self.df_results["neg"] = [tick_stats[c]["neg"] for c in self.contract_deal]

            # 初始化1分钟数据的计数
            min1_stats = self.init_signal_stats(
                self.main_contract, self.dict_history_all, morning_start, today
            )
            self.df_results_all["pos"] = [
                min1_stats[c]["pos"] for c in self.main_contract
            ]
            self.df_results_all["neg"] = [
                min1_stats[c]["neg"] for c in self.main_contract
            ]

            self.log_message("数据初始化完成")

        except Exception as e:
            self.log_message(f"数据初始化失败: {str(e)}")

    def init_signal_stats(self, contracts, dict_history, start, today):
        """
        用今日历史数据初始化每个合约的pos/neg统计
        """
        stats = {}
        try:
            # 获取1分钟历史数据
            hist_data = self.get_market_data(contracts, "1m", start, today, -1)
            for contract in contracts:
                close_min = dict_history[contract]["close_min"]
                close_max = dict_history[contract]["close_max"]
                closes = hist_data[contract]["close"]
                pos = (closes > close_max).sum()
                neg = (closes < close_min).sum()
                stats[contract] = {"pos": int(pos), "neg": int(neg)}
                self.log_message(f"初始化 {contract}: pos={pos}, neg={neg}")
        except Exception as e:
            self.log_message(f"初始化信号统计失败: {str(e)}")
            # 如果失败，使用默认值
            for contract in contracts:
                stats[contract] = {"pos": 0, "neg": 0}
        return stats

    def get_market_data(
        self, codes: list, period: str, start_time: str, end_time: str, count: int
    ) -> dict:
        """获取市场数据"""
        for code in codes:
            xtdata.subscribe_quote(
                code, period, start_time, end_time, count, callback=None
            )
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

        for code in codes:
            if market_data[code].empty:
                self.log_message(f"数据 {code} 获取失败！")
                break

        return market_data

    async def get_tick_data_async(
        self, codes: list, start_time: str, end_time: str, count: int
    ) -> dict:
        """异步获取tick数据"""
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(
                executor,
                self.get_market_data,
                codes,
                "tick",
                start_time,
                end_time,
                count,
            )

        # for code in codes:
        #     if code in result and not result[code].empty:
        #         self.log_message(f"Tick数据 {code} 获取成功, 共{len(result[code])}条记录")
        #     else:
        #         self.log_message(f"Tick数据 {code} 获取失败或无数据！")

        return result

    async def get_1min_data_async(
        self, main_contract: list, start_time: str, end_time: str, count: int
    ) -> dict:
        """异步获取1分钟数据"""
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(
                executor,
                self.get_market_data,
                main_contract,
                "1m",
                start_time,
                end_time,
                count,
            )
        return result

    def update_treeview(self, tree, df, update_time_label, data_type):
        """更新表格显示"""
        # 清空现有数据
        for item in tree.get_children():
            tree.delete(item)

        # 更新时间标签
        current_time = datetime.now().strftime("%H:%M:%S")
        update_time_label.config(text=f"上次更新: {current_time}")

        # 添加新数据
        df_sorted = df.sort_values(
            by=["signal", "strike", "pos", "neg"],
            ascending=[False, False, False, False],
        )

        for contract, row in df_sorted.iterrows():
            values = []
            if data_type == "Tick":
                columns_to_show = [
                    "signal",
                    "pos",
                    "neg",
                    "strike",
                    "min",
                    "max",
                    "price",
                    "alarm_price",
                ]
            else:
                columns_to_show = [
                    "signal",
                    "pos",
                    "neg",
                    "strike",
                    "min",
                    "max",
                    "price",
                ]
            for col in columns_to_show:
                val = row[col]
                if pd.isna(val):
                    values.append("")
                elif isinstance(val, float):
                    values.append(f"{val:.2f}")
                else:
                    values.append(str(val))

            # 根据信号设置颜色标记
            item = tree.insert("", tk.END, text=contract, values=values)
            if row["signal"] == 1:
                tree.set(item, "signal", "Put")
                tree.item(item, tags=("put_signal",))
            elif row["signal"] == -1:
                tree.set(item, "signal", "Call")
                tree.item(item, tags=("call_signal",))
            else:
                if (
                    data_type == "1分钟"
                    and not pd.isna(row["price"])
                    and not pd.isna(row["min"])
                    and not pd.isna(row["max"])
                ):
                    current_price = row["price"]
                    min_price = row["min"]
                    max_price = row["max"]

                    if current_price > max_price * 0.99 and current_price < max_price:
                        tree.item(item, tags=("neutral_signal",))
                    elif current_price < min_price * 1.01 and current_price > min_price:
                        tree.item(item, tags=("neutral_signal",))

        # 设置标签颜色
        tree.tag_configure("put_signal", background="lightgreen")
        tree.tag_configure("call_signal", background="lightcoral")
        tree.tag_configure("neutral_signal", background="yellow")

        self.log_message(f"{data_type}数据更新完成")

    def update_option_positions(self):
        try:
            option_data = xtdata.get_full_tick(self.option_codes)

            for item in self.option_tree.get_children():
                self.option_tree.delete(item)

            current_tiem = datetime.now().strftime("%H:%M:%S")
            self.option_update_label.config(text=f"上次更新: {current_tiem}")

            total_gain_all = 0

            for option_code in self.option_codes:
                if option_code in option_data and option_code in self.option_positions:
                    current_price = option_data[option_code]["lastPrice"]
                    position_info = self.option_positions[option_code]

                    cost_price = position_info["cost_price"]
                    position = position_info["position"]
                    multiplier = position_info["multiplier"]

                    # if 'P' in option_code:

                    gain_loss = cost_price - current_price
                    gain_percent = (gain_loss / cost_price) * 100
                    total_gain = gain_loss * position * multiplier
                    total_gain_all += total_gain
                    # elif 'C' in option_code:
                    # gain_loss = current_price - cost_price
                    # gain_percent = (gain_loss / cost_price) * 100
                    # total_gain = gain_loss * position * multiplier
                    # total_gain_all += total_gain

                    values = [
                        f"{current_price:.2f}",
                        f"{gain_loss:.2f}",
                        f"{gain_percent:.2f}%",
                        f"{position}",
                        f"{total_gain:.2f}",
                    ]

                    item = self.option_tree.insert(
                        "", tk.END, text=option_code, values=values
                    )

                    if gain_percent > 0:
                        self.option_tree.item(item, tags=("profit",))
                    elif gain_percent < 0:
                        self.option_tree.item(item, tags=("loss",))

                    # if len(self.option_codes) > 1:
                    #     total_values = ['', '', '', '', '总计:', f"{total_gain_all:.2f}"]
                    #     total_item = self.option_tree.insert('', tk.END, text='总计', values=total_values)
                    #     self.option_tree.item(total_item, tags=('total',))

                    self.option_tree.tag_configure("profit", background="lightgreen")
                    self.option_tree.tag_configure("loss", background="lightcoral")
                    self.option_tree.tag_configure("normal", background="white")
                    self.option_tree.tag_configure(
                        "total", background="lightyellow", font=("Arial", 10, "bold")
                    )

        except Exception as e:
            self.log_message(f"期权持仓更新失败: {str(e)}")

    def update_status(self):
        """更新状态栏"""
        try:
            # current_time = datetime.now().strftime("%H:%M:%S")
            # self.time_label.config(text=f"当前时间: {current_time}")

            # self.option_now.config(text=f"当前合约: {','.join(self.option_codes)}")

            # option_now_data = xtdata.get_full_tick(self.option_codes)

            # option_prices = []

            # for i, option_code in enumerate(self.option_codes):
            #     if option_code in option_now_data:
            #         price = option_now_data[option_code]['lastPrice']
            #         option_prices.append(price)
            #     else:
            #         option_prices.append(0.0)

            # if len(option_prices) >= 2:
            #     self.option_label.config(text=f"期权价格: {option_prices[0]:.2f}||| {option_prices[1]:.2f}元/单位")

            #     gain_1 = self.contract_price - option_prices[0]
            #     percentage_gain_1 = (gain_1 / self.contract_price) * 100
            #     gain_2 = self.contract_price_2 - option_prices[1]
            #     percentage_gain_2 = (gain_2 / self.contract_price_2) * 100

            #     self.gain_label.config(text=f"盈亏: {percentage_gain_1:.2f}%({gain_1:.2f}元) | {percentage_gain_2:.2f}%({gain_2:.2f}元)")

            # # option_now_price = option_now_data[self.option_codes[0]]['lastPrice']
            # # option_now_price = option_now_data[self.option_codes[1]]['lastPrice']

            # # self.option_label.config(text=f"期权价格: {option_now_price:.2f}||| {self.contract_price:.2f}元/单位")

            # # gain = self.contract_price - option_now_price
            # # percentage_gain = (self.contract_price - option_now_price) / self.contract_price * 100
            # # gain_2 = self.contract_price_2 - option_now_price
            # # percentage_gain_2 = (self.contract_price_2 - option_now_price) / self.contract_price_2 * 100
            # # self.gain_label.config(text=f"盈亏: {percentage_gain:.2f}% ====== {gain:.2f}元/单位||| {percentage_gain_2:.2f}% ====== {gain_2:.2f}元/单位")

            #     if percentage_gain_1 < -5:
            #         self.gain_label.config(foreground='red')
            #         self.log_message("期权价格下跌超过5%，请注意！")
            #     else:
            #         self.gain_label.config(foreground='black')

            # for option_code in self.option_codes:
            #     if option_code in option_now_data:
            #         price = option_now_data[option_code]['lastPrice']
            #         self.log_message(f"期权 {option_code} 当前价格: {price:.2f}")
            self.update_option_positions()

        except Exception as e:
            self.log_message(f"状态更新失败: {str(e)}")

    async def update_data(self):
        """更新数据"""
        today = datetime.now().date().strftime("%Y%m%d")
        current_time = datetime.now()
        morning_start = datetime.strptime("09:00:00", "%H:%M:%S").time()
        morning_end = datetime.strptime("11:30:00", "%H:%M:%S").time()
        afternoon_start = datetime.strptime("13:30:00", "%H:%M:%S").time()
        afternoon_end = datetime.strptime("15:00:00", "%H:%M:%S").time()
        night_start = datetime.strptime("21:00:00", "%H:%M:%S").time()
        night_end = datetime.strptime("23:00:00", "%H:%M:%S").time()

        try:
            # 修正：使用total_seconds()计算时间差
            time_diff = (current_time - self.last_1min_update).total_seconds()
            need_1min_update = time_diff >= 60

            if need_1min_update:
                tick_task = self.get_tick_data_async(
                    self.contract_deal, today, today, 1
                )
                min1_task = self.get_1min_data_async(
                    self.main_contract, today, today, 1
                )

                tick_data, min1_data = await asyncio.gather(tick_task, min1_task)

                for contract in self.main_contract:
                    close_min = self.dict_history_all[contract]["close_min"]
                    close_max = self.dict_history_all[contract]["close_max"]
                    close_now = min1_data[contract]["close"].iloc[-1]

                    self.df_results_all.at[contract, "min"] = close_min
                    self.df_results_all.at[contract, "max"] = close_max
                    self.df_results_all.at[contract, "price"] = close_now

                    count_pos = self.df_results_all.at[contract, "pos"]
                    count_neg = self.df_results_all.at[contract, "neg"]

                    if close_now > close_max and (
                        current_time.time() >= morning_start
                        and current_time.time() <= morning_end
                        or current_time.time() >= afternoon_start
                        and current_time.time() <= afternoon_end
                        or current_time.time() >= night_start
                        and current_time.time() <= night_end
                    ):
                        count_pos += 1
                        self.df_results_all.at[contract, "pos"] = count_pos
                    elif close_now < close_min and (
                        current_time.time() >= morning_start
                        and current_time.time() <= morning_end
                        or current_time.time() >= afternoon_start
                        and current_time.time() <= afternoon_end
                        or current_time.time() >= night_start
                        and current_time.time() <= night_end
                    ):
                        count_neg += 1
                        self.df_results_all.at[contract, "neg"] = count_neg

                    if (
                        count_pos >= 1
                        and self.df_results_all.at[contract, "signal"] != 1
                    ):
                        self.df_results_all.at[contract, "strike"] = close_now * (
                            1 - self.n
                        )
                    elif (
                        count_neg >= 1
                        and self.df_results_all.at[contract, "signal"] != -1
                    ):
                        self.df_results_all.at[contract, "strike"] = close_now * (
                            1 + self.n
                        )

                    if (
                        count_pos >= 10
                        and self.df_results_all.at[contract, "signal"] != 1
                    ):
                        self.df_results_all.at[contract, "signal"] = 1
                        self.log_message(
                            f"Sell Put信号: {contract} at price {self.df_results_all.at[contract, 'strike']:.2f}"
                        )
                    elif (
                        count_neg >= 10
                        and self.df_results_all.at[contract, "signal"] != -1
                    ):
                        self.df_results_all.at[contract, "signal"] = -1
                        self.log_message(
                            f"Sell Call信号: {contract} at price {self.df_results_all.at[contract, 'strike']:.2f}"
                        )

                self.update_treeview(
                    self.min1_tree, self.df_results_all, self.min1_update_label, "1分钟"
                )
                self.last_1min_update = current_time

            else:
                tick_data = await self.get_tick_data_async(
                    self.contract_deal, today, today, 1
                )

            for contract in self.contract_deal:
                close_min = self.dict_history[contract]["close_min"]
                close_max = self.dict_history[contract]["close_max"]
                close_now = tick_data[contract]["lastPrice"].iloc[-1]

                self.df_results.at[contract, "min"] = close_min
                self.df_results.at[contract, "max"] = close_max
                self.df_results.at[contract, "price"] = close_now

                if contract in self.alarm_price:
                    self.df_results.at[contract, "alarm_price"] = self.alarm_price[
                        contract
                    ]

                count_pos = self.df_results.at[contract, "pos"]
                count_neg = self.df_results.at[contract, "neg"]

                if close_now < self.alarm_price[contract]:
                    self.log_message(
                        f"价格 {close_now} 低于警戒线 {self.alarm_price[contract]}，请注意！"
                    )

                if close_now > close_max and (
                    current_time.time() >= morning_start
                    and current_time.time() <= morning_end
                    or current_time.time() >= afternoon_start
                    and current_time.time() <= afternoon_end
                    or current_time.time() >= night_start
                    and current_time.time() <= night_end
                ):
                    count_pos += 1
                    self.df_results.at[contract, "pos"] = count_pos
                elif close_now < close_min and (
                    current_time.time() >= morning_start
                    and current_time.time() <= morning_end
                    or current_time.time() >= afternoon_start
                    and current_time.time() <= afternoon_end
                    or current_time.time() >= night_start
                    and current_time.time() <= night_end
                ):
                    count_neg += 1
                    self.df_results.at[contract, "neg"] = count_neg

                if count_pos >= 1 and self.df_results.at[contract, "signal"] != 1:
                    self.df_results.at[contract, "strike"] = close_now * (1 - self.n)
                elif count_neg >= 1 and self.df_results.at[contract, "signal"] != -1:
                    self.df_results.at[contract, "strike"] = close_now * (1 + self.n)

                if count_pos >= 10 and self.df_results.at[contract, "signal"] != 1:
                    self.df_results.at[contract, "signal"] = 1
                    self.log_message(
                        f"Sell Put信号: {contract} at price {self.df_results.at[contract, 'strike']:.2f}"
                    )
                elif count_neg >= 10 and self.df_results.at[contract, "signal"] != -1:
                    self.df_results.at[contract, "signal"] = -1
                    self.log_message(
                        f"Sell Call信号: {contract} at price {self.df_results.at[contract, 'strike']:.2f}"
                    )

            self.update_treeview(
                self.tick_tree, self.df_results, self.tick_update_label, "Tick"
            )

        except Exception as e:
            self.log_message(f"数据更新失败: {str(e)}")

    async def main_loop(self):
        """主循环"""
        while True:
            # self.update_status()
            self.update_option_positions()

            # 检查交易时间
            current_time = datetime.now().time()
            if current_time >= datetime.strptime("23:00:00", "%H:%M:%S").time():
                self.log_message("交易日结束")
                break

            # 更新数据
            await self.update_data()

            # 等待1秒
            await asyncio.sleep(1)


def run_async_loop(gui):
    """在新线程中运行异步循环"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(gui.main_loop())


def main():
    root = tk.Tk()
    gui = TradingMonitorGUI(root)

    thread = threading.Thread(target=run_async_loop, args=(gui,), daemon=True)
    thread.start()

    # 启动GUI主循环
    root.mainloop()


if __name__ == "__main__":
    main()
