from read_data import *
from datetime import datetime, timedelta
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq

def parse_option_code(option_code):
  
    code  = option_code.split('.')[0]
    if '-' in code:
        parts = code.split('-')
        if len(parts) == 3:
            underlying = parts[0]
            option_type = 'call' if parts[1].upper() == 'C' else 'put'
            strike = int(parts[2])
        else:
            import traceback
            traceback.print_exc()

    else:

        call_pos = code.find('C') # 找不到指定字符串的时候返回 -1
        put_pos = code.find('P')

        if call_pos != -1:
            option_type = 'call'
            underlying = code[:call_pos]
            strike = int(code[call_pos + 1:])
        elif put_pos != -1:
            option_type = 'put'
            underlying = code[:put_pos]
            strike = int(code[put_pos + 1:])
        else:
            import traceback
            traceback.print_exc()

    return {
        'option_type': option_type,
        'underlying': underlying,
        'strike': strike,
        'exchange': option_code.split('.')[-1] if '.' in option_code else None
    }

def BS_call(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

    return call_price

def BS_put(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    return put_price

def calc_implied_volatility(market_price, S, K, T, r, option_type):
    if option_type == 'call':
        pricing_func = BS_call
        instrinsic_value = max(S - K, 0)
    else:
        pricing_func = BS_put
        instrinsic_value = max(K - S, 0)

    if market_price <= instrinsic_value:
        print(f"市场价格 {market_price} 小于或等于内在价值 {instrinsic_value}，无法计算隐含波动率")
        return None
    
    def objective_function(sigma):
        try:
            theoretical_price = pricing_func(S, K, T, r, sigma)
            return theoretical_price - market_price
        except Exception as e:
            print(f"计算理论价格时出错: {e}")
            return float('inf')
        
    try:
        sigma = brentq(objective_function, 0.001, 5.0,xtol = 1e-6,  maxiter=100)
        return sigma
    except Exception as e:
        print(f"计算隐含波动率时出错: {e}")
        return None

def calc_hv(option_code: list, days: int = None) -> float:
    if days is None:
        days = 30
    today = datetime.now().strftime('%Y%m%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    data = get_market_data(option_code, '1d', '20230101', today, days + 20)
    # print(data, data[option_code[0]].columns)
    for code in option_code:
        if code not in data:
            print(f"未找到期权代码: {code} 的数据")
            return
        
        df = data[code].copy()

        df = df.sort_values('time')

        df = df[df['close'] > 0].copy()
        if len(df) < days:
            print(f"{code}数据量不足: {len(df)} 行，无法计算历史波动率")
            continue

        df_recent = df.tail(days).copy()

        df_recent['log_return'] = np.log(df_recent['close'] / df_recent['close'].shift(1))

        log_returns = df_recent['log_return'].dropna()

        if len(log_returns) < 2:
            print(f"数据量不足: {len(log_returns)} 行，无法计算历史波动率")
            continue

        hv = log_returns.std()

        print(f"期权代码: {code}，最近 {days} 天的历史波动率: {hv:.4f}")
    return hv



def calc_iv(option_code: list, risk_free_rate: float = None) -> float:
    if risk_free_rate is None:
        risk_free_rate = 0.015

    today = datetime.now().strftime('%Y%m%d')

    data = get_market_data(option_code, '1d', '20230101', today, 10)
    results = {}

    for code in option_code:
        try:
            if code not in data:
                print(f"未找到期权代码: {code} 的数据")
                continue

            option_info = parse_option_code(code)

            underlying_code = option_info['underlying'] + '.' + option_info['exchange']

            underlying_data = get_market_data([underlying_code], '1d', '20230101', today, 10)

            if underlying_code not in underlying_data or underlying_data[underlying_code].empty:
                print(f"未找到标的代码: {underlying_code} 的数据")
                continue

            option_df = data[code].sort_values('time')
            underlying_df = underlying_data[underlying_code].sort_values('time')

            option_price = option_df['close'].iloc[-1]
            underlying_price = underlying_df['close'].iloc[-1]
            strike_price = option_info['strike']
            option_type = option_info['option_type']

            print(f"期权代码: {code}，期权价格: {option_price}, 标的价格: {underlying_price}, 行权价: {strike_price}")

            detail_data = xtdata.get_option_detail_data(code)
            expire_date = detail_data['ExpireDate'].strftime('%Y%m%d')
            if not expire_date:
                print(f"期权代码: {code} 的到期日信息缺失")
                continue
            else:
                days_to_expiration = (datetime.strptime(expire_date, '%Y%m%d') - datetime.now()).days
                print(f"期权代码: {code} 的到期日: {expire_date}, 距离到期天数: {days_to_expiration}")

            # days_to_expiration = 30
            T = days_to_expiration / 365

            sigma = calc_implied_volatility(
                market_price=option_price,
                S=underlying_price,
                K=strike_price,
                T=T,
                r=risk_free_rate,
                option_type=option_type
            )

            if sigma is not None:
                results[code] = {
                    'implied_volatility': sigma,
                    'iv': sigma * 100,
                    'option_price': option_price,
                    'underlying_price': underlying_price,
                    'strike_price': strike_price,
                    'time_to_expiration': T,
                    'option_type': option_type
                }

                print(f"期权代码: {code} 的隐含波动率:({sigma * 100:.2f}%)")
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"处理期权代码 {code} 时出错: {e}")



            









if __name__ == "__main__":
    option_code = ['ag2508P7800.SF', 'cu2507P73000.SF', 'SH509C2560.ZF', 'SR509C6200.ZF', 'a2509-C-4450.DF', 'ps2508-C-36000.GF','ag2508P8000.SF']
    calc_hv(option_code, 90)
    calc_iv(option_code, 0.03)