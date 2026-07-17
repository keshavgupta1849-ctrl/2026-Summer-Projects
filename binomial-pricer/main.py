import math
import matplotlib.pyplot as plt
import numpy as np

def print_tree(tree):
    for row in tree:
        print("  ".join(f"{price:8.2f}" for price in row))

def one_period_call_price(S0, u, d, R, K):
    Su = S0 * u
    Sd = S0 * d

    payoff_up = max(Su - K, 0)
    payoff_down = max(Sd - K, 0)

    q = (R - d) / (u - d)

    price = (1/R) * (q * payoff_up + (1-q) * payoff_down)

    return price

def crr_price(S0, K, sigma, r, T, N, is_call, is_american):
    dt = T / N
    u = math.exp(sigma * math.sqrt(dt))
    d = 1 / u
    R = math.exp(r * dt)

    tree = []
    for t in range(N + 1):
        row = []
        for i in range(t + 1):
            row.append(S0 * (u**i) * (d**(t-i)))
        tree.append(row)

    option_tree = [None] * (N + 1)
    last_row = []
    for i in range(N + 1):
        if is_call:
            last_row.append(max(tree[N][i] - K, 0))
        else:
            last_row.append(max(K - tree[N][i], 0))
    option_tree[N] = last_row

    for t in range(N - 1, -1, -1):
        row = []
        for i in range(t + 1):
            value_down = option_tree[t+1][i]
            value_up = option_tree[t+1][i+1]
            q = (R - d) / (u - d)
            continuation = (1/R) * (q * value_up + (1-q) * value_down)

            if is_american:
                if is_call:
                    node_value = max(continuation, max(tree[t][i] - K, 0))
                else:
                    node_value = max(continuation, max(K - tree[t][i], 0))
            else:
                node_value = continuation

            row.append(node_value)
        option_tree[t] = row

    return option_tree[0][0]


# Check against your original one-period calculation
print(one_period_call_price(100, 1.1, 0.9, 1.05, 100))

# Inputs for the N-period version
S0 = 100
K = 100
sigma = 0.3
r = 0.05
T = 1
N=100

# Convergence table
def print_convergence_table(label, is_call, is_american):
    print(label)
    print(f"{'N':>5} | {'Price':>10}")
    print("-" * 20)
    for N_test in [1, 2, 5, 25, 100, 500]:
        price = crr_price(S0, K, sigma, r, T, N_test, is_call, is_american)
        print(f"{N_test:>5} | {price:>10.4f}")
    print()  # blank line for spacing between tables

#Volatility loop
sigmas = np.linspace(0.05, 0.8, 20)
prices = []
for sigma_test in sigmas:
    price = crr_price(S0, K, sigma_test, r, T, N, True, False) 
    prices.append(price)

#Graphing Volatility loop
plt.plot(sigmas,prices)
plt.xlabel("Volatility")
plt.ylabel("Price")
plt.title("Volatility vs Price")
plt.show()

#Strike loop
strikes = np.linspace(50, 150, 20)
strike_prices = []
for K_test in strikes:
    price = crr_price(S0, K_test, sigma, r, T, N, True, False)
    strike_prices.append(price)

#Graphing Strike loop
plt.plot(strikes, strike_prices)
plt.xlabel("Strike Price (K)")
plt.ylabel("Price")
plt.title("Strike vs Price")
plt.show()

#Time to Expiry loop
times = np.linspace(0.1, 2, 20)
time_prices = []
for T_test in times:
    price = crr_price(S0, K, sigma, r, T_test, N, True, False)  # which variable goes here instead of T?
    time_prices.append(price)

#Graphing Time loop
plt.plot(times, time_prices)
plt.xlabel("Time to Expiry (T)")
plt.ylabel("Price")
plt.title("Time to Expiry vs Price")
plt.show()

#European vs American
sigmas2 = np.linspace(0.05, 0.8, 20)
euro_put_prices = []
amer_put_prices = []
for sigma_test in sigmas2:
    euro_price = crr_price(S0, K, sigma_test, r, T, N, False, False)
    amer_price = crr_price(S0, K, sigma_test, r, T, N, False, True)
    euro_put_prices.append(euro_price)
    amer_put_prices.append(amer_price)

#Graphing European vs American
plt.plot(sigmas2, euro_put_prices, label="European Put")
plt.plot(sigmas2, amer_put_prices, label="American Put")
plt.xlabel("Volatility")
plt.ylabel("Price")
plt.title("American vs European Put")
plt.legend()
plt.show()

print_convergence_table("American Call", True, True)
print_convergence_table("American Put", False, True)
print_convergence_table("European Call", True, False)
print_convergence_table("European Put", False, False)