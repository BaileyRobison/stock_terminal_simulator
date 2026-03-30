"""
Panel which displays the trades that have taken place
"""
import matplotlib.pyplot as plt
from display.base import SubPlotBase

class TradeBook(SubPlotBase):
    def __init__(self, base_fig, row, col, width=1, height=1):
        super().__init__(base_fig, row, col, width, height)
        
        self.ax.set_facecolor(self.COLORS['bg'])
        
        for side in ['bottom', 'top', 'left', 'right']: # set axes colors
            self.ax.spines[side].set_color(self.COLORS['axes'])
        self.ax.tick_params(axis='both', color=self.COLORS['axes'], labelcolor=self.COLORS['axes'])
        
        _ = self._plot_header_text(0.05, 0.965, "Time",  ha='left')
        _ = self._plot_header_text(0.6, 0.965, "Price", ha='right')
        _ = self._plot_header_text(0.95, 0.965, "Size",  ha='right')
        
        self.ax.axhline(0.9, color='gray', linewidth=0.5) # line under header
        
        # initialize trade text
        self.trade_rows = []
        self._init_trade_text()
        
        plt.grid(alpha=0) # no grid lines
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
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
        self.max_rows = 10
        line_height = 0.8 / self.max_rows
        self.trade_rows = []
        
        for i in range(self.max_rows):
            y = 0.925 - (i + 1) * line_height
            
            ax_txt = self.ax.text(
                0.05, y, '',
                transform=self.ax.transAxes,
                family='monospace',
                verticalalignment='top',
                fontsize=self.DESIGN['header']['trades_font'],
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
            