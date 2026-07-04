import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

#Data 
tickers = ['AAPL', 'MSFT', 'BAC', 'JNJ', 'XOM', 'AMZN', 'GLD']

raw = yf.download(tickers, start='2021-01-01', end='2024-01-01', auto_adjust=True)

if isinstance(raw.columns, pd.MultiIndex):
    prices = raw['Close']
else:
    prices = raw

returns = prices.pct_change().dropna()

print(returns.head())
print(returns.shape)

#  Statistics 
mean_returns = returns.mean()
cov_matrix = returns.cov()

print("\nMean daily returns:")
print(mean_returns)
print("\nCovariance matrix:")
print(cov_matrix)

#  Simulate random portfolios 
num_portfolios = 10000
results = np.zeros((3, num_portfolios))
all_weights = np.zeros((num_portfolios, len(tickers)))

for i in range(num_portfolios):
    weights = np.random.random(len(tickers))
    weights /= np.sum(weights)
    all_weights[i] = weights

    port_return = np.sum(mean_returns * weights) * 252
    port_variance = np.dot(weights.T, np.dot(cov_matrix * 252, weights))
    port_volatility = np.sqrt(port_variance)
    sharpe = (port_return - 0.04) / port_volatility

    results[0, i] = port_return
    results[1, i] = port_volatility
    results[2, i] = sharpe

# --- Plot ---
fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(results[1], results[0], c=results[2], cmap='viridis', alpha=0.5, s=10)
plt.colorbar(scatter, label='Sharpe Ratio')
ax.set_xlabel('Annual Volatility (Risk)')
ax.set_ylabel('Annual Return')
ax.set_title('Efficient Frontier — Random Portfolio Simulation')

#  Mark key portfolios 
max_sharpe_idx = np.argmax(results[2])
ax.scatter(results[1, max_sharpe_idx], results[0, max_sharpe_idx],
           marker='*', color='gold', s=500, zorder=5, label='Max Sharpe')

min_vol_idx = np.argmin(results[1])
ax.scatter(results[1, min_vol_idx], results[0, min_vol_idx],
           marker='*', color='red', s=500, zorder=5, label='Min Volatility')

ax.legend()
print("\nMax Sharpe Portfolio:")
print(f"  Return: {results[0, max_sharpe_idx]:.3f}, Volatility: {results[1, max_sharpe_idx]:.3f}, Sharpe: {results[2, max_sharpe_idx]:.3f}")
for ticker, w in zip(tickers, all_weights[max_sharpe_idx]):
    print(f"  {ticker}: {w*100:.1f}%")

print("\nMin Volatility Portfolio:")
print(f"  Return: {results[0, min_vol_idx]:.3f}, Volatility: {results[1, min_vol_idx]:.3f}, Sharpe: {results[2, min_vol_idx]:.3f}")
for ticker, w in zip(tickers, all_weights[min_vol_idx]):
    print(f"  {ticker}: {w*100:.1f}%")

#  Click handler
def onclick(event):
    if event.inaxes != ax:
        return
    distances = (results[1] - event.xdata)**2 + (results[0] - event.ydata)**2
    idx = np.argmin(distances)
    print(f"\nPortfolio at (Risk: {results[1,idx]:.3f}, Return: {results[0,idx]:.3f})")
    print(f"Sharpe Ratio: {results[2,idx]:.3f}")
    print("Weights:")
    for ticker, w in zip(tickers, all_weights[idx]):
        print(f"  {ticker}: {w*100:.1f}%")

fig.canvas.mpl_connect('button_press_event', onclick)

plt.tight_layout()
plt.savefig('efficient_frontier.png', dpi=150, bbox_inches='tight')
plt.show()