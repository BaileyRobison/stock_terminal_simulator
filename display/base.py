"""
Base classes for display in matplotlib
"""
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from PIL import Image, ImageTk

from utils import read_yaml


class PlotBase:
    """
    Base plot, holds subplots
    """
    COLORS = read_yaml('style')['colors']
    
    def __init__(self, size=(1,1)):
        plt.switch_backend('TkAgg')

        fig = plt.figure(facecolor=self.COLORS['bg'], constrained_layout=False)
        fig.canvas.manager.toolbar.pack_forget() # remove toolbar and buttons
        fig.canvas.manager.window.title('TERMINAL') # window name

        # cover entire screen        
        fig_manager = plt.get_current_fig_manager()
        fig_manager.window.state('zoomed')

        white_image = Image.new('RGB', (1, 1), (255, 255, 255)) # 1x1 white image
        white_image_tk = ImageTk.PhotoImage(white_image)
        fig.canvas.manager.window.iconphoto(False, white_image_tk) # replace matplotlib logo

        self.fig = fig
        self.gs = GridSpec(size[0], size[1], figure=self.fig, left=0.01, right=0.99, top=1, bottom=0.05, hspace=0)
        
    def add_subplot(self, row, col, width=1, height=1):
        """
        Add another plotting object as a subplot
        Return and use in class constructor
        """
        ax = self.fig.add_subplot(self.gs[row:row+height, col:col+width])
        return ax
    
    def start_plot(self):
        plt.ion() # enter interactive mode
    
    def refresh(self):        
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()
    
    def end_plot(self):
        plt.ioff() # leave interactive mode
        plt.show()


class SubPlotBase:
    """
    Super class for all subplots
    """
    COLORS = read_yaml('style')['colors']
    DESIGN = read_yaml('style')['design']
    
    def __init__(self, base_fig, row, col, width=1, height=1):
        self.ax = base_fig.add_subplot(row, col, width, height)