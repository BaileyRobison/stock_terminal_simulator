from datetime import datetime, timedelta
import numpy as np

from display import Plotter

class Engine:
    def __init__(self, market):
        self.market = market
        self.pl = None
        
        self.time_step = 1 # minutes
        self.time_format = '%H:%M'
        
        self.prices = [self.market.price]
        self.lows = [0]
        self.highs = [0]
        self.times = [datetime(2026,1,1,12,0).strftime(self.time_format)]
        
    def update(self):
        # update stock price
        self.market.update_stock()
        self.prices.append(self.market.price)

        self.random_wicks()

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
        
    def run(self, ticks = 100, duration = 0.1):
        self.pl = Plotter(ticks, duration)
        self.pl.initialize_plot()
        
        for tick in range(1, ticks):
            self.update()
            self.pl.plot_tick(tick, self.prices, self.times, self.lows, self.highs)            
            self.pl.pause(duration)
            
        self.pl.end_plot()