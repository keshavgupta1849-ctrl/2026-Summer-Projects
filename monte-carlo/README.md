Phase 3 — Monte Carlo Simulator

What this does
Instead of building an exhaustive tree of every possible price path (binomial), Monte Carlo 
prices an option by simulating many random future price paths under risk-neutral 
dynamics, averaging the payoff across all of them, and discounting that average back 
to today.

Geometric Brownian Motion (GBM)
Each simulated step advances the stock price using:

    S(t+dt) = S(t) * exp[(r - sigma^2/2)*dt + sigma*sqrt(dt)*Z]

- Z is a fresh draw from the standard normal distribution each step — the random shock.
- sigma*sqrt(dt) scales that shock correctly: variance adds linearly across independent 
  time steps, but standard deviation (which sets the actual size of the price wiggle) is 
  the square root of variance — the same sqrt(dt) logic used to derive u and d in the 
  binomial tree (Phase 2a).
- (r - sigma^2/2) is a drift correction. Naively, you'd expect the stock to grow at 
  exactly rate r, but because we're compounding random percentage changes over and over, 
  the average of exp(random stuff) isn't the same as exp(average of random stuff) — 
  averaging pulls it up. Subtracting sigma^2/2 from the drift cancels that effect out, 
  so the average growth rate still lands on r, as risk-neutral pricing requires.

Pricing formula
    price ≈ (1 / e^(r*T)) * average(payoff across all simulated paths)

Unlike the binomial tree, which discounts step-by-step through backward induction 
(since it needs a known option value at every node), Monte Carlo never computes an 
intermediate value — it only knows the payoff at expiry. So there's nothing to 
discount along the way; the full average payoff gets discounted once, over the 
entire time to expiry.

Results (S0=100, K=100, sigma=0.30, r=0.05, T=1, 10,000 paths, seed=42)
- Mean simulated final price: $104.95 (theoretical risk-neutral expectation: $105.13 — matches closely)
- Monte Carlo call price: $14.00
- Binomial tree call price (Phase 2a, converged): $14.20–14.23
- Monte Carlo put price: $9.29
- Put-call parity check: Call − Put = $4.71 (Monte Carlo) vs. S0 − K*e^(-rT) = $4.88 
  (theoretical) — a real, expected mismatch, discussed below.

Visualizations
- sample_paths.png — 20 individual simulated price paths, all starting at $100 and 
  spreading out over the year, showing how much randomness dominates any single outcome.
- final_price_histogram.png — distribution of all 10,000 final prices. Notably 
  asymmetric (lognormal): a sharp cutoff near zero on the left, a long thin tail 
  stretching to the right. The most common (modal) outcome sits below $100 even 
  though the average lands near the risk-free-implied $105 — these are different 
  statistics, and mode-below-mean here does *not* mean the stock is expected to lose value.
- convergence_plot.png — the Monte Carlo price estimate at increasing path counts 
  (100 to 10,000), compared to the binomial tree's converged value. The estimate is 
  noisy at low path counts and settles closer to the true value as the number of 
  paths grows, though not perfectly monotonically.

Limitations
- Monte Carlo error shrinks proportional to 1/sqrt(n), not 1/n — quadrupling the number 
  of paths only halves the error. This is why the put-call parity check has a larger gap 
  ($0.17) than the call-price-vs-binomial check: each price carries its own independent 
  sampling error, and those errors don't necessarily cancel.
- The convergence plot uses subsets of the same 10,000 simulated paths rather than fully 
  independent reruns at each path count, so it shows one run's specific noise pattern 
  settling down — not a rigorous average-case convergence curve.
- A fixed random seed (np.random.seed(42)) was added specifically so these results and 
  saved plots are exactly reproducible — rerunning main.py will regenerate the same 
  numbers and figures shown here.
- As implemented, this only prices European options. Unlike the binomial tree, plain 
  Monte Carlo has no natural way to check for early exercise at intermediate points 
  (it never computes a value partway through a path), so it can't handle American options 
  without more advanced techniques (e.g. Longstaff-Schwartz), which are out of scope here.