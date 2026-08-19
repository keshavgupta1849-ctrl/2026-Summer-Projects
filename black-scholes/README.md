# Phase 4 — Black-Scholes Option Pricing

Closed-form pricing for European **call** and **put** options, plus a three-way
comparison against the binomial tree (Phase 2a) and Monte Carlo (Phase 3) methods
from earlier in this project.

## What it does

- `price_call(S0, K, r, sigma, T)` — Black-Scholes price of a European call
- `price_put(S0, K, r, sigma, T)` — Black-Scholes price of a European put

Both use the standard normal CDF (`scipy.stats.norm.cdf`) for `N(d1)` and `N(d2)`:

```
d1 = [ ln(S0/K) + (r + sigma^2 / 2) * T ] / (sigma * sqrt(T))
d2 = d1 - sigma * sqrt(T)

Call = S0 * N(d1)  - K * e^(-rT) * N(d2)
Put  = K * e^(-rT) * N(-d2) - S0 * N(-d1)
```

## Results

Same option across all three methods (`S0=100, K=100, r=0.05, sigma=0.30, T=1`):

| Method         | Call price | Diff vs Black-Scholes |
|----------------|-----------:|----------------------:|
| Binomial tree  |    14.21   |        −0.02          |
| Monte Carlo    |    14.00   |        −0.23          |
| Black-Scholes  |   14.2313  |         0.00          |

Put price: **9.3542**. As an independent check, put-call parity holds exactly:

```
C - P            = 4.8771
S0 - K*e^(-rT)   = 4.8771
```

Because parity is a no-arbitrage identity (it doesn't depend on Black-Scholes at
all), matching both sides confirms the put is priced correctly.

## What I learned

The biggest takeaway was watching three completely different methods agree. The
binomial tree, the Monte Carlo simulation, and the Black-Scholes formula all priced
the same option at essentially the same value (~14.23). That agreement isn't a
coincidence: all three assume the same geometric Brownian motion model for the
stock, so they're really three roads to the same "true" price. The tree approximates
it with discrete up/down steps, Monte Carlo estimates it by averaging thousands of
simulated payoffs, and Black-Scholes computes it directly in closed form. Getting
them to match is what actually *verifies* that each one is implemented correctly.

The comparison also made the tradeoffs concrete. The tree came within about 0.02 of
Black-Scholes, but Monte Carlo was about 0.23 off. That's because Monte Carlo is the
only one of the three with randomness in it — its error shrinks like 1/√n as you add
paths, but with a finite number of simulations there's always some sampling noise.
The tree and the formula are both deterministic, so they don't have that wiggle.

On the formula itself, the piece that clicked was `N(d2)`: it's the risk-neutral
probability that the option finishes in the money — literally the area under the
terminal price distribution to the right of the strike. So the call price is just
"the stock you'd receive if you exercise" minus "the strike you'd pay," each
weighted by the probability it actually happens.

What surprised me was seeing `sigma^2 / 2` show up again. I'd already met it in the
Monte Carlo phase as the drift correction in GBM `(r - sigma^2/2)`, and here it
reappears inside `d1`. Same variance-adjustment idea turning up in both the
simulation and the closed-form formula — that connection made Black-Scholes feel
less like a formula to memorize and more like the exact version of the thing I'd
already been simulating.

## How to run

```
python3 main.py
```

Requires `scipy` (`pip install scipy`).
