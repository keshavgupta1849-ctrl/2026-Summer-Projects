Portfolio Optimizer — Markowitz Efficient Frontier

What this project does

Given a basket of 7 stocks, this program finds every possible way to allocate 
money across them and identifies the best combinations — the ones with the 
highest return for each level of risk. That boundary is called the efficient frontier.

Stocks used: AAPL, MSFT, BAC, JNJ, XOM, AMZN, GLD (2021-2024)


The core finance idea

Diversification reduces risk through the relationship between assets, not through 
individual stock behavior. When one stock drops, another may hold steady, and the 
covariance matrix captures that relationship mathematically.

A portfolio's return is w^T * u (weights dot mean returns) and its variance is 
w^T * E * w (weights through the covariance matrix). The covariance matrix bends 
the frontier into a curve. Low or negative covariances between assets create that 
curve. GLD carries near-zero covariance with the tech stocks, which drives its 
heavy weighting in the optimal portfolios.


Key results

Max Sharpe portfolio (best return per unit of risk): 26.3% return, 19.0% volatility, 
Sharpe of 1.17. The optimizer allocated 51.7% to GLD because of its low covariance 
with equities.

Min volatility portfolio (lowest possible risk): 10.1% return, 11.2% volatility, 
Sharpe of 0.54. JNJ (34.6%) and XOM (32.8%) dominate this portfolio as defensive, 
low-covariance stocks.


Honest limitations

Random sampling across 10,000 portfolios locates approximate frontier points. 
Finding the true frontier requires scipy minimize. The optimizer also places no 
constraints on position sizes, making 51% in GLD unrealistic in practice. Mean 
returns come from historical data, which carries no guarantee about the future.


How I built this

I came into this project with a strong CS background and no finance or probability 
background. Before writing any code I self-studied probability from scratch, working 
through random variables, expectation, variance, and the normal distribution 
independently. I learned the finance concepts — mean-variance optimization, the 
covariance matrix, the Sharpe ratio, and what the efficient frontier represents — 
through conversation with an AI assistant who explained the reasoning behind each 
step rather than providing the code directly.

I wrote the code myself, working through the logic piece by piece and asking for 
guidance when I got stuck. I want to be straightforward: this is a beginner project 
and the code is simple enough to generate in seconds. The goal was understanding every line, every formula, and every finance decision behind it.


What I learned

Mean-variance optimization is sensitive to estimated mean returns, which historical 
data measures noisily. Real portfolio managers treat the output as a starting point 
rather than a prescription. Diversification provides free risk reduction, and the 
covariance matrix is exactly where that reduction lives.