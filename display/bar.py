"""
Classes to plot bar charts
"""
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np

from display.base import SubPlotBase     
from utils import format_num_display

    
class BarPlotter(SubPlotBase):
    """
    Super class for plotting bars
    Used for candlesticks and volume chart
    """
    def __init__(self, base_fig, row, col, width=1, height=1, plot_ticks=True):
        super().__init__(base_fig, row, col, width, height)
        
        self.plot_ticks = plot_ticks
        self.bars = []
        
        for side in ['bottom', 'top', 'left', 'right']: # set axes colors
            self.ax.spines[side].set_color(self.COLORS['axes'])
        self.ax.tick_params(axis='both', color=self.COLORS['axes'], labelcolor=self.COLORS['axes'])
        
        if self.DESIGN['axes_right']:
            self.ax.yaxis.tick_right()
        
        line = self.DESIGN['grid_line']['style']
        alpha = self.DESIGN['grid_line']['alpha']
        plt.grid(color=self.COLORS['grid'], linestyle=line, alpha=alpha) # grid lines
        
    def initialize_bars(self, num_bars):
        """
        Initialize based on number of bars
        """
        self.bars = self.ax.bar(range(num_bars), [0]*num_bars)
        
        buffer = self.DESIGN['lim_buffer']['x_axis']
        self.ax.set_xlim(-1 * buffer, num_bars + buffer)
        
        if not self.plot_ticks:
            self.ax.set_xticks([])
            self.ax.set_yticks([])
        
    def set_x_ticks(self, tick, price_engine):
        """
        Set tick positions and labels, time labels move left over time
        """
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
            

class VolumePlotter(BarPlotter):
    def __init__(self, base_fig, row, col, width=1, height=1, plot_ticks=True, plot_mean=True):
        super().__init__(base_fig, row, col, width, height, plot_ticks)
        
        self.plot_mean = plot_mean
        
        # update line when plotting mean
        line = self.DESIGN['volume_mean']['style']
        alpha = self.DESIGN['volume_mean']['alpha']
        color = self.COLORS['mean_line']
        self.mean_line, = self.ax.plot([], [], linestyle=line, alpha=alpha, color=color)
        
        plt.grid(alpha=0) # no grid lines
        
    def initialize_bars(self, num_bars = 50):
        """
        Initialize based on number of bars
        """
        super().initialize_bars(num_bars)
        
        for rect in self.bars:
            rect.set_facecolor(self.COLORS['volume_bar'])
            rect.set_alpha(self.DESIGN['volume_bar_alpha'])
    
    def plot_bars(self, tick, price_engine):
        """
        Adjust heights, positions, colors for bars
        """       
        for i, rect in enumerate(self.bars): # loop over bars and set
            plot_tick = tick - len(self.bars) + i # bar positions
            
            vol = price_engine.volumes[plot_tick]
            rect.set_height(vol) # set height of bar

    def set_y_lim(self, tick, price_engine):
        """
        Scale y axis, account for whether or not we are plotting wicks
        """
        max_vol = max(price_engine.volumes[tick-len(self.bars):tick])
        max_vol *= 1.1
        
        self.ax.set_ylim(0, max_vol) # set y limits
        
        self.set_ytick_labels()
        
    def set_ytick_labels(self):
        self.ax.yaxis.set_major_locator(MaxNLocator(integer=True, prune='lower', nbins=4))
        yticks = self.ax.get_yticks()
        
        formatted_labels = []
        for t in yticks: # format numbers            
            f_num = format_num_display(t * 1000) # format for display
            formatted_labels.append(f_num)
        
        formatted_labels[-1] = '' # hide top label to avoid overlap
        
        self.ax.set_yticks(yticks)
        self.ax.set_yticklabels(formatted_labels)
        
    def plot_mean_line(self, tick, price_engine):
        mean_window = 20
        mean = np.median(price_engine.volumes[tick-mean_window:tick])
        
        buffer = self.DESIGN['lim_buffer']['x_axis']
        x_vals = [-1*buffer, len(self.bars)+buffer]
        y_vals = [mean, mean]
        self.mean_line.set_data(x_vals, y_vals)
        
    def plot_tick(self, tick, price_engine):      
        self.plot_bars(tick, price_engine)
        self.set_y_lim(tick, price_engine)
        
        if self.plot_mean:
            self.plot_mean_line(tick, price_engine)
        
        self.set_x_ticks(tick, price_engine)
    
        
