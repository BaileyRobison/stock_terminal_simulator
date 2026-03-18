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
        
        _ = self._plot_text(0.05, 0.95, "Time",  ha='left')
        _ = self._plot_text(0.6, 0.95, "Price", ha='right')
        _ = self._plot_text(0.95, 0.95, "Size",  ha='right')
        
        plt.grid(alpha=0) # no grid lines
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
    def _plot_text(self, x, y, text, ha='right'):
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
