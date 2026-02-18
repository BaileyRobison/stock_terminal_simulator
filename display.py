"""
Basic display in matplotlib
"""
import matplotlib.pyplot as plt

def run_stock(market, ticks = 100, duration = 0.1):
    prices = [market.stocks[0].price]
    changes = [0]

    plt.ion()
    fig, ax = plt.subplots()
    
    for i in range(ticks): # random updates to price
        market.update_stock()
        
        prices.append(market.price)
        changes.append(prices[i] - prices[i-1])
        
    colors = ['green' if c > 0 else 'red' if c < 0 else 'gray' for c in changes]
        
        
    for i in range(ticks): # show updating plot
        ax.clear()
        
        #ax.plot(prices[:i+1]
        ax.bar(range(len(changes[:i+1])), changes[:i+1], color=colors[:i+1])
        
        plt.pause(duration)
    
    
    plt.ioff()
    plt.show()