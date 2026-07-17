import math

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

def crr_price(S0, K, sigma, r, T, N, is_call):
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
            last_row.append(max(K-tree[N][i], 0))
    option_tree[N] = last_row

    for t in range(N - 1, -1, -1):
        row = []
        for i in range(t + 1):
            value_down = option_tree[t+1][i]
            value_up = option_tree[t+1][i+1]
            q = (R - d) / (u - d)
            node_value = (1/R) * (q * value_up + (1-q) * value_down)
            row.append(node_value)
        option_tree[t] = row

    return option_tree[0][0]


# Sanity check against your original one-period calculation
print(one_period_call_price(100, 1.1, 0.9, 1.05, 100))

# Inputs for the N-period version
S0 = 100
K = 100
sigma = 0.3
r = 0.05
T = 1

# --- Convergence table: fill this loop in yourself ---
print(f"{'N':>5} | {'Price':>10}")
print("-" * 20)
for N_test in [1, 2, 5, 25, 100, 500]:
    price = crr_price(S0,K,sigma,r,T,N_test,False) 
    print(f"{N_test:>5} | {price:>10.4f}")