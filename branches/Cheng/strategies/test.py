from read_data import get_market_data
from datetime import datetime
import pandas as pd

today = datetime.now().date().strftime('%Y%m%d')

# 获取数据
dict_data = get_market_data(['ag2507.SF'], '1m', '20250101', today, 20000)

df = dict_data['ag2507.SF'].copy()

# 先检查数据结构
print("原始数据信息:")
print(f"数据形状: {df.shape}")
print(f"列名: {df.columns.tolist()}")
print(f"索引信息: {df.index}")
print(f"索引名称: {df.index.name}")
print("\n前5行数据:")
print(df.head())
print("\n数据类型:")
print(df.dtypes)

# 修复：始终将索引数据作为'date'列
print("\n将索引数据转换为'date'列")
df = df.reset_index()

# 如果索引有名称，重命名为'date'
if df.columns[0] != 'date':
    df = df.rename(columns={df.columns[0]: 'date'})

print("重置索引后的列名:")
print(df.columns.tolist())

# 将date列转换为字符串格式
if 'date' in df.columns:
    print(f"\n原始date列数据类型: {df['date'].dtype}")
    print("date列前5个值:")
    print(df['date'].head())
    
    # 根据数据类型进行适当的转换
    if pd.api.types.is_datetime64_any_dtype(df['date']):
        # 如果是datetime类型，格式化为YYYYMMDDHHMM
        df['date'] = df['date'].dt.strftime('%Y%m%d%H%M%S')
    else:
        # 如果不是datetime类型，直接转为字符串
        df['date'] = df['date'].astype(str)
    
    print(f"转换后date列数据类型: {df['date'].dtype}")
    print("转换后date列前5个值:")
    print(df['date'].head())

# 检查数据完整性
print(f"\n处理后数据行数: {len(df)}")
print(f"处理后列名: {df.columns.tolist()}")
print("处理后前5行数据:")
print(df.head())

# 删除任何可能的空值行
df_clean = df.dropna().reset_index(drop=True)
print(f"\n清理后数据行数: {len(df_clean)}")

# 保存数据
output_file = r'C:\Users\HP\Desktop\myProject\strategies\data\ag2507_data.csv'

try:
    # 确保所有数据都是有效的
    df_clean = df_clean.fillna(0)  # 填充任何剩余的空值
    
    # 保存文件 - 不保存索引
    df_clean.to_csv(output_file, index=False, encoding='utf-8', lineterminator='\n')
    print(f"\n✓ 数据已保存到: {output_file}")
    
    # 验证保存的文件
    saved_data = pd.read_csv(output_file)
    print(f"✓ 文件验证: 保存了 {len(saved_data)} 条记录")
    print(f"✓ 保存文件的列名: {saved_data.columns.tolist()}")
    print("✓ 保存文件前5行:")
    print(saved_data.head())
    
    # 检查是否有空行
    with open(output_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    empty_lines = [i for i, line in enumerate(lines) if line.strip() == '']
    if empty_lines:
        print(f"⚠️ 发现空行在第 {empty_lines} 行")
        
        # 自动修复空行
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 移除空行
        lines = [line for line in content.split('\n') if line.strip()]
        
        # 重新保存
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print("✓ 空行已自动修复")
    else:
        print("✓ 文件中没有空行")
        
except Exception as e:
    print(f"❌ 保存失败: {e}")
    
    # 显示调试信息
    print("\n调试信息:")
    print(f"DataFrame形状: {df_clean.shape}")
    print(f"DataFrame列: {df_clean.columns.tolist()}")
    print(f"DataFrame数据类型:\n{df_clean.dtypes}")

print(f"\n数据获取完成，字典键: {list(dict_data.keys())}")