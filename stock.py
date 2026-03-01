import numpy as np

from utils import read_yaml


class Stock:
    def __init__(self, name = '', price = 100):
        self.name = name
        self.price = price
        
    def update_price(self, delta):
        self.set_price(self.price + delta)
    
    def set_price(self, price):
        self.price = price        
        
        # account for bounds
        self.price = max([0, self.price])
        self.price = min([self.price, 1000])


class Market:
    # parameters for market regimes
    REGIMES = read_yaml('parameters')['regimes']
    
    def __init__(self):
        self.stock = Stock()
        
        # market variables
        self.mu = 0 # drift upward or downward
        self.base_vol = 0 # market stability
        self.df = 0 # rarity of crashes and spikes
   
        # set initial market regime
        self.set_regime('neutral')
        self.volatility = self.base_vol
        
    def __getattr__(self, attr): # only runs if missing attribute
        if attr == 'price':
            return self.stock.price
        
    def set_stock(self, *args, **kwargs):
        self.stock = Stock(*args, **kwargs)
        
    def set_regime(self, regime):
        if regime not in self.REGIMES:
            raise ValueError(f"Invalid market regime: {regime}")
            regime = 'neutral'
        
        # set market variables    
        for key in ['mu', 'base_vol', 'df']:
           setattr(self, key, self.REGIMES[regime][key])
        
    def update_volatility(self):
        self.volatility = np.random.normal(0, 0.001) # random noise
        
        # revert toward base
        self.volatility += 0.05 * (self.base_vol - self.volatility)
        
        # apply bounds
        self.volatility = max([0.02, self.volatility])
        self.volatility = min([self.volatility, 0.05])
        
    def update_stock(self):    
        self.update_volatility()
    
        # calculate shock from volatility
        scale = np.sqrt(self.df / (self.df - 2))
        shock = np.random.standard_t(self.df) * self.volatility / scale
    
        # adjust price
        new_price = self.price * np.exp(self.mu + shock)
        self.stock.set_price(new_price)
        