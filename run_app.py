"""
Run app with streamlit
"""
import streamlit as st
from streamlit_autorefresh import st_autorefresh

import matplotlib.pyplot as plt

from utils import read_yaml

from stock import Market
from display import Plotter

st_autorefresh(interval=1000, limit=None, key="auto_refresh_timer")

# initialize state
if "plotter" not in st.session_state:
    market = Market()
    market.set_stock(name = 'ABX')
    
    pl = Plotter()
    pl.calculate_prices(market)
    st.session_state.plotter = pl
    
if "tick" not in st.session_state:
    st.session_state.tick = 0
    
if 'colors' not in st.session_state:
    st.session_state.colors = read_yaml('style')
    
# increment tick
st.session_state.tick += 1

colors = st.session_state.colors

fig, ax = plt.subplots(facecolor=colors['bg'])
ax.set_facecolor(colors['bg'])

for side in ['bottom', 'top', 'left', 'right']:
    ax.spines[side].set_color(colors['axes'])
ax.tick_params(axis='both', color=colors['axes'], labelcolor=colors['axes'])

plt.grid(color=colors['grid'], linestyle='--', alpha=0.2)

for t in range(st.session_state.tick):
    st.session_state.plotter._plot_tick(ax, t)
    
st.pyplot(fig)