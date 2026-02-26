"""
Basic display in matplotlib
"""
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from PIL import Image, ImageTk
import time

from utils import read_yaml


class PlotBase:
    """
    Base plot, holds subplots
    """
    def __init__(self, size=(1,1)):
        self.colors = read_yaml('style')

        plt.switch_backend('TkAgg')

        fig = plt.figure(facecolor=self.colors['bg'])
        fig.canvas.manager.toolbar.pack_forget() # remove toolbar and buttons
        fig.canvas.manager.window.title('TERMINAL') # window name

        # cover entire screen        
        fig_manager = plt.get_current_fig_manager()
        fig_manager.window.state('zoomed')

        white_image = Image.new('RGB', (1, 1), (255, 255, 255)) # 1x1 white image
        white_image_tk = ImageTk.PhotoImage(white_image)
        fig.canvas.manager.window.iconphoto(False, white_image_tk) # replace matplotlib logo

        self.fig = fig
        self.gs = GridSpec(size[0], size[1], figure=self.fig)
        
    def add_subplot(self, row, col, width=1, height=1):
        """
        Add another plotting object as a subplot
        Return and use in class constructor
        """
        ax = self.fig.add_subplot(self.gs[row:row+height, col:col+width])
        return ax
    
    def start_plot(self):
        plt.ion() # enter interactive mode
    
    def pause(self, duration):        
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()
    
        time.sleep(duration)
    
    def end_plot(self):
        plt.ioff() # leave interactive mode
        plt.show()


class CandlestickPlotter:
    """
    Plots candlestick chart
    Takes base plot as argument
    """
    def __init__(self, base_fig, row, col, width=1, height=1, plot_wicks=True, plot_ticks=True):
        self.plot_wicks = plot_wicks
        self.plot_ticks = plot_ticks
        self.colors = read_yaml('style')
        
        self.ax = base_fig.add_subplot(row, col, width, height)
        
        self.ax.set_facecolor(self.colors['bg'])
        
        for side in ['bottom', 'top', 'left', 'right']:
            self.ax.spines[side].set_color(self.colors['axes'])
        self.ax.tick_params(axis='both', color=self.colors['axes'], labelcolor=self.colors['axes'])
        
        plt.grid(color=self.colors['grid'], linestyle='--', alpha=0.2)

        self.bars = []
        self.wicks = []

    def initialize_bars(self, num_bars = 50):
        self.bars = self.ax.bar(range(num_bars), [0]*num_bars)
        
        buffer = 2
        self.ax.set_xlim(-1 * buffer, num_bars + buffer)
        
        if self.plot_wicks: # add wicks if needed
            self.wicks = self.ax.vlines(range(num_bars), [0]*num_bars, [0]*num_bars)
        
        if not self.plot_ticks:
            self.ax.set_xticks([])
            self.ax.set_yticks([])

    def plot_tick(self, tick, price_engine):      
        # for wicks
        segments = []
        colors = []
        
        for i, rect in enumerate(self.bars): # loop over bars and set
            plot_tick = tick - len(self.bars) + i # bar positions
            
            prev = price_engine.prices[plot_tick-1] # previous price for bar
            curr = price_engine.prices[plot_tick] # current price for bar
            
            if curr > prev: # set color based on change
                bar_color = self.colors['green_bar']
            else:
                bar_color = self.colors['red_bar']
            colors.append(bar_color)
            
            rect.set_y(min(prev, curr)) # set bottom of bar
            rect.set_height(abs(curr - prev)) # set height of bar
            rect.set_facecolor(bar_color) # set color of bar
            
            segments.append([(i, price_engine.lows[plot_tick]), (i, price_engine.highs[plot_tick])])
            
        if self.plot_wicks: # set wick lengths and colors
            self.wicks.set_segments(segments)
            self.wicks.set_color(colors)

        # set y limits
        if self.plot_wicks: # include wicks in y lim
            low_wicks = price_engine.lows[tick-len(self.bars):tick]
            high_wicks = price_engine.highs[tick-len(self.bars):tick]
        else:
            low_wicks = price_engine.prices[tick-len(self.bars):tick]
            high_wicks = price_engine.prices[tick-len(self.bars):tick]

        buffer = 2
        min_price = min(low_wicks) - buffer
        max_price = max(high_wicks) + buffer
        
        self.ax.set_ylim(min_price, max_price)
        
        # ticks
        if self.plot_ticks:
            times = price_engine.times[tick-len(self.bars):tick]
                    
            tick_positions = []
            tick_times = []
            for i in range(len(times)):
                
                if times[i][-2:] in ['00', '15', '30', '45']:
                    tick_positions.append(i)
                    tick_times.append(times[i])
                            
            self.ax.set_xticks(tick_positions)
            self.ax.set_xticklabels(tick_times)
