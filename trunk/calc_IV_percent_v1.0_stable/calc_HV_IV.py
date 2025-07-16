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
    if isinstance(option_code, str):
        option_code = [option_code]
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
    if hv is not None:
        return hv
    else:
        print(f"期权代码: {code} 的历史波动率计算失败")
        return None



def calc_iv(option_code: list, date: str, risk_free_rate: float = None) -> float:
    if risk_free_rate is None:
        risk_free_rate = 0.02

    if isinstance(option_code, str):
        option_code = [option_code]

    pre_date = (datetime.strptime(date, '%Y%m%d') - timedelta(days=10)).strftime('%Y%m%d')

    # today = datetime.now().strftime('%Y%m%d')

    data = get_market_data(option_code, '1d', pre_date, date, 1)
    # print(data)
    results = {}

    for code in option_code:
        try:
            if code not in data:
                print(f"未找到期权代码: {code} 的数据")
                continue

            option_info = parse_option_code(code)

            underlying_code = option_info['underlying'] + '.' + option_info['exchange']

            underlying_data = get_market_data([underlying_code], '1d', pre_date, date, 1)
            # print("+++++++++++++++++++",underlying_code)

            if underlying_code not in underlying_data or underlying_data[underlying_code].empty:
                print(f"未找到标的代码: {underlying_code} 的数据")
                continue

            option_df = data[code].sort_values('time')
            underlying_df = underlying_data[underlying_code].sort_values('time')

            option_price = option_df['close'].iloc[-1]
            underlying_price = underlying_df['close'].iloc[-1]
            strike_price = option_info['strike']
            option_type = option_info['option_type']

            # print(f"期权代码: {code}，期权价格: {option_price}, 标的价格: {underlying_price}, 行权价: {strike_price}")

            detail_data = xtdata.get_option_detail_data(code)
            expire_date = detail_data['ExpireDate']
            # print(f"期权代码: {code} 的到期日: {expire_date}")
            if not expire_date:
                print(f"期权代码: {code} 的到期日信息缺失")
                continue
            else:
                days_to_expiration = (datetime.strptime(expire_date, '%Y%m%d') - datetime.strptime(date, '%Y%m%d')).days
                # print(f"期权代码: {code} 的到期日: {expire_date}, 距离到期天数: {days_to_expiration}")

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

                # print(f"期权代码: {code} 的隐含波动率:({sigma * 100:.2f}%)")

            
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"处理期权代码 {code} 时出错: {e}")
    return results


def calc_gamma(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))

    return gamma


def calc_delta(S, K, T, r, sigma, option_type):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

    if option_type == 'call':
        delta = norm.cdf(d1)
    else:
        delta = norm.cdf(d1) - 1
        
    return delta

def calc_vega(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T)

    return vega / 100

def clac_theta(S, K, T, r, sigma, option_type):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
    else:
        theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365

    return theta

def calc_rho(S, K, T, r, sigma, option_type):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        rho = K * T * np.exp(-r * T) * norm.cdf(d2) / 100
    else:
        rho = -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100

    return rho

def american_option_binomial(S, K, T, r, sigma, option_type, n=100):
    dt = T / n
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)
    discount = np.exp(-r * dt)

    stock_prices = np.zeros((n + 1, n + 1))
    for i in range(n + 1):
        for j in range(i + 1):
            stock_prices[j , i] = S * (u ** (i - j)) * (d ** j)

    option_values = np.zeros((n + 1, n + 1))
    for j in range(n + 1):
        if option_type == 'call':
            option_values[j, n] = max(0, stock_prices[j, n] - K)
        else:
            option_values[j, n] = max(0, K - stock_prices[j, n])

    for i in range(n - 1, -1, -1):
        for j in range(i + 1):
            hold_value = discount * (p * option_values[j, i + 1] + (1 - p) * option_values[j + 1, i + 1])

            if option_type == 'call':
                exercise_value = max(0, stock_prices[j, i] - K)
            else:
                exercise_value = max(0, K - stock_prices[j, i])

            option_values[j, i] = max(hold_value, exercise_value)
        
    return option_values[0, 0]

