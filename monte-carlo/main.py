import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

#Inputting the GBM
def GBM(S0,sigma,r,dt,Z):
    return S0*np.exp((r-((sigma*sigma)/2))*dt+sigma*np.sqrt(dt)*Z)

#Simulates Prices
def simulate_path(S0, sigma, r, dt, N):
    Z = np.random.normal(0, 1, size=N)
    prices = [S0]
    for i in range(N):
        S_next = GBM(prices[i], sigma, r, dt, Z[i])
        prices.append(S_next)
    return np.array(prices)

#Simulates Multiple Prices 
def simulate_multiple_paths(S0, r, sigma, T, num_steps, num_paths, num_visual_paths):
    dt = T / num_steps
    
    final_prices = np.zeros(num_paths)
    sample_paths = np.zeros((num_visual_paths, num_steps + 1))
    
    for i in range(num_paths):
        current_path = simulate_path(S0, sigma, r, dt, num_steps)
        
        final_prices[i] = current_path[-1]
        
        if i < num_visual_paths:
            sample_paths[i] = current_path
    
    return final_prices, sample_paths


S0 = 100
sigma = 0.3
r = 0.05
dt = 1/252
N = 500

path = simulate_path(S0, sigma, r, dt, N)
print(np.round(path[:5], 2))
print(len(path)) 

#Tessting Single Path
path = simulate_path(S0, sigma, r, dt, N)

#Testing Final Multiple Path
final_prices, sample_paths = simulate_multiple_paths(
    S0=S0,
    r=r,
    sigma=sigma,
    T=1,             # 1 year
    num_steps=N,     # 500, matches your earlier dt = 1/252
    num_paths=10000,
    num_visual_paths=20
)

print("final_prices shape:", final_prices.shape)
print("first 5 final prices:", np.round(final_prices[:5], 2))
print("sample_paths shape:", sample_paths.shape)

#Plotting Sample Paths
plt.figure(figsize=(10, 6))

for i in range(sample_paths.shape[0]):
    plt.plot(sample_paths[i], alpha=0.6)

plt.xlabel("Time step (day)")
plt.ylabel("Stock price")
plt.savefig("sample_paths.png")
plt.title("20 sample simulated GBM price paths")


#Plotting histogram: 
plt.figure(figsize=(10, 6))
plt.hist(final_prices, bins=50, edgecolor='black', alpha=0.7)
plt.xlabel("Final stock price (after 1 year)")
plt.ylabel("Number of paths")
plt.savefig("final_price_histogram.png")
plt.title("Distribution of simulated final prices (10,000 paths)")


#Calculating Average
print("Mean final price:", np.mean(final_prices))
print("Theoretical expected price (S0 * e^(r*T)):", S0 * np.exp(r * 1))


K = 100  # strike price, adjust as needed

#Simulating Call Price
# Step 1: payoff for each path (call option)
payoffs = np.maximum(final_prices - K, 0)

# Step 2: average payoff across all paths
average_payoff = np.mean(payoffs)

# Step 3: discount back to today
R_total = np.exp(r * 1)  # T = 1 year, matches your simulation
mc_call_price = average_payoff / R_total

print("Monte Carlo call price:", mc_call_price)

#Simulating Put Price
put_payoffs = np.maximum(K - final_prices, 0)
average_put_payoff = np.mean(put_payoffs)
mc_put_price = average_put_payoff / R_total

print("Monte Carlo put price:", mc_put_price)

#Convergence Plot
path_counts = [100, 500, 1000, 2500, 5000, 10000]
mc_estimates = []

for n in path_counts:
    payoffs_subset = np.maximum(final_prices[:n] - K, 0)
    price_subset = np.mean(payoffs_subset) / R_total
    mc_estimates.append(price_subset)

binomial_reference = 14.21  # your Phase 2a converged binomial price

plt.figure(figsize=(10, 6))
plt.plot(path_counts, mc_estimates, marker='o', label='Monte Carlo estimate')
plt.axhline(y=binomial_reference, color='red', linestyle='--', label='Binomial tree (converged)')
plt.xlabel("Number of simulated paths")
plt.ylabel("Estimated call price")
plt.title("Monte Carlo convergence vs. binomial reference")
plt.savefig("convergence_plot.png")
plt.legend()
plt.show()
