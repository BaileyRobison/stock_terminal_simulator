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
market.stock.set_price(110)

settings = {
    'bars': 100,
}

eng = Engine(market, settings)
eng.run(ticks = 100, duration = 0.1)
