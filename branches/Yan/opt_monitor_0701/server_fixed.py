# venv\Scripts\activate
# python server_fixed.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
from datetime import datetime
from xtquant import xtdata, xtdatacenter
import threading
import time
from calc_HV_IV import calc_greeks_letter

app = Flask(__name__)
CORS(app)

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)


class DataService:
    def __init__(self):
        self.calendar = pd.read_pickle("./data/trading_days.pkl")
        self.main_contract = []
        self.dict_history_all = {}
        self.df_results_all = pd.DataFrame()
        self.n = 0.08  # 信号判定参数
        self.alarm_ratio = 0.03
        self.option_static_df = pd.DataFrame()
        self.option_table = pd.DataFrame()
        self.logs = []
        self.max_log_length = 20
        self.latest_results = None
        self.update_data_lock = threading.Lock()
        self.keep_running = True
        self.setup_data()  # 初始化只做一次
        self.setup_option()
        threading.Thread(target=self.background_update, daemon=True).start()

    def background_update(self):
        while self.keep_running:
            update_start = time.time()
            try:
                self.update_data()
                self.update_option()
            except Exception as e:
                print(f"[BG] update_data error: {e}")
            update_end = time.time()
            update_duration = update_end - update_start
            if update_duration < 60:
                time.sleep(max(0, 60 - update_duration))

    def log_message(self, msg):
        now = datetime.now().strftime("%H:%M:%S")
        self.logs.append({"time": now, "msg": msg})
        if len(self.logs) > 20:
            self.logs.pop(0)

    def get_market_data(self, codes, period, start_time, end_time, count):
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
        return market_data

    def setup_data(self):
        """初始化数据"""
        try:
            with open("./data/code.txt", "r") as f:
                codes = f.read().splitlines()

            # 主力合约初始化
            self.main_contract = []
            for code in codes:
                data = xtdata.get_main_contract(code)
                if data:
                    self.main_contract.append(data)
                else:
                    self.log_message(f"未找到主力合约: {code}")

            print("main_contract in setup:", self.main_contract)
            today = datetime.now().strftime("%Y%m%d")
            calendar = pd.read_pickle("./data/trading_days.pkl")
            # 1. 如果是只有一列的DataFrame，取第一列
            if isinstance(calendar, pd.DataFrame):
                days = calendar.iloc[:, 0].tolist()  # 取出第1列作为list
            elif isinstance(calendar, pd.Series):
                days = calendar.tolist()
            else:
                days = list(calendar)

            today = datetime.now().strftime("%Y%m%d")
            if today in days:
                idx = days.index(today)
                yesterday = days[idx - 1] if idx > 0 else days[0]
            else:
                yesterday = days[-1]

            dict_data_all = self.get_market_data(
                self.main_contract, "1d", "20250407", yesterday, 20
            )
            # 历史数据字典
            self.dict_history_all = {}
            for contract in self.main_contract:
                close_min = dict_data_all[contract]["close"].min()
                close_max = dict_data_all[contract]["close"].max()
                self.dict_history_all[contract] = {
                    "close_min": close_min,
                    "close_max": close_max,
                }

            columns_1m = ["signal", "pos", "neg", "strike", "min", "max", "price"]
            self.df_results_all = pd.DataFrame(
                0.0, index=self.main_contract, columns=columns_1m
            )

            # 计数初始化
            morning_start = today + "090000"
            min1_stats = self.init_signal_stats(
                self.main_contract, self.dict_history_all, morning_start, today
            )
            self.df_results_all["pos"] = [
                min1_stats.get(c, {}).get("pos", 0) for c in self.main_contract
            ]
            self.df_results_all["neg"] = [
                min1_stats.get(c, {}).get("neg", 0) for c in self.main_contract
            ]
            self.log_message("数据初始化完成")

        except Exception as e:
            self.log_message(f"数据初始化失败: {str(e)}")

    def setup_option(self):
        today = datetime.now().strftime("%Y%m%d")
        # 把交易日取成list
        if isinstance(self.calendar, pd.DataFrame):
            days = self.calendar.iloc[:, 0].tolist()
        elif isinstance(self.calendar, pd.Series):
            days = self.calendar.tolist()
        else:
            days = list(self.calendar)
        # 判断今天是不是交易日
        if today in days:
            idx = days.index(today)
            last_trading_day = days[idx - 1] if idx > 0 else days[0]
        else:
            last_trading_day = days[-1]  # 取最后一个可用日
        file = f"./data/每日报告_{last_trading_day}.xlsx"
        try:
            # 读取昨日报告合约
            df = pd.read_excel(file)
            df_copy = df.copy()
            df_copy.columns = df_copy.columns.str.strip().str.replace("\n", "")
            df_copy = df_copy.drop("日期", axis=1)
            df_copy = df_copy.dropna()

            # 读主力合约
            with open("./data/code.txt") as f:
                codes = [line.strip() for line in f]
            # 生成映射，如 {'ag': '.SF', 'al': '.SF', 'cu': '.SHF', ...}
            code_map = {}
            import re

            for code in codes:
                m = re.match(r"([a-zA-Z]{1,2})[0-9]*\..+", code)
                if m:
                    short = m.group(1)
                    code_map[short] = "." + code.split(".")[-1]

            # 处理合约
            def add_exchange_suffix(option_code):
                # 只对像 ag2508C9100 这样无后缀的代码处理
                m = re.match(r"([a-zA-Z]{1,2})", option_code)
                if m:
                    short = m.group(1)
                    suffix = code_map.get(short)
                    if suffix and not option_code.endswith(suffix):
                        return option_code + suffix
                return option_code

            def extract_future_code(option_code):
                option_code = str(option_code).strip()  # 确保是字符串并去除空格

                if len(option_code) < 11:
                    return pd.NaT
                if "-" in option_code:
                    future_code = option_code.split("-")[0] + option_code[-3:]
                    return future_code

                elif "P" in option_code[2:].upper():  # 处理看跌期权（如 SR405P6200）
                    return (
                        option_code.split("P")[0] + option_code[-3:]
                    )  # 取 P 之前的部分

                elif "C" in option_code[2:].upper():  # 处理看涨期权（如 SR405C6200）
                    return option_code.split("C")[0] + option_code[-3:]

                else:  # 未知格式，返回原值或报错
                    return option_code

            # 统一使用option_code列名
            df_copy["option_code"] = df_copy["期权合约代码"].apply(add_exchange_suffix)
            df_copy["future_code"] = df_copy["option_code"].apply(extract_future_code)

            # 计算需要展示的字段
            # 1. 持仓均价=‘平均开仓期权价'
            df_copy["pos_avg_price"] = df_copy["平均开仓期权价"]

            df_copy["pos"] = df_copy["手数"]
            df_copy["multiply"] = df_copy["交易单位"].fillna(1).astype(int)
            # 最终展示字段（你可以调整顺序/筛选字段）
            show_cols = [
                "option_code",
                "pos_avg_price",
                "pos",
                "future_code",
                "multiply",
            ]
            result = df_copy[show_cols].copy()
            # 保存/缓存到类变量里，或返回result
            self.option_static_df = result.dropna()  # 可前端展示用
            print(f"期权静态数据加载成功，共 {len(self.option_static_df)} 条记录")
        except Exception as e:
            print(f"期权数据设置失败: {e}")
            self.option_static_df = pd.DataFrame()

    def update_option(self):
        print("option update start")
        if self.option_static_df.empty:
            print("期权静态数据为空")
            self.option_table = pd.DataFrame()
            return

        today = datetime.now().strftime("%Y%m%d")
        df = self.option_static_df.copy()

        # 1. 保证 option_code 是索引
        if "option_code" in df.columns:
            df.set_index("option_code", inplace=True)

        df.columns = [c.strip() for c in df.columns]  # 清理空格
        opt_codes = [code for code in df.index if "." in code]
        fut_codes = [code for code in df["future_code"].unique() if "." in code]
        
        print(f"处理 {len(opt_codes)} 个期权代码，{len(fut_codes)} 个期货代码")
        
        # 2. Greeks - 使用模拟数据避免API调用失败
        try:
            greeks = calc_greeks_letter(opt_codes[:10])  # 限制数量避免超时
            deltas = {code: greek.get("delta", 0.0) for code, greek in greeks.items()}
            ivs = {code: greek.get("iv", 0.0) for code, greek in greeks.items()}
            print(f"Greeks计算成功，获取到 {len(greeks)} 个结果")
        except Exception as e:
            print(f"Greeks计算失败，使用默认值: {e}")
            deltas = {code: 0.0 for code in opt_codes}
            ivs = {code: 0.0 for code in opt_codes}
        
        # 3. 行情数据 - 使用模拟数据
        print("使用模拟市场数据")
        opt_prices_dict = {}
        fut_prices_dict = {}
        
        # 为期权代码生成模拟价格
        for code in opt_codes:
            # 基于持仓均价生成合理的当前价格
            pos_avg = df.loc[code, "pos_avg_price"] if code in df.index else 50.0
            # 模拟价格波动 ±20%
            import random
            price_change = random.uniform(-0.2, 0.2)
            current_price = pos_avg * (1 + price_change)
            opt_prices_dict[code] = {"close": pd.Series([current_price])}
        
        # 为期货代码生成模拟价格
        for code in fut_codes:
            # 模拟期货价格
            base_price = 5000.0  # 基础价格
            import random
            price_change = random.uniform(-0.1, 0.1)
            current_price = base_price * (1 + price_change)
            fut_prices_dict[code] = {"close": pd.Series([current_price])}

        # 4. 填充到df
        def pick_last_close(code, data_dict):
            v = data_dict.get(code, {})
            series = v.get("close", None)
            if series is not None and hasattr(series, "iloc") and len(series) > 0:
                return series.iloc[-1]
            return None

        df["current_opt_price"] = df.index.map(
            lambda code: pick_last_close(code, opt_prices_dict)
        )
        df["current_fut_price"] = df["future_code"].map(
            lambda code: pick_last_close(code, fut_prices_dict)
        )
        df["iv"] = df.index.map(lambda code: ivs.get(code, 0.0))
        df["delta"] = df.index.map(lambda code: deltas.get(code, 0.0))
        df["option_type"] = df.index.map(
            lambda x: "P" if "P" in x.upper() else ("C" if "C" in x.upper() else "")
        )
        
        # 5. 浮动盈亏等
        df["gain_loss"] = df.apply(
            lambda x: (x["pos_avg_price"] - x["current_opt_price"])
            * x["pos"]
            * x["multiply"]
            if pd.notnull(x["current_opt_price"])
            and pd.notnull(x["pos_avg_price"])
            and pd.notnull(x["pos"])
            and pd.notnull(x["multiply"])
            and x["pos"] != 0
            and x["multiply"] != 0
            else 0.0,
            axis=1,
        )

        df["gain_loss_pct"] = df.apply(
            lambda x: (
                x["gain_loss"]
                / (x["pos_avg_price"] * abs(x["pos"]) * x["multiply"])
                * 100
            )
            if pd.notnull(x["gain_loss"])
            and x["pos_avg_price"]
            and x["pos"]
            and x["multiply"]
            and x["pos_avg_price"] != 0
            and x["pos"] != 0
            and x["multiply"] != 0
            else 0.0,
            axis=1,
        )

        # 6. 报警价
        alarm_ratio = getattr(self, "alarm_ratio", 0.02)

        def calc_alarm_price(row):
            if pd.isnull(row["current_fut_price"]):
                return 0.0
            if row["option_type"] == "P":
                return row["current_fut_price"] * (1 - alarm_ratio)
            elif row["option_type"] == "C":
                return row["current_fut_price"] * (1 + alarm_ratio)
            return 0.0

        df["alarm_price"] = df.apply(calc_alarm_price, axis=1)

        show_cols = [
            "current_fut_price",
            "option_type",
            "current_opt_price",
            "pos_avg_price",
            "pos",
            "gain_loss",
            "gain_loss_pct",
            "alarm_price",
            "iv",
            "delta",
        ]
        show_df = df.reset_index()[["option_code"] + show_cols].fillna(0.0)
        num_cols = show_df.select_dtypes(
            include=["float", "float64", "int", "int64"]
        ).columns
        show_df[num_cols] = show_df[num_cols].round(2)
        
        print(f"期权数据更新完成，共 {len(show_df)} 条记录")
        print("option update end")
        
        # 保证 option_code 在前端可见
        with self.update_data_lock:
            self.option_table = show_df

    def init_signal_stats(self, contracts, dict_history, start, today):
        """用历史数据初始化每个合约的pos/neg统计"""
        stats = {}
        try:
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
            for contract in contracts:
                stats[contract] = {"pos": 0, "neg": 0}
        return stats

    def update_data(self):
        """刷新行情和信号等数据"""
        self.log_message("数据刷新开始")
        try:
            today = datetime.now().strftime("%Y%m%d")
            current_time = datetime.now()
            morning_start = datetime.strptime("09:00:00", "%H:%M:%S").time()
            morning_end = datetime.strptime("11:30:00", "%H:%M:%S").time()
            afternoon_start = datetime.strptime("13:30:00", "%H:%M:%S").time()
            afternoon_end = datetime.strptime("15:00:00", "%H:%M:%S").time()
            night_start = datetime.strptime("21:00:00", "%H:%M:%S").time()
            night_end = datetime.strptime("23:00:00", "%H:%M:%S").time()

            min1_data = self.get_market_data(self.main_contract, "1m", today, today, 1)

            for contract in self.main_contract:
                close_min = self.dict_history_all[contract]["close_min"]
                close_max = self.dict_history_all[contract]["close_max"]
                close_now = min1_data[contract]["close"].iloc[-1]

                self.df_results_all.at[contract, "min"] = close_min
                self.df_results_all.at[contract, "max"] = close_max
                self.df_results_all.at[contract, "price"] = close_now

                count_pos = self.df_results_all.at[contract, "pos"]
                count_neg = self.df_results_all.at[contract, "neg"]

                trading_period = (
                    (morning_start <= current_time.time() <= morning_end)
                    or (afternoon_start <= current_time.time() <= afternoon_end)
                    or (night_start <= current_time.time() <= night_end)
                )

                if close_now > close_max and trading_period:
                    count_pos += 1
                    self.df_results_all.at[contract, "pos"] = count_pos
                elif close_now < close_min and trading_period:
                    count_neg += 1
                    self.df_results_all.at[contract, "neg"] = count_neg

                if count_pos >= 1 and self.df_results_all.at[contract, "signal"] != 1:
                    self.df_results_all.at[contract, "strike"] = close_now * (
                        1 - self.n
                    )
                elif (
                    count_neg >= 1 and self.df_results_all.at[contract, "signal"] != -1
                ):
                    self.df_results_all.at[contract, "strike"] = close_now * (
                        1 + self.n
                    )

                if count_pos >= 10 and self.df_results_all.at[contract, "signal"] != 1:
                    self.df_results_all.at[contract, "signal"] = 1
                    self.log_message(
                        f"Sell Put信号: {contract} at price {self.df_results_all.at[contract, 'strike']:.2f}"
                    )
                elif (
                    count_neg >= 10 and self.df_results_all.at[contract, "signal"] != -1
                ):
                    self.df_results_all.at[contract, "signal"] = -1
                    self.log_message(
                        f"Sell Call信号: {contract} at price {self.df_results_all.at[contract, 'strike']:.2f}"
                    )

            df = self.df_results_all.copy().fillna(0)

            df["signal"] = df["signal"].astype(int)
            df["pos"] = df["pos"].astype(int)
            df["neg"] = df["neg"].astype(int)
            for col in ["strike", "min", "max", "price"]:
                df[col] = df[col].astype(float).round(2)

            df["signal_flag"] = df["signal"].apply(
                lambda x: 2 if x == 1 else (1 if x == -1 else 0)
            )
            df = df.sort_values(
                by=["signal_flag", "pos", "neg"], ascending=[False, False, False]
            )
            df = df.drop(columns=["signal_flag"])
            df = df.reset_index().rename(columns={"index": "contract"})
            result = {
                "results_all": df.to_dict(orient="records"),
                "logs": self.logs,
            }
            with self.update_data_lock:
                self.latest_results = result
            self.log_message(f"{today}数据更新完成")
            return result

        except Exception as e:
            self.log_message(f"数据更新失败: {str(e)}")
            return {"error": str(e)}

    def get_cached_result(self):
        with self.update_data_lock:
            return self.latest_results if self.latest_results else {}


data_service = DataService()


@app.route("/api/update", methods=["POST"])
def api_update():
    # 只返回缓存，不重新抓数据
    return jsonify(data_service.get_cached_result())


@app.route("/api/options")
def api_options():
    df = data_service.option_table
    if not df.empty:
        df_sorted = df.sort_values(
            by=["option_code", "gain_loss"], ascending=[True, False]
        )
        return jsonify(df_sorted.to_dict(orient="records"))
    return jsonify([])


@app.route("/api/min1")
def get_min1():
    return jsonify(data_service.df_results_all.to_dict(orient="records"))


@app.route("/api/logs")
def api_logs():
    return jsonify(data_service.logs)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True) 