"""
Basic display in matplotlib
"""
import matplotlib.pyplot as plt

def run_stock(market, ticks = 100, duration = 0.1):
    prices = [market.stocks[0].price] # initial price

    plt.ion() # enter interactive mode
    fig, ax = plt.subplots()
    
    for tick in range(ticks): # random updates to price
        market.update_stock()
        prices.append(market.price)
        
    for tick in range(1, ticks): # plot bars
        prev = prices[tick-1]
        curr = prices[tick]

        if curr > prev:
            color = 'green'
        else:
            color = 'red'
            
        # plot new bar
        ax.bar(tick, curr - prev, bottom=prev, color=color, width=0.8)
        
        plt.pause(duration)    
    
    plt.ioff() # leave interactive mode
    plt.show()