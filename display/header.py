"""
Class to display stock ticker header
"""
from display.base import SubPlotBase


class HeaderPane(SubPlotBase):
    """
    Header with stock name, stats
    """
    def __init__(self, base_fig, row, col, width=1, height=1):
        super().__init__(base_fig, row, col, width, height)

        self.ax.axis("off")
        self.ax.set_facecolor(self.COLORS['bg'])
        
        # stock name and price
        self.stock_text = self.create_text(0.05, 0.9, fontsize='large_font')
        self.price_text = self.create_text(0.05, 0.5)
        
        # stat labels
        stat_x = [0.4, 0.5, 0.6] # position of stats
        stat_y = 0.7
        _ = self.create_text(stat_x[0], stat_y, text='24h High', color='header_text')
        _ = self.create_text(stat_x[1], stat_y, text='24h Low', color='header_text')
        _ = self.create_text(stat_x[2], stat_y, text='24h Volume', color='header_text')
        
        # stat text
        stat_y = 0.5
        self.high_text = self.create_text(stat_x[0], stat_y)
        self.low_text = self.create_text(stat_x[1], stat_y)
        self.volume_text = self.create_text(stat_x[2], stat_y)        
        
    def create_text(self, x, y, **kwargs):
        """
        Used to initialize text
        """
        text = kwargs.get('text', '')
        color = kwargs.get('color', 'axes')
        fontsize = kwargs.get('fontsize', 'small_font')
        
        return self.ax.text(
            x, y, text,
            transform=self.ax.transAxes,
            ha="left",
            va="center",
            fontsize=self.DESIGN['header'][fontsize],
            fontweight="bold",
            color=self.COLORS[color],
        )
        
    def set_stock(self, price_engine):
        """
        Set name of stock
        """
        self.stock_text.set_text(price_engine.market.stock.name)
        
    def update(self, price_engine):
        # price
        current_price = price_engine.prices[-1]
        percent_change = (current_price - price_engine.prices[0]) / price_engine.prices[0] * 100
        
        text = "${0:.2f} ({1:.2f}%)".format(current_price, percent_change)
        self.price_text.set_text(text)
        
        # stats
        window = 20
        high_price = max(price_engine.prices[-1*window:])
        low_price = min(price_engine.prices[-1*window:])
        tot_vol = sum(price_engine.volumes[-1*window:])
        
        # update text
        self.high_text.set_text("{0:.2f}".format(high_price))
        self.low_text.set_text("{0:.2f}".format(low_price))
        self.volume_text.set_text("{0:.2f}".format(tot_vol))
