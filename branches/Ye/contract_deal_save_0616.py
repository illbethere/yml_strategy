# -*- coding: utf-8 -*-
# 数据读写于“./data/”目录下
from xtquant import xtdatacenter as xtdc
from xtquant import xtdata
import pandas as pd
from datetime import datetime

xtdc.set_token("4065054877ce5724155dbc5bcba200381ce5eb35")
xtdc.init()


class G:
    def __init__(self):
        self.path = "./data/"
        self.today = datetime.today().strftime("%Y%m%d")


g = G()


def get_market_data(
    codes: list, period: str, start_time: str, end_time: str, count: int
) -> dict:
    """获取市场数据"""
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


def read_contract_deal(contract_deal_path: str):
    try:
        # read_path = g.path + f"成交记录_{date}.csv"
        read_path = contract_deal_path
        df = pd.read_csv(read_path, encoding="gbk")
        return df
    except Exception as e:
        print(e)


def read_yesterday_report(yesaterday_report_path: str):
    try:
        # read_path = g.path + f"成交记录_{date}.csv"
        df_own = pd.read_excel(yesaterday_report_path, sheet_name="持有")
        df_close_order = pd.read_excel(yesaterday_report_path, sheet_name="已平仓")
        df_total_gain_loss = pd.read_excel(yesaterday_report_path, sheet_name="总盈亏")
        return df_own, df_close_order, df_total_gain_loss
    except Exception as e:
        print(e)
        return (pd.DataFrame, pd.DataFrame, pd.DataFrame)


def daily_report_contract_deal(contract_deal):
    df = read_contract_deal(contract_deal)
    output_df = df.copy()
    # 重置索引并确保索引唯一
    output_df = output_df.reset_index(drop=True)

    # 检查是否有重复的索引
    if output_df.index.duplicated().any():
        print("发现重复索引，重新设置索引")
        output_df = output_df.reset_index(drop=True)

    def get_market_name(name):
        if name == "上期所":
            return "SF"
        elif name == "大商所":
            return "DF"
        elif name == "郑商所":
            return "ZF"
        elif name == "中金所":
            return "CF"
        elif name == "广交所":
            return "GF"
        elif name == "上海国际能源交易中心":
            return "INE"
        else:
            print(f"未知市场名称: {name}")
            return "UNKNOWN"

    def get_multiplier(name):
        try:
            detail = xtdata.get_option_detail_data(name)
            if detail is not None:
                return detail.get("VolumeMultiple", None)
            else:
                print(f"{name} 获取option detail数据失败: 返回None")
                return None
        except Exception as e:
            print(f"{name} 获取VolumeMultiple失败: {e}")
            return None

    def get_object_price(name, time):
        today = g.today
        time = str(time)
        try:
            option_detail = xtdata.get_option_detail_data(name)
            object_code = (
                option_detail["OptUndlCode"] + "." + option_detail["OptUndlMarket"]
            )
            data = get_market_data([object_code], "tick", "20250604", today, -1)[
                object_code
            ]
            data = data[~data.index.duplicated(keep="last")]
            value = data.loc[time, "lastPrice"]
            return value
        except Exception as e:
            print(e)
            return 0

    def get_manager(market):
        if market == "上期所" or market == "广交所":
            return "程"
        elif market == "大商所" or market == "上海国际能源交易中心":
            return "叶"
        elif market == "郑商所":
            return "梁"
        else:
            print(f"未知市场名称: {market}")
            return "UNKNOWN"

    output_df["market"] = output_df["交易所"].apply(get_market_name)
    output_df["手数"] = output_df["成交手数"].astype(int)
    output_df["成交价格"] = output_df["成交价格"].astype(float)
    output_df["name"] = output_df["合约"] + "." + output_df["market"]
    output_df["交易单位"] = output_df["name"].apply(get_multiplier)
    output_df["手续费"] = output_df["手续费"].astype(float)
    output_df["time"] = pd.to_datetime(
        "20250611" + " " + output_df["成交时间"], format="%Y%m%d %H:%M:%S"
    ).dt.strftime("%Y%m%d%H%M%S")

    object_prices = []
    for idx, row in output_df.iterrows():
        try:
            price = get_object_price(row["name"], row["time"])
            object_prices.append(price)
        except Exception as e:
            print(f"获取object_price失败 (行{idx}): {e}")
            object_prices.append(0)

    output_df["标的价格"] = object_prices

    output_df["期权合约代码"] = output_df["合约"]

    column_chosed = [
        "期权合约代码",
        "负责人",
        "手数",
        "成交价格",
        "手续费",
        "交易单位",
        "标的价格",
    ]

    output_df["负责人"] = output_df["交易所"].apply(get_manager)
    output_df = output_df.rename(
        columns={
            "期权合约代码": "期权合约代码",
            "负责人": "负责人",
            "手数": "手数",
            "成交价格": "平均开仓期权价",
            "手续费": "手续费",
            "交易单位": "交易单位",
            "标的价格": "成交期货平均价",
        }
    )

    df_open = output_df[output_df["开平"] == "开仓"].copy()
    df_close = output_df[output_df["开平"] == "平仓"].copy()

    return df_open[column_chosed], df_close[column_chosed]


