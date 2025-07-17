import os
import re
from datetime import datetime, timedelta
import pandas as pd
from xtquant import xtdatacenter as xtdc
from xtquant import xtdata

# ========== 初始化 ==========
xtdc.set_token("4065054877ce5724155dbc5bcba200381ce5eb35")
xtdc.init()


class G:
    def __init__(self):
        self.path = "./data/"
        self.today = datetime.today().strftime("%Y%m%d")


g = G()


# ========== 通用工具 ==========
def safe_read_csv(path, encoding="gbk"):
    try:
        df = pd.read_csv(path, encoding=encoding)
        return df
    except Exception as e:
        print(f"[读CSV失败] {path}: {e}")
        return pd.DataFrame()


def safe_read_excel(path, **kwargs):
    try:
        df = pd.read_excel(path, **kwargs)
        return df
    except Exception as e:
        print(f"[读Excel失败] {path}: {e}")
        return pd.DataFrame()


def safe_to_csv(df, path, **kwargs):
    try:
        df.to_csv(path, **kwargs)
        print(f"[保存CSV] {path}")
    except Exception as e:
        print(f"[保存CSV失败] {path}: {e}")


# ========== 行情与合约对照 ==========
def load_code_market_map(code_txt_path="./data/code.txt"):
    code_map = {}
    try:
        with open(code_txt_path, "r", encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if "." in s:
                    code, market = s.split(".")
                    code = code.split("0")[0]
                    code_map[code] = market
    except Exception as e:
        print(f"[读取合约对照表失败] {e}")
    return code_map


def code_to_full(code, code_map, default_market="SF"):
    if not isinstance(code, str) or pd.isna(code) or code.strip() == "":
        return ""
    if "." in code:
        return code
    m = re.match(r"([A-Za-z]{1,2})", code)
    if m:
        prefix = m.group(1)
        market = code_map.get(prefix, default_market)
        return f"{code}.{market}"
    else:
        return f"{code}.{default_market}"


def get_market_data(
    codes: list, period: str, start_time: str, end_time: str, count: int
) -> dict:
    for code in codes:
        xtdata.subscribe_quote(code, period, start_time, end_time, count, callback=None)
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
            print(f"数据 {code} 获取失败！")
            break
    return market_data


def get_latest_option_close(code_list, code_map):
    code_full_list = [code_to_full(c, code_map) for c in code_list]
    mdict = get_market_data(code_full_list, "1d", g.today, g.today, 1)
    result = {}
    for fullcode in code_full_list:
        df = mdict.get(fullcode, None)
        code_base = fullcode.split(".")[0]
        if df is None:
            print(f"[WARN] {fullcode}: 行情接口返回None")
            result[code_base] = float("nan")
        elif not isinstance(df, pd.DataFrame):
            print(
                f"[WARN] {fullcode}: 返回类型不是DataFrame，实际是{type(df)}，内容为{df}"
            )
            result[code_base] = float("nan")
        elif df.empty:
            print(f"[WARN] {fullcode}: DataFrame为空")
            result[code_base] = float("nan")
        elif "close" not in df.columns:
            print(f"[WARN] {fullcode}: DataFrame无close列，columns={df.columns}")
            result[code_base] = float("nan")
        else:
            close_val = df["close"].iloc[-1]
            result[code_base] = (
                float(close_val) if pd.notnull(close_val) else float("nan")
            )
    return result


# ========== 读取/标准化 成交/持仓 ==========
def read_contract_deal(contract_deal_path):
    df = safe_read_csv(contract_deal_path)
    if df.empty:
        print("[读取成交记录失败] 路径:", contract_deal_path)
    return df


def read_yesterday_report(yesaterday_report_path):
    df_own = safe_read_excel(yesaterday_report_path, sheet_name="持有")
    df_close = safe_read_excel(yesaterday_report_path, sheet_name="已平仓")
    df_total = safe_read_excel(yesaterday_report_path, sheet_name="总盈亏")
    return df_own, df_close, df_total


def standardize_contract_deal(df):
    if df.empty:
        return pd.DataFrame(), pd.DataFrame()
    df = df.copy()
    market_map = {
        "上期所": "SF",
        "大商所": "DF",
        "郑商所": "ZF",
        "中金所": "CF",
        "广期所": "GF",
        "上海国际能源交易中心": "INE",
    }
    manager_map = {
        "上期所": "程",
        "广期所": "程",
        "大商所": "叶",
        "上海国际能源交易中心": "叶",
        "郑商所": "梁",
    }
    df["market"] = df["交易所"].map(market_map).fillna("UNKNOWN")
    df["负责人"] = df["交易所"].map(manager_map).fillna("UNKNOWN")
    df["手数"] = df["成交手数"].astype(int)
    df["成交价格"] = df["成交价格"].astype(float)
    df["name"] = df["合约"] + "." + df["market"]

    def get_multiplier(name):
        try:
            detail = xtdata.get_option_detail_data(name)
            if detail is not None:
                return detail.get("VolumeMultiple", None)
        except Exception as e:
            pass
        return None

    df["交易单位"] = df["name"].apply(get_multiplier)
    df["手续费"] = df["手续费"].astype(float)
    df["time"] = pd.to_datetime(
        g.today + " " + df["成交时间"], format="%Y%m%d %H:%M:%S"
    ).dt.strftime("%Y%m%d%H%M%S")
    df["期权合约代码"] = df["合约"]
    df = df.rename(
        columns={
            "期权合约代码": "期权合约代码",
            "负责人": "负责人",
            "手数": "手数",
            "成交价格": "平均开仓期权价",
            "手续费": "手续费",
            "交易单位": "交易单位",
        }
    )
    columns_chose = [
        "期权合约代码",
        "负责人",
        "手数",
        "平均开仓期权价",
        "手续费",
        "交易单位",
        "开平",  # 保留成交价格给平仓均价用
    ]
    # 若"成交价格"已被rename，仍可用
    for c in columns_chose:
        if c not in df.columns:
            df[c] = None
    df = df[columns_chose]
    df_open = df[df["开平"] == "开仓"].copy()
    df_close = df[df["开平"] == "平仓"].copy()
    df_open = df_open.drop(columns=["开平"])
    df_close = df_close.drop(columns=["开平"])
    return df_open, df_close


def standardize_yesterday(df):
    col_map = {
        "期权合约代码": "期权合约代码",
        "负责人": "负责人",
        "手数": "手数",
        "平均开仓期权价": "平均开仓期权价",
        "手续费（买入）": "手续费",
        "交易单位": "交易单位",
    }
    df = df.rename(columns=col_map)
    df = df.drop(columns=["日期"])
    df = df.dropna()
    return df[list(col_map.values())]


# ========== 合并核心 ==========
def merge_contract_deal(
    df_open: pd.DataFrame, yesaterday_report_path: str, code_map: dict
):
    df_own, _, _ = read_yesterday_report(yesaterday_report_path)
    if df_own.empty and df_open.empty:
        print("[无可合并数据]")
        return pd.DataFrame()
    if not df_own.empty:
        df_own = standardize_yesterday(df_own)
    combined = pd.concat([df_open, df_own], ignore_index=True)
    combined = combined[combined["期权合约代码"].notnull()].copy()
    combined["期权合约代码"] = combined["期权合约代码"].astype(str)
    combined["full_code"] = combined["期权合约代码"].map(
        lambda x: code_to_full(x, code_map)
    )
    code_base_list = combined["期权合约代码"].unique().tolist()
    price_dict = get_latest_option_close(code_base_list, code_map)
    combined["期权收盘价"] = combined["期权合约代码"].map(price_dict)

    def weighted_avg(df, avg_col, weight_col):
        s = df[weight_col].sum()
        return (df[avg_col] * df[weight_col]).sum() / s if s else 0

    agg_dict = {
        "负责人": "first",
        "手数": "sum",
        "平均开仓期权价": lambda x: weighted_avg(
            combined.loc[x.index], "平均开仓期权价", "手数"
        ),
        "期权收盘价": "first",
        "交易单位": "first",
        "手续费": "sum",
    }
    merged = combined.groupby("期权合约代码", as_index=False).agg(agg_dict)
    merged = (
        merged[
            [
                "期权合约代码",
                "负责人",
                "手数",
                "平均开仓期权价",
                "期权收盘价",
                "交易单位",
                "手续费",
            ]
        ]
        .sort_values("期权合约代码")
        .reset_index(drop=True)
    ).round(2)
    merged["总盈亏"] = (merged["平均开仓期权价"] - merged["期权收盘价"]) * merged[
        "交易单位"
    ] * merged["手数"] - merged["手续费"]
    return merged


# ========== 已平仓核心算法 ==========
def calculate_closed_positions_by_merge(df_yesterday, df_today_open, df_today_close):
    # 1. 可用持仓合并
    df_available = pd.concat([df_yesterday, df_today_open], ignore_index=True)
    df_available = df_available.groupby("期权合约代码", as_index=False).agg({
        "负责人": "first",
        "手数": "sum",
        "平均开仓期权价": "first",
        "交易单位": "first",
        "手续费": "sum"
    })

    # 2. 平仓明细聚合
    def weighted_avg(group):
        s = group["手数"].sum()
        return (group["平均开仓期权价"] * group["手数"]).sum() / s if s else 0

    df_close_agg = df_today_close.groupby("期权合约代码", as_index=False).apply(
        lambda g: pd.Series({
            "平仓手数": g["手数"].sum(),
            "平仓均价": weighted_avg(g),
            "平仓手续费": g["手续费"].sum()
        })
    ).reset_index(drop=True)

    # 3. merge合并
    df_merged = pd.merge(
        df_available,
        df_close_agg,
        on="期权合约代码",
        how="inner"
    )
    df_merged["手续费"] = df_merged["手续费"] + df_merged["平仓手续费"]
    df_merged["净盈亏"] = (
        (df_merged["平均开仓期权价"] - df_merged["平仓均价"]) *
        df_merged["平仓手数"] * df_merged["交易单位"] -
        df_merged["手续费"]
    )
    # 只保留有平仓的
    df_closed = df_merged[df_merged["平仓手数"] > 0].copy()

    return df_closed[
        [
            "期权合约代码", "负责人", "平仓手数", "平均开仓期权价",
            "平仓均价", "交易单位", "手续费", "净盈亏"
        ]
    ]

def save_to_excel_with_sheets(path, df1, df2, sheet1="持有", sheet2="已平仓"):
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df1.to_excel(writer, sheet_name=sheet1, index=False)
        df2.to_excel(writer, sheet_name=sheet2, index=False)
    print(f"[Excel导出] {path} 已生成 {sheet1}, {sheet2}")


# ========== 入口与调度 ==========
if __name__ == "__main__":
    date = datetime.today().strftime("%y%m%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")

    contract_deal_path = os.path.join(g.path, f"成交记录_{date}.csv")
    yesaterday_report_path = os.path.join(g.path, f"对冲3号金石期货_{yesterday}.xlsx")
    code_map = load_code_market_map()

    df_deal = read_contract_deal(contract_deal_path)
    contract_deal_open, contract_deal_close = standardize_contract_deal(df_deal)
    print("[今日开仓]:\n", contract_deal_open)
    print("[今日平仓]:\n", contract_deal_close)
    safe_to_csv(
        contract_deal_open,
        os.path.join(g.path, f"成交记录_{date}_open.csv"),
        encoding="utf-8-sig",
        index=False,
    )
    safe_to_csv(
        contract_deal_close,
        os.path.join(g.path, f"成交记录_{date}_close.csv"),
        encoding="utf-8-sig",
        index=False,
    )

    merged = merge_contract_deal(contract_deal_open, yesaterday_report_path, code_map)
    df_own, _, _ = read_yesterday_report(yesaterday_report_path)
    if not df_own.empty:
        df_own = standardize_yesterday(df_own)
    else:
        df_own = pd.DataFrame()
    df_closed = calculate_closed_positions_by_merge(
        merged, contract_deal_open, contract_deal_close
    )
    merged = merged.sort_values("期权合约代码", axis=0, ascending=True)
    if merged is not None and not merged.empty:
        print("[合并后持仓]:\n", merged)
        print("平仓：", df_closed)
        save_to_excel_with_sheets(
            os.path.join(g.path, f"持仓汇总_{g.today}.xlsx"),
            merged,
            df_closed,
            sheet1="持有",
            sheet2="已平仓",
        )
    else:
        print("[无合并持仓数据]")
