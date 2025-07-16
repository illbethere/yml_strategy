from strategy_0616 import StrategyManager
from pocess_order import OrderManager
from backtesting import Backtest
from read_data import read_history_file
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class Main:
    def __init__(self):
        pass

    # def read_files(self):

    def single_test(self, catagory):
        INITIAL_CAPITAL = 10000000  # 初始资金
        CONTRACT_SIZE = 300  # 合约大小
        MARGIN_RATE = 0.12  # 保证金率
        MAX_POSITION_RATIO = 0.3  # 单方向最大仓位比例
        FEE_PER_LOT = 5  # 每手手续费
        LOT = 1  # 每次开仓手数
        START_DATE = "20240101"  # 回测开始日期
        END_DATE = "20241231"  # 回测结束日期
        RISK_FREE_RATE = 0.016  # 无风险利率
        SLIP_RATE = 0.0001  # 滑点率

        try:
            order_manager = OrderManager(
                initial_capital=INITIAL_CAPITAL,
                contract_size=CONTRACT_SIZE,
                margin_rate=MARGIN_RATE,
                max_position_ratio=MAX_POSITION_RATIO,
                fee_per_lot=FEE_PER_LOT,
                lot=LOT,
                slip_rate=SLIP_RATE,
            )

            strategy_manager = StrategyManager(order_manager)
            backtest = Backtest(
                initial_capital=INITIAL_CAPITAL, risk_free_rate=RISK_FREE_RATE
            )

            strategy_manager.strategy(
                catagory, START_DATE, END_DATE, 30, 20, lot=LOT, slip=SLIP_RATE
            )

            analysis = backtest.get_detail_analyze(
                pd.DataFrame(order_manager.closed_orders)
            )
            print(analysis)
        except Exception as e:
            print(f"发生错误: {e}")
            import traceback

            traceback.print_exc()

    def parameter_optimization(self):
        INITIAL_CAPITAL = 10000000  # 初始资金
        CONTRACT_SIZE = 300  # 合约大小
        MARGIN_RATE = 0.12  # 保证金率
        MAX_POSITION_RATIO = 0.3  # 单方向最大仓位比例
        FEE_RATE_T1 = 0.000023  # 隔日手续费，万分之0.23
        FEE_RATE_T0 = 0.00023  # 当日手续费，万分之2.3
        LOT = 1  # 每次开仓手数
        START_DATE = "20240101"  # 回测开始日期
        END_DATE = "20241231"  # 回测结束日期
        RISK_FREE_RATE = 0.016  # 无风险利率
        SLIP_RATE = 0.0001  # 滑点率

        try:
            # base_path = r"C:\Users\HP\Desktop\myProject\option_data"
            # df_IF_path = os.path.join(base_path, 'IF.pkl')
            # df_IF = read_history_file(df_IF_path)

            results = []
            total_combinations = 8 * 8
            current_combination = 0

            for k1 in range(10, 50, 5):
                for k2 in range(10, 50, 5):
                    current_combination += 1
                    print(
                        f"Processing {current_combination} / {total_combinations}, K1: {k1}, K2: {k2}"
                    )

                    try:
                        order_manager = OrderManager(
                            initial_capital=INITIAL_CAPITAL,
                            contract_size=CONTRACT_SIZE,
                            margin_rate=MARGIN_RATE,
                            max_position_ratio=MAX_POSITION_RATIO,
                            fee_rate_t1=FEE_RATE_T1,
                            fee_rate_t0=FEE_RATE_T0,
                            slip_rate=SLIP_RATE,
                        )

                        strategy_manager = StrategyManager(order_manager)
                        backtest = Backtest(
                            initial_capital=INITIAL_CAPITAL,
                            risk_free_rate=RISK_FREE_RATE,
                        )

                        strategy_manager.strategy_1(
                            "IF",
                            START_DATE,
                            END_DATE,
                            self.DF_IF,
                            k1=k1,
                            k2=k2,
                            lot=LOT,
                            slip=SLIP_RATE,
                        )

                        analysis = backtest.get_detail_analyze(
                            pd.DataFrame(order_manager.closed_orders)
                        )

                        return_rate = (
                            analysis["总收益率(%)"].values[0]
                            if "总收益率(%)" in analysis.columns
                            else 0
                        )
                        max_drawdown = (
                            analysis["相对最大回撤(%)"].values[0]
                            if "相对最大回撤(%)" in analysis.columns
                            else 0
                        )
                        sharpe_ratio = (
                            analysis["夏普比率"].values[0]
                            if "夏普比率" in analysis.columns
                            else 0
                        )
                        trades_count = len(order_manager.closed_orders)

                        results.append(
                            {
                                "k1": k1,
                                "k2": k2,
                                "return_rate": return_rate,
                                "max_drawdown": max_drawdown,
                                "sharpe_ratio": sharpe_ratio,
                                "trades_count": trades_count,
                            }
                        )

                        equity_data = []
                        current_equity = INITIAL_CAPITAL

                        for order in order_manager.closed_orders:
                            current_equity += order["net_profit"]
                            equity_data.append(
                                {"time": order["close_time"], "equity": current_equity}
                            )

                        picture = self.plt_output(pd.DataFrame(equity_data))

                        # 保存结果到文件夹
                        save_dir = os.path.join("basis_results", str(k1), str(k2))
                        os.makedirs(save_dir, exist_ok=True)

                        # 保存交易数据
                        csv_path = os.path.join(save_dir, "订单簿数据.csv")
                        pd.DataFrame(order_manager.closed_orders).to_csv(
                            csv_path, index=False, encoding="utf-8-sig"
                        )

                        # 保存权益曲线图
                        save_path = os.path.join(
                            save_dir, f"equity_k1_{k1}_k2_{k2}.png"
                        )
                        picture.savefig(save_path, bbox_inches="tight", dpi=300)
                        plt.close(picture)
                    except Exception as e:
                        print(f"处理 K1: {k1}, K2: {k2} 时发生错误: {e}")
                        import traceback

                        traceback.print_exc()

            if results:
                df = pd.DataFrame(results)
                results_path = os.path.join("basis_results", "optimization_results.csv")
                df.to_csv(results_path, index=False, encoding="utf-8-sig")

                self.generate_heatmaps(df)

        except Exception as e:
            print(f"参数优化发生错误: {e}")
            import traceback

            traceback.print_exc()

    def plt_output(self, equity_df, max_time_ticks=30):
        plt.rcParams["font.family"] = ["DejaVu Sans"]
        plt.rcParams["axes.unicode_minus"] = False

        fig = plt.figure(figsize=(14, 7))

        if isinstance(equity_df, pd.DataFrame) and "equity" in equity_df.columns:
            times = pd.to_datetime(equity_df["time"])
            plt.plot(
                times, equity_df["equity"], label="Equity", linewidth=2, color="blue"
            )
        else:
            print("Error: 'equity' column not found")
            return fig

        plt.title("Equity Curve", fontsize=16)
        plt.xlabel("Time", fontsize=14)
        plt.ylabel("Equity", fontsize=14)
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.legend(loc="best")

        ax = plt.gca()
        if max_time_ticks > 0:
            ax.xaxis.set_major_locator(plt.MaxNLocator(max_time_ticks))
        plt.xticks(rotation=45)
        plt.tight_layout()

        return fig

    def generate_heatmaps(self, df):
        try:
            # Create pivot tables
            df_return_rate = df.pivot(index="k1", columns="k2", values="return_rate")
            df_max_drawdown = df.pivot(index="k1", columns="k2", values="max_drawdown")
            df_sharpe_ratio = df.pivot(index="k1", columns="k2", values="sharpe_ratio")

            # Set English font only
            plt.rcParams["font.family"] = ["DejaVu Sans"]
            plt.rcParams["axes.unicode_minus"] = False
            plt.rcParams["font.size"] = 12

            output_dir = "basis_results"
            os.makedirs(output_dir, exist_ok=True)

            colors_return = sns.color_palette("Reds", as_cmap=True)
            colors_return.set_bad(color="lightgrey")

            plt.figure(figsize=(12, 8))
            _heatmap_return = sns.heatmap(
                df_return_rate,
                annot=True,
                fmt=".1f",
                cmap=colors_return,
                annot_kws={"size": 10, "weight": "bold"},
                cbar_kws={"label": "Return Rate (%)"},
            )
            plt.title(
                "Return Rate Heatmap for Different k1 and k2 Combinations",
                fontsize=16,
                pad=20,
            )
            plt.xlabel("k2 (Close Signal Threshold)", fontsize=14)
            plt.ylabel("k1 (Open Signal Threshold)", fontsize=14)

            plt.tight_layout()
            plt.savefig(
                os.path.join(output_dir, "return_rate_heatmap.png"),
                bbox_inches="tight",
                dpi=300,
            )
            plt.close()

            colors_drawdown = sns.color_palette("Blues_r", as_cmap=True)
            colors_drawdown.set_bad(color="lightgrey")

            plt.figure(figsize=(12, 8))
            _heatmap_drawdown = sns.heatmap(
                df_max_drawdown,
                annot=True,
                fmt=".1f",
                cmap=colors_drawdown,
                annot_kws={"size": 10, "weight": "bold"},
                cbar_kws={"label": "Max Drawdown (%)"},
            )
            plt.title(
                "Max Drawdown Heatmap for Different k1 and k2 Combinations",
                fontsize=16,
                pad=20,
            )
            plt.xlabel("k2 (Close Signal Threshold)", fontsize=14)
            plt.ylabel("k1 (Open Signal Threshold)", fontsize=14)

            plt.tight_layout()
            plt.savefig(
                os.path.join(output_dir, "max_drawdown_heatmap.png"),
                bbox_inches="tight",
                dpi=300,
            )
            plt.close()

            colors_sharpe = sns.color_palette("Greens", as_cmap=True)
            colors_sharpe.set_bad(color="lightgrey")

            plt.figure(figsize=(12, 8))
            _heatmap_sharpe = sns.heatmap(
                df_sharpe_ratio,
                annot=True,
                fmt=".2f",
                cmap=colors_sharpe,
                annot_kws={"size": 10, "weight": "bold"},
                cbar_kws={"label": "Sharpe Ratio"},
            )
            plt.title(
                "Sharpe Ratio Heatmap for Different k1 and k2 Combinations",
                fontsize=16,
                pad=20,
            )
            plt.xlabel("k2 (Close Signal Threshold)", fontsize=14)
            plt.ylabel("k1 (Open Signal Threshold)", fontsize=14)

            plt.tight_layout()
            plt.savefig(
                os.path.join(output_dir, "sharpe_ratio_heatmap.png"),
                bbox_inches="tight",
                dpi=300,
            )
            plt.close()

            # Print optimization summary
            # print_optimization_summary(df)

        except Exception:
            import traceback

            traceback.print_exc()


if __name__ == "__main__":
    main = Main()
    # catagory  可选: 'IF', 'IH', 'IC', 'IM'
    main.single_test("IC")
    # main.parameter_optimization()
