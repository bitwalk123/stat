#!/usr/bin/env python
# coding: utf-8
# Reference
# https://saralgyaan.com/posts/python-candlestick-chart-matplotlib-tutorial-chapter-11/
import matplotlib.pyplot as plt
# from mpl_finance import candlestick_ohlc
import mplfinance as mpf
import pandas as pd
import matplotlib.dates as mpl_dates

plt.style.use('ggplot')

# Extracting Data for plotting
#data = pd.read_csv('candlestick_python_data.csv')
#ohlc = data.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]
#ohlc['Date'] = pd.to_datetime(ohlc['Date'])
#ohlc['Date'] = ohlc['Date'].apply(mpl_dates.date2num)
#ohlc = ohlc.astype(float)

daily = pd.read_csv('candlestick_python_data.csv',index_col=0,parse_dates=True)
daily.index.name = 'Date'
daily.shape
daily.head(3)
daily.tail(3)
# Creating Subplots
#fig, ax = plt.subplots()

mpf.plot(daily, type='candle')

# Setting labels & titles
#ax.set_xlabel('Date')
#ax.set_ylabel('Price')
#fig.suptitle('Daily Candlestick Chart of NIFTY50')

# Formatting Date
#date_format = mpl_dates.DateFormatter('%d-%m-%Y')
#ax.xaxis.set_major_formatter(date_format)
#fig.autofmt_xdate()

#fig.tight_layout()

#plt.show()
