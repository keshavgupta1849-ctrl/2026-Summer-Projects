import math
from scipy.stats import norm

def price_call(S0, K, r, sigma, T):
    # Step 1: Calculate d1
    d1 = (math.log(S0 / K) + (r + (sigma**2) / 2) * T) / (sigma * math.sqrt(T))
    
    # Step 2: Calculate d2
    d2 = d1 - sigma * math.sqrt(T)
    
    # Step 3: Calculate call option price using N(d1) and N(d2)
    price = S0 * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    
    # Step 4: Return the result
    return price

# Quick test run
if __name__ == "__main__":
    # S0=100, K=100, r=5% (0.05), sigma=20% (0.30), T=1 year
    call_price = price_call(100, 100, 0.05, 0.30, 1.0)
    print(f"Call Option Price: {call_price:.4f}")


# ---- Three-way comparison: same option, three methods ----
S0, K, r, sigma, T = 100, 100, 0.05, 0.30, 1.0

bs_call = price_call(S0, K, r, sigma, T)          # exact, computed live
tree_call = 14.21   # <-- replace with the exact number your Phase 2a tree printed
mc_call   = 14.00   # <-- replace with the exact number your Phase 3 Monte Carlo printed

print(f"Option: S0={S0}, K={K}, r={r}, sigma={sigma}, T={T}\n")
print(f"{'Method':<18}{'Call price':>12}{'Diff vs BS':>14}")
print("-" * 44)
print(f"{'Binomial tree':<18}{tree_call:>12.4f}{tree_call - bs_call:>+14.4f}")
print(f"{'Monte Carlo':<18}{mc_call:>12.4f}{mc_call - bs_call:>+14.4f}")
print(f"{'Black-Scholes':<18}{bs_call:>12.4f}{0.0:>+14.4f}")