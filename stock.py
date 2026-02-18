import random

class Stock:
    def __init__(self, name = '', price = 100):
        self.name = name
        self.price = price
        
    def update_price(self, delta):
        self.price += delta
        
        # account for bounds
        self.price = max([0, self.price])
        self.price = min([self.price, 1000])
        

class Market:
    def __init__(self):
        self.stocks = []
        self.market = 'neutral'
        
        self.regimes = {
            'neutral': (-10, 10),
            'bull': (-5, 15),
            'bear': (-15, 5),
            'crash': (-20, -5),
            'rally': (5, 20),
        }
    
    def __getattr__(self, attr):
        # only runs if missing attribute
        if attr == 'price':
            return self.stocks[0].price
        
    def add_stock(self, *args, **kwargs):
        stock = Stock(*args, **kwargs)
        self.stocks.append(stock)
        
    def set_regime(self, regime):
        if regime not in self.regimes:
            raise ValueError(f"Invalid market regime: {regime}")
            regime = 'neutral'
        
        self.regime = regime
        
    def update_stock(self):
        lower, upper = self.regimes[self.regime]
        
        r = random.randint(lower, upper)
        self.stocks[0].update_price(r)
        