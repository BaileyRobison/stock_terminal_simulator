import sys

from stock import Market
from engine import Engine

if len(sys.argv) > 1:
    regime = sys.argv[1]
else:
    regime = 'neutral'

market = Market()
market.set_regime(regime)
market.set_stock(name = 'ABX')

eng = Engine(market)
eng.run(ticks = 200, duration = 0.0005)
