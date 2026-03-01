"""
Basic display in matplotlib
"""
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.gridspec import GridSpec
from PIL import Image, ImageTk

from utils import read_yaml


class PlotBase:
    """
    Base plot, holds subplots
    """
    COLORS = read_yaml('style')['colors']
    
    def __init__(self, size=(1,1)):
        plt.switch_backend('TkAgg')

        fig = plt.figure(facecolor=self.COLORS['bg'])
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
    
    def refresh(self):        
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()
    
    def end_plot(self):
        plt.ioff() # leave interactive mode
        plt.show()


class SubPlotBase:
    """
    Super class for all subplots
    """
    COLORS = read_yaml('style')['colors']
    DESIGN = read_yaml('style')['design']
    
    def __init__(self, base_fig, row, col, width=1, height=1):
        self.ax = base_fig.add_subplot(row, col, width, height)


class BarPlotter(SubPlotBase):
    """
    Super class for plotting bars
    Used for candlesticks and volume chart
    """
    def __init__(self, base_fig, row, col, width=1, height=1, plot_ticks=True):
        super().__init__(base_fig, row, col, width, height)
        
        self.plot_ticks = plot_ticks
        self.bars = []
        
        self.ax.set_facecolor(self.COLORS['bg']) # background color
        
        for side in ['bottom', 'top', 'left', 'right']: # set axes colors
            self.ax.spines[side].set_color(self.COLORS['axes'])
        self.ax.tick_params(axis='both', color=self.COLORS['axes'], labelcolor=self.COLORS['axes'])
        
        if self.DESIGN['axes_right']:
            self.ax.yaxis.tick_right()
        
        line = self.DESIGN['grid_line_style']
        alpha = self.DESIGN['grid_line_alpha']
        plt.grid(color=self.COLORS['grid'], linestyle=line, alpha=alpha) # grid lines
        
    def initialize_bars(self, num_bars):
        """
        Initialize based on number of bars
        """
        self.bars = self.ax.bar(range(num_bars), [0]*num_bars)
        
        buffer = self.DESIGN['x_lim_buffer']
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
    def __init__(self, base_fig, row, col, width=1, height=1, plot_ticks=True):
        super().__init__(base_fig, row, col, width, height, plot_ticks)
        
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
            num = t * 1000
            
            if num >= 1e6: # divide by million or thousand
                num /= 1e6
                suffix = 'M'
            elif num >= 1e3:
                num /= 1e3
                suffix = 'k'
            else:
                suffix = ''
            
            if num >= 10: # round
                num = round(num)
            else: # keep decimal if only 1s place
                num = round(num,1)
                
            if num.is_integer(): # convert to int if needed
                num = int(num)
                
            formatted_labels.append(str(num)+suffix)
        
        self.ax.set_yticks(yticks)
        self.ax.set_yticklabels(formatted_labels)
        
    def plot_tick(self, tick, price_engine):      
        self.plot_bars(tick, price_engine)
        self.set_y_lim(tick, price_engine)
        self.set_x_ticks(tick, price_engine)
    
        
class CandlestickPlotter(BarPlotter):
    """
    Plots candlestick chart
    Takes base plot as argument
    """
    def __init__(self, base_fig, row, col, width=1, height=1, plot_wicks=True, plot_ticks=True):
        super().__init__(base_fig, row, col, width, height, plot_ticks)
        
        self.plot_wicks = plot_wicks        
        self.wicks = []

    def initialize_bars(self, num_bars = 50):
        """
        Initialize based on number of bars
        """
        super().initialize_bars(num_bars)
        
        if self.plot_wicks: # add wicks if needed
            self.wicks = self.ax.vlines(range(num_bars), [0]*num_bars, [0]*num_bars)

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

        min_price = min(low_wicks) - self.DESIGN['y_lim_buffer']
        max_price = max(high_wicks) + self.DESIGN['y_lim_buffer']
        
        self.ax.set_ylim(min_price, max_price) # set y limits
        
    def plot_tick(self, tick, price_engine):      
        self.plot_bars(tick, price_engine)
        self.set_y_lim(tick, price_engine)
        self.set_x_ticks(tick, price_engine)
