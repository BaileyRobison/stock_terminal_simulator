from datetime import datetime, timedelta
import numpy as np
import time

from display import PlotBase, CandlestickPlotter, VolumePlotter, HeaderPane
from utils import read_yaml


class Engine:
    """
    Runs everything
    """
    def __init__(self, market, settings = {}):  
        self.price_engine = PriceEngine(market)
        
        self.pl = PlotBase((5,3)) # base plot
        
        self.start_tick = settings.get('bars', 100) + 1
        
        # header with price and stats
        self.header_pane = HeaderPane(self.pl, 0, 0, 3, 1)
        self.header_pane.set_stock(self.price_engine)
        
        # short term candle chart
        self.candle_pl = CandlestickPlotter(self.pl, 1, 0, 3, 3)
        self.candle_pl.initialize_bars(num_bars = settings.get('bars', 100))
        
        # volume plot
        self.volume_pl = VolumePlotter(self.pl, 4, 0, 3, 1)
        self.volume_pl.initialize_bars(num_bars = settings.get('bars', 100))
        
        self.pl.fig.subplots_adjust(hspace=0)
        
        padding = read_yaml('style')['design']['figure_padding'] # remove extra padding outside plot
        self.pl.fig.subplots_adjust(left=padding, right=1-padding, top=1-padding, bottom=padding)
        
    def run(self, ticks = 100, duration = 0.1):
        for tick in range(1, self.start_tick): # initial bars
            self.price_engine.update()
        
        self.pl.start_plot()
        
        next_run = time.perf_counter() # start time before execution
        
        for tick in range(0, ticks): # plot ticks on both
            next_run += duration # time for next loop execution
            total_tick = tick + self.start_tick + 1 # total ticks so far
            
            self.price_engine.update()
            self.header_pane.update(self.price_engine)
            self.candle_pl.plot_tick(total_tick, self.price_engine)    
            self.volume_pl.plot_tick(total_tick, self.price_engine)    
            
            self.pl.refresh() # redraw updated plot
            
            sleep_time = next_run - time.perf_counter() # adjust sleep time
            if sleep_time > 0: # account for execution taking longer than delay
                time.sleep(sleep_time)
            
        self.pl.end_plot()
        
class PriceEngine:
    """
    Handles stock prices for candlestick chart
    """
    PARAMETERS = read_yaml('parameters')
    
    def __init__(self, market):
        self.market = market
                
        self.time_step = 1 # minutes
        self.time_format = '%H:%M'
        
        self.prices = [self.market.price]
        self.lows = [0]
        self.highs = [0]
        self.times = [datetime(2026,1,1,12,0).strftime(self.time_format)]
        
        self.volumes = [self.PARAMETERS['volume']['base_volume']]
        
    def update(self):
        # update stock price
        self.market.update_stock()
        self.prices.append(self.market.price)

        self.random_wicks()
        self.calculate_volume()

        # update time
        new_time = datetime.strptime(self.times[-1], self.time_format)
        new_time += timedelta(minutes = self.time_step)
        self.times.append(new_time.strftime(self.time_format))
        
    def random_wicks(self):
        open_price = self.prices[-2]
        close_price = self.prices[-1]
        
        # base size based on bar size
        base_wick = abs(close_price - open_price) * np.random.uniform(0.2, 0.6)
        wick_noise = open_price * self.market.volatility * 0.2
        
        # upper and lower wicks
        upper_wick = base_wick + abs(np.random.normal(0, wick_noise))
        lower_wick = base_wick + abs(np.random.normal(0, wick_noise))
        
        if close_price > open_price:  # directional logic, suppress opposite wick
            lower_wick *= 0.6
        else:
            upper_wick *= 0.6
            
        if np.random.rand() < 0.05: # random upper or lower spike
            spike_multiplier = np.random.uniform(1.5, 3)
            if np.random.rand() < 0.5:
                upper_wick *= spike_multiplier
            else:
                lower_wick *= spike_multiplier
                
        high = max(open_price, close_price) + upper_wick
        low = min(open_price, close_price) - lower_wick
        self.lows.append(low)
        self.highs.append(high)
        
    def calculate_volume(self):
        beta = self.PARAMETERS['volume']['beta']
        base_volume = self.PARAMETERS['volume']['base_volume']
        
        raw_vol = base_volume
        raw_vol *= (1 + 5*self.market.volatility) # effect of volatility
        raw_vol *= (1 + 3*abs(self.prices[-1] - self.prices[-2])) # price change
        raw_vol *= np.random.lognormal(mean=0, sigma=0.25) # noise
        
        # clustering
        last_vol = self.volumes[-1]
        volume = (beta * last_vol) + (raw_vol * (1 - beta))
        
        self.volumes.append(volume)
        