def calc_american_option_greeks(S, K, T, r, sigma, option_type):
    price_func = lambda s, k, t, rate, vol, opt_type: american_option_binomial(s, k, t, rate, vol, opt_type)

    base_price = price_func(S, K, T, r, sigma, option_type)

    dS = S * 0.001
    price_up = price_func(S + dS, K, T, r, sigma, option_type)
    price_down = price_func(S - dS, K, T, r, sigma, option_type)
    delta = (price_up - price_down) / (2 * dS)

    gamma = (price_up - 2 * base_price + price_down) / (dS ** 2)

    dT = 1/365
    if T > dT:
        price_tomorrow = price_func(S, K, T - dT, r, sigma, option_type)
        theta = -(base_price - price_tomorrow)
    else:
        theta = 0

    dsigma = 0.001
    price_vega = price_func(S, K, T, r, sigma + dsigma, option_type)
    vega = (price_vega - base_price) / dsigma

    dr = 0.001
    price_rho = price_func(S, K, T, r + dr, sigma, option_type)
    rho = (price_rho - base_price) / dr

    return {
        'price': base_price,
        'delta': delta,
        'gamma': gamma,
        'theta': theta,
        'vega': vega / 100,
        'rho': rho / 100
    }

def calc_greeks_letter(option_code, risk_free_rate = None) -> dict:
    if risk_free_rate is None:
        risk_free_rate = 0.02

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
            opiton_type = option_info['option_type']

            detail_data = xtdata.get_option_detail_data(code)
            expire_date = detail_data['ExpireDate']
            if not expire_date:
                print(f"期权代码: {code} 的到期日信息缺失")
                continue
            else:
                days_to_expiration = (datetime.strptime(expire_date, '%Y%m%d') - datetime.now()).days

            T = days_to_expiration / 365

            sigma = calc_implied_volatility(
                market_price=option_price,
                S=underlying_price,
                K=strike_price,
                T=T,
                r=risk_free_rate,
                option_type=opiton_type
            )

            if sigma is not None:
                gamma = calc_gamma(
                    S=underlying_price,
                    K=strike_price,
                    T=T,
                    r=risk_free_rate,
                    sigma=sigma
                )
                delta = calc_delta(
                    S=underlying_price,
                    K=strike_price,
                    T=T,
                    r=risk_free_rate,
                    sigma=sigma,
                    option_type=opiton_type
                )
                vega = calc_vega(
                    S=underlying_price,
                    K=strike_price,
                    T=T,
                    r=risk_free_rate,
                    sigma=sigma
                )

                theta = clac_theta(
                    S=underlying_price,
                    K=strike_price,
                    T=T,
                    r=risk_free_rate,
                    sigma=sigma,
                    option_type=opiton_type
                )

                rho = calc_rho(
                    S=underlying_price,
                    K=strike_price,
                    T=T,
                    r=risk_free_rate,
                    sigma=sigma,
                    option_type=opiton_type
                )


                results[code] = {
                    'implied_volatility': sigma,
                    'iv': sigma * 100,
                    'option_price': option_price,
                    'underlying_price': underlying_price,
                    'strike_price': strike_price,
                    'time_to_expiration': T,
                    'option_type': opiton_type,
                    'gamma': gamma,
                    'delta': delta,
                    'vega': vega,
                    'theta': theta,
                    'rho': rho
                }

                print(f"期权代码: {code} 的希腊字母值:")
                print(f"  隐含波动率: {sigma * 100:.2f}%")
                print(f"  Delta: {delta:.4f}")
                print(f"  Gamma: {gamma:.4f}")
                print(f"  Vega: {vega:.4f}")
                print(f"  Theta: {theta:.4f}")
                print(f"  Rho: {rho:.4f}")


        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"处理期权代码 {code} 时出错: {e}")
        
    return results

