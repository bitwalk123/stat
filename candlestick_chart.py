#!/usr/bin/env python
# coding: utf-8
# Reference
# https://note.nkmk.me/python-pandas-matplotlib-candlestick-chart/
import mplfinance as mpf
import pandas as pd

df = pd.read_csv('candlestick_sample_data.csv', index_col=0, parse_dates=True)
df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
mpf.plot(df, type='candle', volume=True, mav=(5, 25), style='yahoo', show_nontrading=True, figratio=(12, 4))
