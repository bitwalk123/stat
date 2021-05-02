#!/usr/bin/env python
# coding: utf-8
# Reference
# https://note.nkmk.me/python-pandas-matplotlib-candlestick-chart/
# https://stackoverflow.com/questions/60599812/how-can-i-customize-mplfinance-plot
import mplfinance as mpf
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)

filename = 'candlestick_sample_data.csv'
df = pd.read_csv(filename, index_col=0, parse_dates=True)
# df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

sty = mpf.make_mpf_style(base_mpf_style='yahoo', rc={'font.size': 6})
fig = mpf.figure(figsize=(10, 7), style=sty)
ax = fig.add_subplot(2, 1, 1)
av = fig.add_subplot(2, 1, 2, sharex=ax)
mpf.plot(df, type='candle', mav=(3, 6, 9), show_nontrading=True, datetime_format='%Y-%m-%d', ax=ax, volume=av)

plt.show()
