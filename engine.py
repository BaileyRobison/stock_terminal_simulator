from datetime import datetime, timedelta

from display import Plotter

class Engine:
    def __init__(self, market):
        self.market = market
        self.pl = None
        
        self.time_step = 1 # minutes
        self.time_format = '%H:%M'
        
        self.prices = [self.market.price]
        self.times = [datetime(2026,1,1,12,0).strftime(self.time_format)]
        
    def update(self):
        # update stock price
        self.market.update_stock()
        self.prices.append(self.market.price)

        # update time
        new_time = datetime.strptime(self.times[-1], self.time_format)
        new_time += timedelta(minutes = self.time_step)
        self.times.append(new_time.strftime(self.time_format))
        
    def run(self, ticks = 100, duration = 0.1):
        self.pl = Plotter(ticks, duration)
        self.pl.initialize_plot()
        
        for tick in range(1, ticks):
            self.update()
            self.pl.plot_tick(tick, self.prices, self.times)
            self.pl.pause(duration)
            
        self.pl.end_plot()