import numpy as np
import torch
import matplotlib.pyplot as plt
from scipy.stats import norm
import time

# Set random seed to ensure reproducibility
np.random.seed(42)
torch.manual_seed(42)

# Check if GPU is available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# Heston model parameters
class HestonParams:
    def __init__(self):
        self.S0 = 100.0       # Initial stock price
        self.V0 = 0.04        # Initial volatility
        self.kappa = 2.0      # Mean reversion speed of volatility
        self.theta = 0.04     # Long-term mean of volatility
        self.sigma = 0.3      # Volatility of volatility
        self.rho = -0.7       # Correlation between price and volatility
        self.r = 0.05         # Risk-free rate
        self.T = 1.0          # Option maturity (years)
        self.K = 100.0        # Option strike price
        self.trading_days = 252  # Trading days per year

# Simulate Heston model
def simulate_heston(params, n_paths, n_steps):
    """
    Simulate Heston model paths using Euler scheme
    
    Parameters:
    params: HestonParams object
    n_paths: Number of simulation paths
    n_steps: Number of time steps
    
    Returns:
    S: Stock price paths [n_paths, n_steps+1]
    V: Volatility paths [n_paths, n_steps+1]
    integrated_var: Integrated variance paths [n_paths, n_steps+1]
    """
    dt = params.T / n_steps
    sqrt_dt = np.sqrt(dt)
    
    # Initialize paths
    S = np.zeros((n_paths, n_steps + 1))
    V = np.zeros((n_paths, n_steps + 1))
    integrated_var = np.zeros((n_paths, n_steps + 1))
    
    # Set initial values
    S[:, 0] = params.S0
    V[:, 0] = params.V0
    
    # Generate correlated random numbers
    Z1 = np.random.randn(n_paths, n_steps)
    Z2 = params.rho * Z1 + np.sqrt(1 - params.rho**2) * np.random.randn(n_paths, n_steps)
    
    # Simulate paths
    for t in range(n_steps):
        # Ensure volatility is positive (Feller condition)
        V[:, t] = np.maximum(V[:, t], 0)
        
        # Update stock price using log-normal dynamics
        S[:, t+1] = S[:, t] * np.exp((params.r - 0.5 * V[:, t]) * dt + np.sqrt(V[:, t]) * sqrt_dt * Z1[:, t])
        
        # Update volatility using CIR process
        V[:, t+1] = V[:, t] + params.kappa * (params.theta - V[:, t]) * dt + params.sigma * np.sqrt(V[:, t]) * sqrt_dt * Z2[:, t]
        
        # Calculate integrated variance
        integrated_var[:, t+1] = integrated_var[:, t] + V[:, t] * dt
    
    return S, V, integrated_var

# Calculate variance swap value based on theoretical formula
def calculate_variance_swap(integrated_var_t, V_t, t, T, params):
    """
    Calculate variance swap value using the formula:
    S_t^2 = ∫_0^t V_s ds + L(t, V_t)
    where L(t,v) = (v-h)/α * (1-e^(-α(T-t))) + h(T-t)
    
    Parameters:
    integrated_var_t: Realized variance from 0 to t
    V_t: Current instantaneous variance
    t: Current time
    T: Maturity
    params: Model parameters
    
    Returns:
    variance_swap_value: Variance swap value
    """
    h = params.theta      # Long-term variance mean
    alpha = params.kappa  # Mean reversion rate
    
    remaining_T = T - t
    if remaining_T <= 0:
        return integrated_var_t
    
    # Calculate L(t, V_t) - expected future variance contribution
    L_t_v = (V_t - h) / alpha * (1 - np.exp(-alpha * remaining_T)) + h * remaining_T
    
    # Total variance swap value
    variance_swap_value = integrated_var_t + L_t_v
    
    return variance_swap_value

# Calculate sensitivity of variance swap to instantaneous variance
def variance_swap_sensitivity(V_t, t, T, params):
    """
    Calculate ∂L(t,V_t)/∂V_t for hedging purposes
    
    Parameters:
    V_t: Current instantaneous variance
    t: Current time
    T: Maturity
    params: Model parameters
    
    Returns:
    sensitivity: Partial derivative of L with respect to V
    """
    alpha = params.kappa
    remaining_T = T - t
    
    if remaining_T <= 0:
        return 0
    
    # Sensitivity: ∂L(t,v)/∂v = 1/α * (1-e^(-α(T-t)))
    sensitivity = (1 - np.exp(-alpha * remaining_T)) / alpha
    
    return sensitivity

