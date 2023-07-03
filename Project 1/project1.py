# This is an equal weight S&P 500 Index Fund Project

#imports

import finnhub
import numpy as np # this is for speed, actually executes in C 
import pandas as pd  # to handle tabular data well
import requests
import xlsxwriter
import math
import time


#api call to client

finnhub_client = finnhub.Client(api_key="ciafar1r01qn522c0hc0ciafar1r01qn522c0hcg")


#Importing th elist of stocks
#Change for your path
stocks = pd.read_csv('/Users/harrygraneygreen/Desktop/tradingBot/tradingBotApp/Project 1/sp_500_stocks.csv')
#print(stocks)

symbol = 'AAPL'

#we need market captilization for each stcok
#also price of each stock
quote = finnhub_client.quote('AAPL')
price = quote.get('c')
#c is for current stock price


#Build pandas data frame : ticker, price, # of shares to buy
my_columns = [ 'Ticker', 'Stock Price', 'Number of Shares to Buy']

#final_dataframe = pd.DataFrame(columns = my_columns)

#adding one row to our Data Frame

#final_dataframe.loc[len(final_dataframe.index)] = [symbol,price,'N/A']

#now loop through every ticker in stocks


final_dataframe = pd.DataFrame(columns = my_columns)

for stock in stocks['Ticker']:
    time.sleep(1)
    #symbol = stock
    price = quote = finnhub_client.quote(stock)
    price = quote.get('c')
    final_dataframe.loc[len(final_dataframe.index)] = [stock,price,'N/A']


print(final_dataframe)
    























