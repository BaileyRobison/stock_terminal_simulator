from datetime import datetime, timedelta
import numpy as np
import time

from display.base import PlotBase
from display.bar import CandlestickPlotter, VolumePlotter
from display.header import HeaderPane
from display.trade_book import TradeBook, OrderBook
from utils import read_yaml, format_num_display


class Engine:
    """
    Runs everything
    """
    def __init__(self, market, settings = {}):  
        self.price_engine = PriceEngine(market)
        
        self.pl = PlotBase((6,6)) # base plot
        
        self.start_tick = settings.get('bars', 100) + 1
        
        # header with price and stats
        self.header_pane = HeaderPane(self.pl, 0, 0, 5, 1)
        self.header_pane.set_stock(self.price_engine)
        
        # short term candle chart
        self.candle_pl = CandlestickPlotter(self.pl, 1, 0, 5, 4)
        self.candle_pl.initialize_bars(num_bars = settings.get('bars', 100))
        
        # volume plot
        self.volume_pl = VolumePlotter(self.pl, 5, 0, 5, 1)
        self.volume_pl.initialize_bars(num_bars = settings.get('bars', 100))
        
        self.trade_book = TradeBook(self.pl, 1, 5, 1, 2)
        self.order_book = OrderBook(self.pl, 4, 5, 1, 2)
        
        self.pl.fig.subplots_adjust(hspace=0, wspace=0.25)
        
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
            self.trade_book.update_trades(self.price_engine)
            
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
        
        self.trades = [] # (time, price, size)
        
    def update(self):
        # update time
        new_time = datetime.strptime(self.times[-1], self.time_format)
        new_time += timedelta(minutes = self.time_step)
        self.times.append(new_time.strftime(self.time_format))

        # update stock price
        self.market.update_stock()
        self.prices.append(self.market.price)

        self.random_wicks()

        self.calculate_volume()
        
        self.update_trades()
        
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

    def update_trades(self):
        n_trades = np.random.poisson(lam=2) # number of trades to generate
        
        # how many seconds have elapsed
        current_time = datetime.strptime(self.times[-1], self.time_format)
        old_time = current_time - timedelta(minutes = self.time_step)
        num_seconds = (current_time - old_time).total_seconds()
        
        # generate all elements of trade
        trade_times = []
        trade_prices = []
        trade_vols = []
        for n in range(n_trades):
            # random new time, between last time and current time
            secs = np.random.randint(0, num_seconds) # random number of seconds
            trade_time = old_time + timedelta(seconds = secs)
            trade_times.append(trade_time.strftime('%H:%M:%S'))
            
            # random price between high and low wicks
            trade_price = np.random.uniform(self.lows[-1], self.highs[-1])
            trade_prices.append('{0:.2f}'.format(trade_price))
            
            # volume
            max_vol = self.volumes[-1] / n_trades # max volume this trade can have
            volume = np.random.uniform(0, max_vol * 100)
            
            trade_vols.append(format_num_display(volume))
            
        trade_times.sort() # sort to add to trade log in order
        
        # build trades
        for i in range(n_trades):
            self.trades.append((trade_times[i], trade_prices[i], trade_vols[i]))
        