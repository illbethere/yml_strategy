# venv\Scripts\activate
# python server.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
from datetime import datetime
from xtquant import xtdata, xtdatacenter
import threading
import time
from calc_HV_IV import calc_greeks_letter
# ====== 1. 集成迅投XtTraderPyApi官方下单功能，支持多账户 ======
from 下单类demo_py3_copy import xtTraderApiClient
from XtTraderPyApi import EPriceType, EOperationType
import logging
from XtTraderPyApi import EBrokerLoginStatus

# 在文件开头设置日志
logging.basicConfig(
    filename='xt_api_login.log',  # 日志文件名
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

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
            # 1. 如果是只有一列的DataFrame，取第一列作为list
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

            # 修复 DataFrame 初始化类型问题，强制转换为 pd.Index
            self.main_contract = list(self.main_contract)
            columns_1m = ["signal", "pos", "neg", "strike", "min", "max", "price"]
            self.df_results_all = pd.DataFrame(
                0.0, index=pd.Index(self.main_contract), columns=pd.Index(columns_1m)
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
            
            # 只删除"期权合约代码"列为空的行，而不是删除所有包含NaN的行
            df_copy = df_copy.dropna(subset=["期权合约代码"])
            
            # 删除"日期"列，因为它不是必需的
            if "日期" in df_copy.columns:
                df_copy = df_copy.drop("日期", axis=1)

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
            # 1. 持仓均价=‘平均开仓期权价’
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
        except Exception as e:
            print(e)
            self.option_static_df = pd.DataFrame()

    def update_option(self):
        print("option update start")
        if self.option_static_df.empty:
            self.option_table = pd.DataFrame()
            return

        today = datetime.now().strftime("%Y%m%d")
        df = self.option_static_df.copy()

        # 1. 保证 option_code 是索引
        if "option_code" in df.columns:
            df.set_index("option_code", inplace=True)

        df.columns = [c.strip() for c in df.columns]
        opt_codes = [str(code) for code in df.index if isinstance(code, str) and "." in code]
        fut_code_arr = list(df["future_code"]) if hasattr(df["future_code"], '__iter__') else []
        fut_codes = [str(code) for code in fut_code_arr if isinstance(code, str) and "." in code]

        # 2. Greeks
        try:
            greeks = calc_greeks_letter(opt_codes)
        except Exception as e:
            self.log_message(f"Greeks批量计算失败: {e}")
            greeks = {}

        # 3. 行情数据
        try:
            opt_prices_dict = self.get_market_data(opt_codes, "1d", today, today, 1)
            fut_prices_dict = self.get_market_data(fut_codes, "1d", today, today, 1)
        except Exception as e:
            self.log_message(f"行情批量获取失败: {e}")
            opt_prices_dict = {}
            fut_prices_dict = {}

        def pick_last_close(code, data_dict):
            v = data_dict.get(code, {})
            series = v.get("close", None)
            if hasattr(series, "iloc") and len(series) > 0:
                return float(series.iloc[-1])
            elif isinstance(series, (list, tuple)) and len(series) > 0:
                return float(series[-1])
            elif isinstance(series, (int, float)):
                return float(series)
            return None

        # 逐行处理，只保留全部数据齐全的合约
        results = []
        for code, row in df.iterrows():
            future_code = row["future_code"]
            pos_avg_price = row["pos_avg_price"]
            pos = row["pos"]
            multiply = row["multiply"]

            # 行情
            current_opt_price = pick_last_close(code, opt_prices_dict)
            current_fut_price = pick_last_close(future_code, fut_prices_dict)

            # Greeks
            greek = greeks.get(code, {})
            iv = greek.get("iv", None)
            delta = greek.get("delta", None)

            # option_type
            code_str = str(code)
            option_type = "P" if "P" in code_str.upper() else ("C" if "C" in code_str.upper() else "")

            # 只要有一个数据获取不到，直接跳过
            if (current_opt_price is None or current_fut_price is None or not greek or iv is None or delta is None):
                self.log_message(f"数据不全，跳过: {code}")
                continue

            # 盈亏
            try:
                if (current_opt_price is not None and pos_avg_price is not None and
                    isinstance(pos, (int, float)) and isinstance(multiply, (int, float)) and pos != 0 and multiply != 0):
                    gain_loss = (float(pos_avg_price) - float(current_opt_price)) * float(pos) * float(multiply)
                else:
                    gain_loss = 0.0
            except Exception:
                gain_loss = 0.0

            try:
                valid = True
                for v in [gain_loss, pos_avg_price, pos, multiply]:
                    if isinstance(v, pd.Series):
                        valid = False
                if (valid and gain_loss != 0.0 and isinstance(pos_avg_price, (int, float)) and isinstance(pos, (int, float)) and isinstance(multiply, (int, float)) and pos_avg_price != 0 and pos != 0 and multiply != 0):
                    gain_loss_pct = gain_loss / (float(pos_avg_price) * abs(float(pos)) * float(multiply)) * 100
                else:
                    gain_loss_pct = 0.0
            except Exception:
                gain_loss_pct = 0.0

            # 报警价
            alarm_ratio = getattr(self, "alarm_ratio", 0.02)
            try:
                if current_fut_price is not None:
                    if option_type == "P":
                        alarm_price = float(current_fut_price) * (1 - alarm_ratio)
                    elif option_type == "C":
                        alarm_price = float(current_fut_price) * (1 + alarm_ratio)
                    else:
                        alarm_price = 0.0
                else:
                    alarm_price = 0.0
            except Exception:
                alarm_price = 0.0

            def safe_round(val, n):
                try:
                    return round(float(val), n)
                except Exception:
                    return "-"

            results.append({
                "option_code": code_str,
                "current_fut_price": safe_round(current_fut_price, 2),
                "option_type": option_type,
                "current_opt_price": safe_round(current_opt_price, 2),
                "pos_avg_price": safe_round(pos_avg_price, 2) if pos_avg_price is not None else "-",
                "pos": pos,
                "gain_loss": safe_round(gain_loss, 2),
                "gain_loss_pct": safe_round(gain_loss_pct, 2),
                "alarm_price": safe_round(alarm_price, 2) if alarm_price else "-",
                "iv": safe_round(iv, 4),
                "delta": safe_round(delta, 4),
            })

        show_df = pd.DataFrame(results)
        print("option update end")
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


# ====== 2. 单账户登录，收集子账户 ======
import time
from 下单类demo_py3_copy import xtTraderApiClient
import threading

# 单账户配置
MAIN_ACCOUNT = {
    "server_addr": "183.36.35.2:65300",
    "username": "tbtest",
    "password": "12341234",
}

# 全局变量
xt_api_client = None  # 主账户客户端
sub_accounts = {}  # 子账户信息 {account_id: account_key}

def init_single_account():
    """初始化单账户登录并收集子账户"""
    global xt_api_client, sub_accounts
    
    print("init_single_account线程已启动")
    logging.info("init_single_account线程已启动")
    
    try:
        logging.info(f"准备初始化主账户: {MAIN_ACCOUNT['username']}")
        print(f"准备初始化主账户: {MAIN_ACCOUNT['username']}")
        
        # 创建客户端
        client = xtTraderApiClient(
            MAIN_ACCOUNT["server_addr"], 
            MAIN_ACCOUNT["username"], 
            MAIN_ACCOUNT["password"]
        )
        client.init()
        
        logging.info("已调用init，等待登录")
        print("已调用init，等待登录")
        
        # 等待登录成功
        wait_count = 0
        while not client.m_dictAccountID2Key:
            logging.info(f"当前m_dictAccountID2Key: {client.m_dictAccountID2Key}")
            logging.info(f"当前m_dictAccountKeyStatus: {client.m_dictAccountKeyStatus}")
            time.sleep(1)
            wait_count += 1
            if wait_count % 10 == 0:
                logging.warning("主账户登录等待中...")
                print("主账户登录等待中...")
            if wait_count > 60:  # 60秒超时
                raise Exception("登录超时")
        
        # 收集所有可用的子账户
        sub_accounts.clear()
        for account_id, account_key in client.m_dictAccountID2Key.items():
            status = client.m_dictAccountKeyStatus.get(account_key)
            if status == EBrokerLoginStatus.BROKER_LOGIN_STATUS_OK:
                sub_accounts[account_id] = account_key
                logging.info(f"发现可用子账户: {account_id}")
                print(f"发现可用子账户: {account_id}")
        
        xt_api_client = client
        logging.info(f"主账户登录成功，发现 {len(sub_accounts)} 个子账户")
        print(f"主账户登录成功，发现 {len(sub_accounts)} 个子账户")
        print(f"子账户列表: {list(sub_accounts.keys())}")
        
    except Exception as e:
        logging.error(f"主账户初始化异常: {e}")
        print(f"主账户初始化异常: {e}")
        xt_api_client = None
        sub_accounts.clear()


@app.route("/api/order", methods=["POST"])
def api_order():
    data = request.json or {}
    account_id = data.get("account_id")
    print("sub_accounts keys:", list(sub_accounts.keys()))
    print("收到下单请求 account_id:", account_id)
    contract = data.get("contract")
    price = data.get("price")
    volume = data.get("volume")
    direction = data.get("direction")  # 'buy' or 'sell'
    order_type = data.get("order_type", "future")
    super_price_rate = data.get("super_price_rate", 0)
    remark = data.get("remark", "api下单")

    # 方向映射
    if direction == "buy":
        operation_type = EOperationType.OPT_OPEN_LONG
    elif direction == "sell":
        operation_type = EOperationType.OPT_OPEN_SHORT
    else:
        operation_type = EOperationType.OPT_OPEN_LONG

    order_info = {
        "contract": contract,
        "price": price,
        "volume": volume,
        "direction": direction,
        "order_type": order_type,
        "account_id": account_id,
        "market": "DCE", # 默认市场
        "super_price_rate": super_price_rate,
        "remark": remark,
    }

    try:
        data_service.log_message(f"收到下单请求: {order_info}")
        if xt_api_client and account_id in sub_accounts:
            # 类型保护
            if not contract or price is None or volume is None or not isinstance(contract, str):
                data_service.log_message(f"下单失败: 合约、价格、数量不能为空")
                return jsonify({"status": "fail", "msg": "合约、价格、数量不能为空"})
            account_key = sub_accounts[account_id]
            xt_api_client.future_order(
                str(account_id),
                account_key,
                float(price),
                float(super_price_rate),
                int(volume),
                "DCE", # 默认市场
                str(contract),
                EPriceType.PRTP_FIX,
                operation_type,
                remark=remark
            )
            data_service.log_message(f"官方API下单已发出: {order_info}")
            return jsonify({"status": "ok", "msg": "官方API下单已发出"})
        else:
            data_service.log_message(f"下单失败: 未找到账户 {account_id}")
            return jsonify({"status": "fail", "msg": f"未找到账户 {account_id}"})
    except Exception as e:
        data_service.log_message(f"官方API下单失败: {order_info}, 错误: {str(e)}")
        return jsonify({"status": "fail", "msg": str(e)})

# ====== 撤单接口 ======
@app.route("/api/cancel_order", methods=["POST"])
def api_cancel_order():
    data = request.json or {}
    account_id = data.get("account_id")
    order_id = data.get("order_id")  # 指令号
    try:
        data_service.log_message(f"收到撤单请求: account_id={account_id}, order_id={order_id}")
        if xt_api_client and account_id in sub_accounts:
            account_key = sub_accounts[account_id]
            # 判空和类型保护
            if order_id is None:
                data_service.log_message(f"撤单失败: order_id 不能为空")
                return jsonify({"status": "fail", "msg": "order_id 不能为空"})
            try:
                order_id_int = int(order_id)
            except Exception as e:
                data_service.log_message(f"撤单失败: order_id 转换失败: {order_id}, 错误: {str(e)}")
                return jsonify({"status": "fail", "msg": f"order_id 转换失败: {order_id}"})
            # 调用demo的cancelSync方法（同步撤单，按指令号）
            xt_api_client.cancelSync(order_id_int, account_key)
            data_service.log_message(f"官方API撤单已发出: account_id={account_id}, order_id={order_id}")
            return jsonify({"status": "ok", "msg": "官方API撤单已发出"})
        else:
            data_service.log_message(f"撤单失败: 未找到账户 {account_id}")
            return jsonify({"status": "fail", "msg": f"未找到账户 {account_id}"})
    except Exception as e:
        data_service.log_message(f"官方API撤单失败: account_id={account_id}, order_id={order_id}, 错误: {str(e)}")
        return jsonify({"status": "fail", "msg": str(e)})

# ====== 查单接口 ======
@app.route("/api/query_order", methods=["POST"])
def api_query_order():
    data = request.json or {}
    account_id = data.get("account_id")
    order_id = data.get("order_id")  # 指令号
    try:
        data_service.log_message(f"收到查单请求: account_id={account_id}, order_id={order_id}")
        if xt_api_client and account_id in sub_accounts:
            account_key = sub_accounts[account_id]
            # 查单功能：调用demo的onRtnOrder/onRtnOrderDetail等回调会自动推送最新状态
            # 这里主动查单可用API的查询接口（如有），否则返回"请看主推"
            # 假设有 get_order_status 方法（如无可自定义返回）
            # result = xt_api_client.get_order_status(order_id, account_key)
            # return jsonify({"status": "ok", "order_status": result})
            return jsonify({"status": "ok", "msg": "请查看主推回报，或在日志区查看最新委托状态"})
        else:
            data_service.log_message(f"查单失败: 未找到账户 {account_id}")
            return jsonify({"status": "fail", "msg": f"未找到账户 {account_id}"})
    except Exception as e:
        data_service.log_message(f"官方API查单失败: account_id={account_id}, order_id={order_id}, 错误: {str(e)}")
        return jsonify({"status": "fail", "msg": str(e)})

@app.route("/api/update", methods=["POST"])
def api_update():
    # 返回主表数据和日志
    return jsonify(data_service.get_cached_result())

@app.route("/api/options", methods=["GET"])
def api_options():
    with data_service.update_data_lock:
        df = data_service.option_table
        if df is not None and not df.empty:
            return jsonify(df.to_dict(orient="records"))
        else:
            return jsonify([])

@app.route("/api/accounts", methods=["GET"])
def api_accounts():
    """返回所有可用的子账户列表"""
    if xt_api_client:
        return jsonify([
            {
                "account_id": account_id, 
                "username": xt_api_client.m_strUserName,
                "account_type": xt_api_client.m_dictAccountKey2type.get(account_key, "未知")
            }
            for account_id, account_key in sub_accounts.items()
        ])
    else:
        return jsonify([])

@app.route("/api/account_info", methods=["GET"])
def api_account_info():
    account_id = request.args.get("account_id")
    # mock 数据，后续可接入真实算法
    if not account_id or account_id not in sub_accounts:
        return jsonify({"status": "fail", "msg": "无效账户"})
    # 这里可以根据实际情况返回更多信息
    info = {
        "account_id": account_id,
        "risk": round(0.2 + 0.6 * hash(account_id) % 100 / 100, 2),  # mock 风险度
        "balance": 1000000 + int(account_id) % 10000,  # mock 资金
        "positions": [
            {"symbol": "ag2408", "volume": 10, "profit": 1200},
            {"symbol": "cu2408", "volume": 5, "profit": -800}
        ] if int(account_id) % 2 == 0 else [],
        "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return jsonify({"status": "ok", "data": info})


if __name__ == "__main__":
    print("程序已启动")
    threading.Thread(target=init_single_account, daemon=True).start()
    app.run(host="0.0.0.0", port=5000, debug=False)  # 关闭debug
    print("Flask已退出")