# Heston model characteristic function for option pricing
def heston_characteristic_function(phi, S, V, T, params):
    """
    Heston model characteristic function for option pricing
    """
    a = params.kappa * params.theta
    b = params.kappa
    
    d = np.sqrt((params.rho * params.sigma * phi * 1j - b)**2 + (params.sigma**2) * (phi * 1j + phi**2))
    g = (b - params.rho * params.sigma * phi * 1j - d) / (b - params.rho * params.sigma * phi * 1j + d)
    
    exp1 = np.exp(params.r * T * phi * 1j)
    exp2 = np.exp(a * T * (b - params.rho * params.sigma * phi * 1j - d) / (params.sigma**2))
    exp3 = np.exp((V * (b - params.rho * params.sigma * phi * 1j - d)) / (params.sigma**2 * (1 - g * np.exp(-d * T))))
    
    return exp1 * exp2 * exp3

# Calculate option price under Heston model
def heston_option_price_fft(S, V, K, T, params, option_type='put'):
    """
    Calculate option price using Heston model and FFT methods
    """
    from scipy.integrate import quad
    
    # Characteristic function integral for call option
    def integrand_call(phi, S, V, K, T, params):
        numerator = np.exp(-phi * np.log(K) * 1j) * heston_characteristic_function(phi - 1j, S, V, T, params)
        denominator = phi * 1j
        return np.real(numerator / denominator)
    
    # Calculate integral
    try:
        result, _ = quad(integrand_call, 0, 100, args=(S, V, K, T, params), limit=100)
        call_price = S / 2 + result / np.pi
        
        # Use put-call parity for put option
        if option_type.lower() == 'call':
            return max(call_price, 0)
        else:  # Put option
            put_price = call_price - S + K * np.exp(-params.r * T)
            return max(put_price, 0)
    except:
        # Fallback to Black-Scholes if Heston pricing fails
        vol = np.sqrt(V)
        d1 = (np.log(S / K) + (params.r + 0.5 * vol**2) * T) / (vol * np.sqrt(T))
        d2 = d1 - vol * np.sqrt(T)
        
        if option_type.lower() == 'call':
            return S * norm.cdf(d1) - K * np.exp(-params.r * T) * norm.cdf(d2)
        else:
            return K * np.exp(-params.r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

# Calculate option Delta under Heston model
def heston_option_delta(S, V, K, T, params, option_type='put'):
    """
    Calculate option Delta using numerical differentiation
    """
    h = 0.01  # Small price change
    
    price_up = heston_option_price_fft(S + h, V, K, T, params, option_type)
    price_down = heston_option_price_fft(S - h, V, K, T, params, option_type)
    
    delta = (price_up - price_down) / (2 * h)
    return delta

# Calculate option Vega under Heston model
def heston_option_vega(S, V, K, T, params, option_type='put'):
    """
    Calculate option Vega (sensitivity to variance) using numerical differentiation
    """
    h = 0.0001  # Small variance change
    
    price_up = heston_option_price_fft(S, V + h, K, T, params, option_type)
    price_down = heston_option_price_fft(S, V - h, K, T, params, option_type)
    
    vega = (price_up - price_down) / (2 * h)
    return vega

# Calculate European put option payoff
def put_option_payoff(S, K):
    """
    Calculate put option payoff
    """
    if isinstance(S, torch.Tensor):
        return torch.maximum(torch.tensor(K, device=S.device) - S, torch.tensor(0.0, device=S.device))
    else:
        return np.maximum(K - S, 0)

# Visualization functions
def plot_heston_paths(S, V, integrated_var, params, n_paths_to_plot=5):
    """
    Plot sample Heston model paths
    """
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Plot stock price paths
    axes[0, 0].plot(S[:n_paths_to_plot].T)
    axes[0, 0].set_title('Stock Price Paths')
    axes[0, 0].set_xlabel('Time Steps')
    axes[0, 0].set_ylabel('Stock Price')
    axes[0, 0].grid(True)
    
    # Plot volatility paths
    axes[0, 1].plot(V[:n_paths_to_plot].T)
    axes[0, 1].set_title('Volatility Paths')
    axes[0, 1].set_xlabel('Time Steps')
    axes[0, 1].set_ylabel('Volatility')
    axes[0, 1].grid(True)
    
    # Plot integrated variance paths
    axes[1, 0].plot(integrated_var[:n_paths_to_plot].T)
    axes[1, 0].set_title('Integrated Variance Paths')
    axes[1, 0].set_xlabel('Time Steps')
    axes[1, 0].set_ylabel('Integrated Variance')
    axes[1, 0].grid(True)
    
    # Plot correlation between stock returns and volatility changes
    returns = np.diff(np.log(S), axis=1)
    vol_changes = np.diff(V, axis=1)
    
    sample_path = 0
    axes[1, 1].scatter(returns[sample_path], vol_changes[sample_path], alpha=0.6)
    axes[1, 1].set_title(f'Returns vs Vol Changes (Path {sample_path})')
    axes[1, 1].set_xlabel('Log Returns')
    axes[1, 1].set_ylabel('Volatility Changes')
    axes[1, 1].grid(True)
    
    # Add correlation coefficient
    corr = np.corrcoef(returns[sample_path], vol_changes[sample_path])[0, 1]
    axes[1, 1].text(0.05, 0.95, f'Correlation: {corr:.3f}', 
                   transform=axes[1, 1].transAxes, verticalalignment='top')
    
    plt.tight_layout()
    plt.savefig('heston_simulation_paths.png')
    plt.show()

# Test Heston model implementation
def test_heston_model():
    """
    Test the Heston model implementation
    """
    print("Testing Heston model implementation...")
    
    # Initialize parameters
    params = HestonParams()
    n_paths = 1000
    n_steps = 252  # One year of daily steps
    
    print(f"Parameters:")
    print(f"  S0={params.S0}, V0={params.V0}, kappa={params.kappa}")
    print(f"  theta={params.theta}, sigma={params.sigma}, rho={params.rho}")
    print(f"  r={params.r}, T={params.T}, K={params.K}")
    
    # Simulate paths
    start_time = time.time()
    S, V, integrated_var = simulate_heston(params, n_paths, n_steps)
    simulation_time = time.time() - start_time
    
    print(f"\nSimulation completed in {simulation_time:.2f} seconds")
    print(f"Generated {n_paths} paths with {n_steps} steps each")
    
    # Basic statistics
    final_prices = S[:, -1]
    final_vols = V[:, -1]
    final_integrated_var = integrated_var[:, -1]
    
    print(f"\nFinal Statistics:")
    print(f"  Stock Price: Mean={np.mean(final_prices):.4f}, Std={np.std(final_prices):.4f}")
    print(f"  Volatility: Mean={np.mean(final_vols):.4f}, Std={np.std(final_vols):.4f}")
    print(f"  Integrated Var: Mean={np.mean(final_integrated_var):.4f}, Std={np.std(final_integrated_var):.4f}")
    
    # Test option pricing
    print(f"\nTesting option pricing...")
    sample_S = params.S0
    sample_V = params.V0
    sample_T = params.T
    
    try:
        put_price = heston_option_price_fft(sample_S, sample_V, params.K, sample_T, params, 'put')
        call_price = heston_option_price_fft(sample_S, sample_V, params.K, sample_T, params, 'call')
        print(f"  Put Price: {put_price:.4f}")
        print(f"  Call Price: {call_price:.4f}")
        
        # Test put-call parity
        parity_check = call_price - put_price - (sample_S - params.K * np.exp(-params.r * sample_T))
        print(f"  Put-call parity check: {parity_check:.6f} (should be near 0)")
        
        # Test Greeks
        delta = heston_option_delta(sample_S, sample_V, params.K, sample_T, params, 'put')
        vega = heston_option_vega(sample_S, sample_V, params.K, sample_T, params, 'put')
        print(f"  Put Delta: {delta:.4f}")
        print(f"  Put Vega: {vega:.4f}")
        
    except Exception as e:
        print(f"  Option pricing failed: {e}")
    
    # Test variance swap calculation
    print(f"\nTesting variance swap calculation...")
    test_t = 0.5  # Half way through
    test_integrated_var = 0.02
    test_V = 0.05
    
    vs_value = calculate_variance_swap(test_integrated_var, test_V, test_t, params.T, params)
    vs_sensitivity = variance_swap_sensitivity(test_V, test_t, params.T, params)
    
    print(f"  Variance Swap Value: {vs_value:.4f}")
    print(f"  Variance Swap Sensitivity: {vs_sensitivity:.4f}")
    
    # Plot sample paths
    plot_heston_paths(S, V, integrated_var, params)
    
    return S, V, integrated_var

if __name__ == "__main__":
    # Run test
    S, V, integrated_var = test_heston_model()