class CandlestickPlotter(BarPlotter):
    """
    Plots candlestick chart
    Takes base plot as argument
    """
    def __init__(self, base_fig, row, col, width=1, height=1, plot_wicks=True, plot_ticks=True):
        super().__init__(base_fig, row, col, width, height, plot_ticks)
        
        self.plot_ticks = plot_ticks
        self.plot_wicks = plot_wicks        
        self.wicks = []

        line = self.DESIGN['last_price']['style']
        alpha = self.DESIGN['last_price']['alpha']
        color = self.COLORS['price_line']
        self.price_line, = self.ax.plot([], [], linestyle=line, alpha=alpha, color=color)

        self.price_marker = None

    def initialize_bars(self, num_bars = 50):
        """
        Initialize based on number of bars
        """
        super().initialize_bars(num_bars)
        
        if self.plot_wicks: # add wicks if needed
            self.wicks = self.ax.vlines(range(num_bars), [0]*num_bars, [0]*num_bars)
            
        if self.plot_ticks: # last price marker
            self.price_marker = self.ax.text(
                len(self.bars) + self.DESIGN['lim_buffer']['x_axis'],
                0,
                "",
                ha='left',
                va='center',
                color=self.COLORS['axes'],
                bbox=dict(
                    boxstyle="round,pad=0.2",
                    facecolor=self.COLORS['bg'],
                    edgecolor=self.COLORS['axes']
                )
            )

    def plot_bars(self, tick, price_engine):
        """
        Adjust heights, positions, colors for bars
        """
        # for wicks
        segments = []
        colors = []
        
        for i, rect in enumerate(self.bars): # loop over bars and set
            plot_tick = tick - len(self.bars) + i # bar positions
            
            prev = price_engine.prices[plot_tick-1] # previous price for bar
            curr = price_engine.prices[plot_tick] # current price for bar
            
            if curr > prev: # set color based on change
                bar_color = self.COLORS['green_bar']
            else:
                bar_color = self.COLORS['red_bar']
            colors.append(bar_color)
            
            rect.set_y(min(prev, curr)) # set bottom of bar
            rect.set_height(abs(curr - prev)) # set height of bar
            rect.set_facecolor(bar_color) # set color of bar
            
            segments.append([(i, price_engine.lows[plot_tick]), (i, price_engine.highs[plot_tick])])
            
        if self.plot_wicks: # set wick lengths and colors
            self.wicks.set_segments(segments)
            self.wicks.set_color(colors)

    def set_y_lim(self, tick, price_engine):
        """
        Scale y axis, account for whether or not we are plotting wicks
        """
        if self.plot_wicks: # include wicks in y lim
            low_wicks = price_engine.lows[tick-len(self.bars):tick]
            high_wicks = price_engine.highs[tick-len(self.bars):tick]
        else:
            low_wicks = price_engine.prices[tick-len(self.bars):tick]
            high_wicks = price_engine.prices[tick-len(self.bars):tick]

        min_price = min(low_wicks) - self.DESIGN['lim_buffer']['y_axis']
        max_price = max(high_wicks) + self.DESIGN['lim_buffer']['y_axis']
        
        self.ax.set_ylim(min_price, max_price) # set y limits
        
    def last_price_marker(self, price_engine):
        last_price = price_engine.prices[-1]
        
        # draw line
        buffer = self.DESIGN['lim_buffer']['x_axis']
        x_vals = [len(self.bars) - 1, len(self.bars)+buffer]
        y_vals = [last_price, last_price]        
        self.price_line.set_data(x_vals, y_vals)
        
        # set marker
        self.price_marker.set_position((len(self.bars)+buffer, last_price))
        self.price_marker.set_text('{0:.2f}'.format(last_price))
        
    def plot_tick(self, tick, price_engine):      
        self.plot_bars(tick, price_engine)
        self.set_y_lim(tick, price_engine)
        
        if self.plot_ticks:
            self.last_price_marker(price_engine)
        
        self.set_x_ticks(tick, price_engine)
