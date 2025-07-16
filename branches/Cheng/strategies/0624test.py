import numpy as np
from pysabr import Hagan2002LognormalSABR
import matplotlib.pyplot as plt

# 1. 市场参数
S = 4792      # 标的现货价格 (Spot)
T = 0.2460    # 年化到期时间 (Maturity in years)
r = 0.02      # 无风险利率 (Risk-free rate)
sigma_atm_ln = 0.20 # 市场的ATM对数正态波动率 (Lognormal ATM Vol)

# SABR模型参数
beta = 0.7    # 建议的股票期权beta值
rho = -0.07   # 价格-波动率相关性
volvol = 0.4 # 波动率的波动率

# 2. 计算远期价格和ATM正态波动率 (核心修正)
f = S * np.exp(r * T)
# 将市场标准的对数正态ATM波动率转换为模型需要的正态ATM波动率
# Normal Vol ≈ Lognormal Vol * Forward Price
v_atm_n = sigma_atm_ln * f

# 3. 初始化SABR模型
sabr_ln = Hagan2002LognormalSABR(
    f=f, t=T, v_atm_n=v_atm_n, beta=beta, rho=rho, volvol=volvol
)

# 4. 定义一系列行权价，以观察整个波动率微笑曲线 (*** 这是修正的部分 ***)
# 使用 np.linspace 创建一个从 4200 到 5800，包含 20 个点的行权价数组
strikes = np.linspace(4200, 5800, num=20)

# 5. 计算每个行权价对应的对数正态隐含波动率
lognormal_vols = [sabr_ln.lognormal_vol(k) for k in strikes]

print("行权价 (Strikes):")
print(np.round(strikes, 2))
print("\n对应的对数正态隐含波动率 (Implied Lognormal Vols):")
print(np.round(lognormal_vols, 4))


# 6. 绘制波动率微笑曲线
plt.figure(figsize=(10, 6))
plt.plot(strikes, lognormal_vols, 'bo-', label='SABR Implied Volatility Smile')
# 标记ATM点
plt.axvline(x=f, color='r', linestyle='--', label=f'Forward Price (ATM) = {f:.2f}')
plt.title(f'SABR Volatility Smile (Beta={beta})')
plt.xlabel('Strike Price (K)')
plt.ylabel('Implied Lognormal Volatility')
plt.grid(True)
plt.legend()
plt.show()