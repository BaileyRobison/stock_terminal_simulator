
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

settings = {
    'bars': 100,
    'long_term_bars': 400,    
    'long_term_update': 10,
}

eng = Engine(market, settings)
eng.run(ticks = 100, duration = 0.0005)
