"""
Basic display in matplotlib
"""
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import yaml
import os

def read_yaml(yaml_file):
    # path to yaml file
    current_dir = os.path.dirname(__file__)
    path = current_dir+'/config/'+yaml_file+'.yaml'
    
    # open yaml file
    with open(path, encoding= 'utf-8') as f:
        yaml_content = yaml.safe_load(f)
        
    return yaml_content

def run_stock(market, ticks = 100, duration = 0.1):
    colors = read_yaml('style')
    
    prices = [market.stocks[0].price] # initial price
    times = [datetime(2026,1,1,12,0)]

    plt.ion() # enter interactive mode
    fig, ax = plt.subplots(facecolor=colors['bg'])
    ax.set_facecolor(colors['bg'])
    
    for side in ['bottom', 'top', 'left', 'right']:
        ax.spines[side].set_color(colors['axes'])
    ax.tick_params(axis='both', color=colors['axes'], labelcolor=colors['axes'])
    
    for tick in range(ticks): # random updates to price
        market.update_stock()
        prices.append(market.price)
        
        times.append(times[-1] + timedelta(minutes = 1))

    # convert times
    times = [t.strftime('%H:%M') for t in times]
        
    for tick in range(1, ticks): # plot bars
        prev = prices[tick-1]
        curr = prices[tick]

        if curr > prev:
            color = colors['green_bar']
        else:
            color = colors['red_bar']
            
        # plot new bar
        ax.bar(tick, curr - prev, bottom=prev, color=color, width=0.8)
    
        tick_delta = max([5, int(tick/5)]) # change spacing between ticks
        ax.set_xticks(range(0, tick, tick_delta))
        ax.set_xticklabels(times[::tick_delta])
    
        plt.pause(duration)    
    
    plt.ioff() # leave interactive mode
    plt.show()