"""
Panel which displays the trades that have taken place
"""
import matplotlib.pyplot as plt
from display.base import SubPlotBase

class TradeBook(SubPlotBase):
    def __init__(self, base_fig, row, col, width=1, height=1):
        super().__init__(base_fig, row, col, width, height)
        
        for side in ['bottom', 'top', 'left', 'right']: # set axes colors
            self.ax.spines[side].set_color(self.COLORS['axes'])
        self.ax.tick_params(axis='both', color=self.COLORS['axes'], labelcolor=self.COLORS['axes'])
        
        # plot header
        _ = self._plot_header_text(0.05, 0.965, "Time",  ha='left')
        _ = self._plot_header_text(0.6, 0.965, "Price", ha='right')
        _ = self._plot_header_text(0.95, 0.965, "Size",  ha='right')
        
        self.ax.axhline(0.9, color='gray', linewidth=0.5) # line under header
        
        # initialize trade text
        self.max_rows = 16
        self.trade_rows = []
        self._init_trade_text()
        
        plt.grid(alpha=0) # no grid lines
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        
    def _plot_header_text(self, x, y, text, ha='right'):
        """
        Used to initialize text
        """
        return self.ax.text(
            x, y, text,
            transform=self.ax.transAxes,
            ha=ha,
            va="top",
            fontsize=self.DESIGN['header']['stat_font'],
            fontweight="bold",
            color=self.COLORS['header_text'],
        )
    
    def _init_trade_text(self):
        """
        Initialize trade text with empty string, update later
        """
        line_height = 0.8 / self.max_rows
        self.trade_rows = []
        
        for i in range(self.max_rows):
            y = 0.925 - (i + 1) * line_height
            alpha = 1 - (i / self.max_rows) * 0.7 # dim older rows
            
            ax_txt = self.ax.text(
                0.05, y, '',
                alpha=alpha,
                transform=self.ax.transAxes,
                family='monospace',
                verticalalignment='top',
                fontsize=self.DESIGN['font']['trades_font'],
                fontweight="bold",
                color=self.COLORS['trade_text'],
            )
            
            self.trade_rows.append(ax_txt)
    
    def update_trades(self, price_engine):
        """
        Update trade text with text from price engine
        """
        # only plot most recent trades
        trades = price_engine.trades[-1 * self.max_rows:]
        
        for i in range(self.max_rows):
            if i < len(trades): # for when we have less trades than max rows
                time, price, volume = trades[::-1][i] # plot last trade first
                text = f"{time:<8} {price:>8} {volume:>9}" # format spacing
                self.trade_rows[i].set_text(text)
            
            
class OrderBook(SubPlotBase):
    def __init__(self, base_fig, row, col, width=1, height=1):
        super().__init__(base_fig, row, col, width, height)
        
        for side in ['bottom', 'top', 'left', 'right']: # set axes colors
            self.ax.spines[side].set_color(self.COLORS['axes'])
            self.ax.tick_params(axis='both', color=self.COLORS['axes'], labelcolor=self.COLORS['axes'])
            
        # plot header
        _ = self._plot_header_text(0.2, 0.965, "Bids",  ha='left')
        _ = self._plot_header_text(0.8, 0.965, "Asks", ha='right')
        
        self.ax.axhline(0.9, color='gray', linewidth=0.5) # line under header

        # bid and ask text
        self.max_rows = 8
        self.bid_rows = []
        self.ask_rows = []
        self._init_bid_ask_text()

        plt.grid(alpha=0) # no grid lines
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        
    def _plot_header_text(self, x, y, text, ha='right'):
        """
        Used to initialize text
        """
        return self.ax.text(
            x, y, text,
            transform=self.ax.transAxes,
            ha=ha,
            va="top",
            fontsize=self.DESIGN['header']['stat_font'],
            fontweight="bold",
            color=self.COLORS['header_text'],
        )
    
    def _init_bid_ask_text(self):
        """
        Initialize order book text with empty strings, update later
        """
        line_height = 0.8 / self.max_rows
        self.trade_rows = []
        
        for i in range(self.max_rows):
            y = 0.925 - (i + 1) * line_height

            bid_txt = self.ax.text( # bid on left
                0.05, y, "",
                color=self.COLORS['order_text'],
                fontsize=self.DESIGN['font']['order_font'],
                family='monospace',
                verticalalignment='top'
            )
            self.bid_rows.append(bid_txt)
    
            divider = self.ax.text( # divider in middle
                0.5, y, "|",
                color=self.COLORS['order_text'],
                fontsize=self.DESIGN['font']['order_font'],
                family='monospace',
                verticalalignment='top',
                horizontalalignment='center'
            )

            ask_txt = self.ax.text( # ask on right
                0.55, y, "",
                color=self.COLORS['order_text'],
                fontsize=self.DESIGN['font']['order_font'],
                family='monospace',
                verticalalignment='top'
            )
            self.ask_rows.append(ask_txt)

    def update_book(self, price_engine):
        bids = price_engine.bids
        asks = price_engine.asks
        
        for i in range(self.max_rows):
            if i < len(bids):
                bid_price, bid_size = bids[i]
                bid_text = f"{bid_size:>4} {bid_price:>7}"

            if i < len(asks):
                ask_price, ask_size = asks[i]
                ask_text = f"{ask_price:<7} {ask_size:<4}"

            self.bid_rows[i].set_text(bid_text)
            self.ask_rows[i].set_text(ask_text)