"""
Basic display in matplotlib
"""
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from utils import read_yaml


class Plotter:
    def __init__(self, ticks = 100, duration = 0.1):
        self.colors = read_yaml('style')
        
        self.ticks = ticks
        self.duration = duration
        
        self.ax = None
    
    def initialize_plot(self):
        fig = plt.figure(figsize=(12, 8), facecolor=self.colors['bg'])
        gs = GridSpec(1, 1, figure=fig)
        self.ax = fig.add_subplot(gs[0])
        self.ax.set_facecolor(self.colors['bg'])
        
        for side in ['bottom', 'top', 'left', 'right']:
            self.ax.spines[side].set_color(self.colors['axes'])
        self.ax.tick_params(axis='both', color=self.colors['axes'], labelcolor=self.colors['axes'])
        
        plt.grid(color=self.colors['grid'], linestyle='--', alpha=0.2)
        
        plt.ion() # enter interactive mode

    def plot_tick(self, tick, prices, times):
        """
        Plot bar for single tick
        """
        prev = prices[tick-1]
        curr = prices[tick]

        if curr > prev:
            color = self.colors['green_bar']
        else:
            color = self.colors['red_bar']
            
        # plot new bar
        self.ax.bar(tick, curr - prev, bottom=prev, color=color, width=0.8)
    
        tick_delta = max([5, int(tick/5)]) # change spacing between ticks
        self.ax.set_xticks(range(0, tick, tick_delta))
        self.ax.set_xticklabels(times[::tick_delta])
    
    def pause(self, duration):
        plt.pause(duration)
    
    def end_plot(self):
        plt.ioff() # leave interactive mode
        plt.show()