def calc_american_greeks_letter(option_code, risk_free_rate = None):
    if risk_free_rate is None:
        risk_free_rate = 0.02

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
            opiton_type = option_info['option_type']

            detail_data = xtdata.get_option_detail_data(code)
            if detail_data is None or 'ExpireDate' not in detail_data:
                print(f"期权代码: {code} 的详细数据获取失败")
                continue
            expire_date = detail_data['ExpireDate']
            print("//////////////////", detail_data, expire_date)
            print(f"期权代码: {code}，期权价格: {option_price}, 标的价格: {underlying_price}, 行权价: {strike_price}")
            if not expire_date:
                print(f"期权代码: {code} 的到期日信息缺失")
                continue
            else:
                days_to_expiration = (datetime.strptime(expire_date, '%Y%m%d') - datetime.now()).days

            T = days_to_expiration / 365

            sigma = calc_implied_volatility(
                market_price=option_price,
                S=underlying_price,
                K=strike_price,
                T=T,
                r=risk_free_rate,
                option_type=opiton_type
            )

            if sigma is not None:
                greeks = calc_american_option_greeks(
                    S=underlying_price,
                    K=strike_price,
                    T=T,
                    r=risk_free_rate,
                    sigma=sigma,
                    option_type=opiton_type
                )

                results[code] = {
                    'implied_volatility': sigma,
                    'iv': sigma * 100,
                    'option_price': option_price,
                    'underlying_price': underlying_price,
                    'strike_price': strike_price,
                    'time_to_expiration': T,
                    'option_type': opiton_type,
                    'price': greeks['price'],
                    'delta': greeks['delta'],
                    'gamma': greeks['gamma'],
                    'vega': greeks['vega'],
                    'theta': greeks['theta'],
                    'rho': greeks['rho']
                }
            # print("------------------------------------")
            print(f"期权代码: {code} 的美式期权希腊字母值:")
            print(f"  隐含波动率: {sigma * 100:.2f}%")
            print(f"  价格: {greeks['price']:.4f}")
            print(f"  Delta: {greeks['delta']:.4f}")
            print(f"  Gamma: {greeks['gamma']:.4f}")
            print(f"  Vega: {greeks['vega']:.4f}")
            print(f"  Theta: {greeks['theta']:.4f}")
            print(f"  Rho: {greeks['rho']:.4f}")
            print("------------------------------------")

        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"处理期权代码 {code} 时出错: {e}")
    return results


if __name__ == "__main__":
    # option_code = ['ao2507C2800.SF']
    # option_codes = []
    # with open('code(1).txt', 'r') as f:
    #     option_codes = [line.strip() for line in f if line.strip()]
        # print(f"读取到 {len(option_code)} 个期权代码")
    # option_codes = ['rb2510P2850.SF','rb2510P2900.SF','sn2507P240000.SF','ao2508C3100.SF', 'ao2507P2800.SF',
    #                 'ao2509C3100.SF','ag2508P8300.SF','ag2508P7800.SF','ag2508P8000.SF', 'cu2507P73000.SF', 
    #                 'SH509C2560.ZF', 'SR509C6200.ZF', 'a2509-C-4450.DF', 'ps2508-C-36000.GF',  'ni2507C128000.SF','lc2509-C-64000.GF']
    option_codes = [ 'si2509-P-7000.GF', 'si2509-P-7100.GF']
    date = '20250626'
    # for code in option_codes:
    # calc_hv(option_codes, 30)
    results = calc_iv(option_codes, date)
    # print(results)
    for code in option_codes:
        print(results[code]['iv'])
    # print(results)
    # print(results[option_codes[0]]['iv'])

    # greek_letter = calc_greeks_letter(option_codes)
    # american_greeks = calc_american_greeks_letter(option_codes)