def merge_contract_deal(
    df_open: pd.DataFrame, df_close: pd.DataFrame, yesaterday_report_path: str
):
    df_own_tuple = read_yesterday_report(yesaterday_report_path)
    # df_own_tuple is a tuple: (df_own, df_close_order, df_total_gain_loss)
    df_own = df_own_tuple[0]

    if not isinstance(df_own, pd.DataFrame):
        print("历史报告读取出错")
        return None

    def get_final_option_price(codes: list[str]):
        final_list = get_market_data(codes, "1d", g.today, g.today, 1)
        return {code: final_list[code]["close"] for code in codes}

    # 提取需要的列
    yesterday_report = df_own[
        [
            "期权合约代码",
            "负责人",
            "手数",
            "平均开仓期权价",
            "交易单位",
            "手续费",
            "成交期货平均价",
        ]
    ]

    # 合并数据
    combined = pd.concat([df_open, yesterday_report], ignore_index=True)
    codes = combined["期权合约代码"].unique().tolist()
    final_price_dict = get_final_option_price(codes)
    combined["期权收盘价"] = combined["期权合约代码"].map(final_price_dict)

    # 定义聚合函数
    agg_funcs = {
        "负责人": "first",
        "手数": "sum",
        "平均开仓期权价": lambda x: (x * combined.loc[x.index, "手数"]).sum()
        / combined.loc[x.index, "手数"].sum(),
        "当日收盘价（15:00）": "first",
        "成交期货平均价": lambda x: (x * combined.loc[x.index, "手数"]).sum()
        / combined.loc[x.index, "手数"].sum(),
        "交易单位": "first",
        "手续费": "sum",
    }

    # 分组聚合
    merged = combined.groupby("期权合约代码", as_index=False).agg(agg_funcs)

    return merged


def save_contract_deal(df):
    save_path = g.path + f"contract_deal_{g.today}.csv"
    if not isinstance(df, pd.DataFrame):
        print("传入的参数不是DataFrame类型")
        return
    df.to_csv(
        save_path,
        index=False,
        mode="w",
        encoding="utf-8-sig",
    )
    print(f"合约成交数据已保存到 {save_path}")


if __name__ == "__main__":
    contract_deal_path = g.path + f"成交记录_250611.csv"
    yesaterday_report_path = g.path + "每日报告_20250610.xlsx"
    contract_deal_open, contract_deal_close = daily_report_contract_deal(
        contract_deal_path
    )
    print("合约成交数据处理完成！")
    print(contract_deal_open, contract_deal_close)
    merge = merge_contract_deal(
        contract_deal_open, contract_deal_close, yesaterday_report_path
    )
    print(merge)
