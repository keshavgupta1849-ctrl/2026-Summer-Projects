Binomial Options Pricer

What this project does

Prices European call and put options using a multi-period binomial tree (the Cox-Ross-Rubinstein, or "CRR," model). Given a stock's current price, a strike price, volatility, the risk-free rate, and time to expiry, it computes what the option is worth today and proves that the answer converges to a stable price as the tree is sliced into more time steps.

The core idea:

The price of an option is not a bet on which way the stock will move. It's determined by a no-arbitrage argument called replication.

At every point in time, the stock can only do one of two things over the next tiny step: go up by a factor u, or go down by a factor d. Given that, you can always build a portfolio out of some shares of stock plus some cash (borrowed or lent at the risk-free rate) that pays off exactly what the option pays off, no matter which way the stock moves. If two things produce identical payoffs in every scenario, they must cost the same today; otherwise, you could buy the cheap one, sell the expensive one, and lock in risk-free profit. That's an arbitrage, and the model assumes those can't persist.

So pricing an option really means figuring out the replicating portfolio and then checking what it costs.

The risk-neutral probability, q

Solving the replication problem produces a specific number, `q`:

q = (R - d) / (u - d)


where R = e^(r·dt)` is the risk-free growth factor over one time step.

q is not a real-world probability. It doesn't reflect anyone's actual belief about whether the stock will rise or fall. It's the specific weighting that makes the discounted expected payoff formula produce the same price as the replicating portfolio. Under q, the stock's expected growth rate works out to exactly the risk-free rate, that's why it's called "risk-neutral." Two investors who violently disagree about the real odds of the stock rising will still agree on the option's price, because the price never depended on those odds in the first place.

Building the tree

Given N time steps over a total life of T years:

- dt = T / N — the length of each step
- u = e^(σ√dt), d = 1/u — up and down factors, derived from the stock's annualized volatility σ
- R = e^(r·dt) — one step's risk-free growth

Because u and d are the same at every step, an "up-then-down" path and a "down-then-up" path land on the exact same stock price, the tree recombines. This keeps the tree cheap: at time step t, there are only t+1 distinct nodes (not 2^t), and each node's price depends only on how many total up-moves occurred, not their order:

tree[t][i] = S0 * u^i * d^(t-i)

Pricing via backward induction

The option's payoff is only known for certain at expiry:

- Call: max(S - K, 0)
- Put: max(K - S, 0)

Starting from those known payoffs at the last time step, the model works backward to today, one layer at a time. At every node, the same formula applies:


value = (1/R) * [q * value_up + (1-q) * value_down]


in words: today's value at this node is the risk-free discount factor times the risk-neutral-weighted average of what the node's two possible children are worth. Repeating this from expiry back to today gives the option's price.

Checks

Convergence. With S0=K=100, σ=0.30, r=0.05, T=1 year, the call price computed by the tree is:

| N | Price |
|---|---|
| 1 | 16.96 |
| 2 | 12.89 |
| 5 | 14.79 |
| 25 | 14.34 |
| 100 | 14.20 |
| 500 | 14.23 |

The price doesn't move monotonically, but it settles into a tight band as N grows. This is expected — S0, K, σ, r, and T describe the actual option contract; N is only a modeling choice (how finely to slice time), and it shouldn't change what is being priced, only how precisely the model approximates its true value.

Put-call parity. For a call and put sharing the same K and T:


Call price - Put price = S0 - K * e^(-r*T)


With the same inputs: Call − Put ≈ 14.22 − 9.35 ≈ 4.87, and S0 − K·e^(−rT) ≈ 4.87. These matching independently is a real check on correctness — a sign error or mis-specified payoff would very likely break this equality.

Limitations

- This prices European options only (exercise at expiry only). American options, which can be exercised early, need one additional comparison at each node — that's the next part I will work on.
- Volatility σ is treated as a known, constant input. In reality it's neither known in advance nor constant over time — estimating it is itself a hard problem this project doesn't address.
- The model assumes frictionless markets: no transaction costs, no bid-ask spread, unlimited borrowing/lending at the same risk-free rate. None of that holds exactly in real markets.