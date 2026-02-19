import sys

from stock import Market
from display import Plotter

if len(sys.argv) > 1:
    regime = sys.argv[1]
else:
    regime = 'neutral'

market = Market()
market.set_regime(regime)
market.add_stock(name = 'ABX')

pl = Plotter()
pl.plot_stock_price(market, ticks = 100, duration = 0.005)
