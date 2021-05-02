#!/usr/bin/env python
# coding: utf-8
# Reference
# https://note.nkmk.me/python-pandas-matplotlib-candlestick-chart/
import mplfinance as mpf
import pandas as pd

filename = 'candlestick_sample_data.csv'
df = pd.read_csv(filename, index_col=0, parse_dates=True)
# df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

mpf.plot(df, type='candle', style='yahoo', volume=True, mav=(3, 6, 9),
         show_nontrading=True, datetime_format='%Y-%m-%d',
         savefig='candlestick_chart.png')
