"""
Basic display in matplotlib
"""
import matplotlib.pyplot as plt

def run_stock(market, ticks = 100, pause = 0.1):
    prices = [market.stocks[0].price]

    plt.ion()
    fig, ax = plt.subplots()
    
    for i in range(100): # random updates for ticks
        market.update_stock()
        prices.append(market.stocks[0].price)
        
        ax.clear()
        ax.plot(prices)
        plt.pause(0.1)
    
    
    plt.ioff()
    plt.show()