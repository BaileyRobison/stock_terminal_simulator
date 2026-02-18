from stock import Market
from display import run_stock

market = Market()

market.set_regime('neutral')
market.add_stock(name = 'ABX')
print(market.stocks[0].__dict__)

run_stock(market, ticks = 100, duration = 0.005)
