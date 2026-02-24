"""
Basic display in matplotlib
"""
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from PIL import Image, ImageTk

from utils import read_yaml



class PlotBase:
    """
    Base plot, holds subplots
    """
    def __init__(self):
        self.colors = read_yaml('style')
        
        plt.switch_backend('TkAgg')
        
        fig = plt.figure(figsize=(12, 8), facecolor=self.colors['bg'])
        fig.canvas.manager.toolbar.pack_forget() # remove toolbar and buttons
        fig.canvas.manager.window.title('TERMINAL') # window name
        fig.set_tight_layout(True) # remove extra padding outside plot
        
        white_image = Image.new('RGB', (1, 1), (255, 255, 255)) # 1x1 white image
        white_image_tk = ImageTk.PhotoImage(white_image)
        fig.canvas.manager.window.iconphoto(False, white_image_tk) # replace matplotlib logo

        self.fig = fig
        self.gs = GridSpec(1, 1, figure=self.fig)
        
    def add_subplot(self, row, col, width=1, height=1):
        """
        Add another plotting object as a subplot
        Return and use in class constructor
        """
        ax = self.fig.add_subplot(self.gs[row:row+height, col:col+width])
        return ax
    
    def start_plot():
        plt.ion() # enter interactive mode
    
    def pause(self, duration):
        plt.pause(duration)
    
    def end_plot(self):
        plt.ioff() # leave interactive mode
        plt.show()
        
class CandlestickPlotter:
    """
    Plots candlestick chart
    Takes base plot as argument
    """
    def __init__(self, base_fig):
        self.colors = read_yaml('style')
        
        self.ax = base_fig.add_subplot(0, 0)
        
        self.ax.set_facecolor(self.colors['bg'])
        
        for side in ['bottom', 'top', 'left', 'right']:
            self.ax.spines[side].set_color(self.colors['axes'])
        self.ax.tick_params(axis='both', color=self.colors['axes'], labelcolor=self.colors['axes'])
        
        plt.grid(color=self.colors['grid'], linestyle='--', alpha=0.2)

    def plot_tick(self, tick, price_engine):
        """
        Plot bar for single tick
        """
        prev = price_engine.prices[tick-1]
        curr = price_engine.prices[tick]

        if curr > prev:
            bar_color = self.colors['green_bar']
        else:
            bar_color = self.colors['red_bar']
            
        # plot wicks    
        self.ax.vlines(tick, price_engine.lows[tick], price_engine.highs[tick], lw=1, color=bar_color)
        
        # plot new bar
        self.ax.bar(tick, curr - prev, bottom=prev, color=bar_color, width=0.8)
    
        tick_delta = max([5, int(tick/5)]) # change spacing between ticks
        self.ax.set_xticks(range(0, tick, tick_delta))
        self.ax.set_xticklabels(price_engine.times[::tick_delta])
