import sys

from stock import Market
from display import run_stock

if len(sys.argv) > 1:
    regime = sys.argv[1]
else:
    regime = 'neutral'

market = Market()
market.set_regime(regime)

market.add_stock(name = 'ABX')
print(market.stocks[0].__dict__)

run_stock(market, ticks = 100, duration = 0.005)
