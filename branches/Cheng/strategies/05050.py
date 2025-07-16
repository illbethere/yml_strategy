from read_data import *

code = 'ag2507.SF'
data = get_market_data([code], '1m', '20250101', '20250131', 20000)
print(f"获取到的数据形状: {data[code].shape}")