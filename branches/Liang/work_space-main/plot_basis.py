import pandas as pd
import os
from read_data import *
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter

base_path = r"C:\Users\HP\Documents\LiangDong"
df_IF_path = os.path.join(base_path, 'IF.pkl')
df_IH_path = os.path.join(base_path, 'IH.pkl')
df_IC_path = os.path.join(base_path, 'IC.pkl')
df_IM_path = os.path.join(base_path, 'IM.pkl')

DF_IF = read_history_file(df_IF_path)
DF_IH = read_history_file(df_IH_path)
DF_IC = read_history_file(df_IC_path)
DF_IM = read_history_file(df_IM_path)


def plot_basis(df: pd.DataFrame, start_date: str, end_date: str, max_time_ticks=30):
    plt.rcParams["font.family"] = ["DejaVu Sans"]
    plt.rcParams['axes.unicode_minus'] = False

    # 确保时间列是datetime类型
    df['time'] = pd.to_datetime(df['time'])

    # 按日期范围切片
    mask = (df['time'] >= pd.to_datetime(start_date)) & (df['time'] <= pd.to_datetime(end_date))
    df_sliced = df.loc[mask].copy()

    # 按时间排序
    df_sliced = df_sliced.sort_values('time')

    # 创建连续的数字索引（用于x轴）
    df_sliced['x_index'] = range(len(df_sliced))

    fig, ax = plt.subplots(figsize=(14, 7))

    # 使用连续数字作为x轴
    ax.plot(df_sliced['x_index'], df_sliced['basis'], label='Basis', linewidth=2, color='blue')

    # 设置标题和标签
    ax.set_title('Basis Curve', fontsize=16)
    ax.set_xlabel('Time', fontsize=14)
    ax.set_ylabel('Basis', fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='best')

    # 设置x轴刻度和标签
    if max_time_ticks > 0:
        # 计算步长以控制显示的刻度数量
        step = max(1, len(df_sliced) // max_time_ticks)
        # 设置刻度位置
        ax.set_xticks(df_sliced['x_index'][::step])
        # 设置刻度标签为实际日期
        ax.set_xticklabels(df_sliced['time'].dt.strftime('%Y-%m-%d')[::step], rotation=45)

    plt.tight_layout()
    return fig

# 使用示例
fig = plot_basis(DF_IF, '20220101', '20251231', max_time_ticks=30)

plt.show()