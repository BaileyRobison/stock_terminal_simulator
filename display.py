"""
Basic display in matplotlib
"""
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

from utils import read_yaml


class Plotter:
    def __init__(self, ticks = 100, duration = 0.1):
        self.colors = read_yaml('style')
        
        self.prices = []
        self.times = []
        
        self.ticks = ticks
        self.duration = duration
        
    def calculate_prices(self, market):
        """
        Calculate stock prices from market
        """
        prices = [market.price]
        times = [datetime(2026,1,1,12,0)]
            
        for tick in range(self.ticks): # random updates to price
            market.update_stock()
            prices.append(market.price)
            
            times.append(times[-1] + timedelta(minutes = 1))
            
        self.prices = prices
        self.times = [t.strftime('%H:%M') for t in times] # convert times
    
    def _plot_tick(self, ax, tick):
        """
        Plot bar for single tick
        """
        prev = self.prices[tick-1]
        curr = self.prices[tick]

        if curr > prev:
            color = self.colors['green_bar']
        else:
            color = self.colors['red_bar']
            
        # plot new bar
        ax.bar(tick, curr - prev, bottom=prev, color=color, width=0.8)
    
        tick_delta = max([5, int(tick/5)]) # change spacing between ticks
        ax.set_xticks(range(0, tick, tick_delta))
        ax.set_xticklabels(self.times[::tick_delta])
    
    def plot(self):
        """
        Generate entire plot with all bars
        """
        plt.ion() # enter interactive mode
        fig, ax = plt.subplots(facecolor=self.colors['bg'])
        ax.set_facecolor(self.colors['bg'])
        
        for side in ['bottom', 'top', 'left', 'right']:
            ax.spines[side].set_color(self.colors['axes'])
        ax.tick_params(axis='both', color=self.colors['axes'], labelcolor=self.colors['axes'])
        
        plt.grid(color=self.colors['grid'], linestyle='--', alpha=0.2)
        
        for tick in range(1, self.ticks):
            self._plot_tick(ax, tick)
            plt.pause(self.duration)
            
        plt.ioff() # leave interactive mode
        plt.show()
        
    def plot_stock_price(self, market, ticks = None, duration = None):
        """
        Run everything required for plotting
        """
        if ticks is not None: # override if given
            self.ticks = ticks
        if duration is not None:
            self.duration = duration
            
        self.calculate_prices(market)
        self.plot()