# This is an equal weight S&P 500 Index Fund Project

#imports

import finnhub
import numpy as np # this is for speed, actually executes in C 
import pandas as pd  # to handle tabular data well
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
#note: limit number of API calls to 30 per second. Will receive 429 code 
#for 500 should take around 20 seconds if at 30 per sec

for stock in stocks['Ticker'][:29]:
    #time.sleep(.05)

    quote = finnhub_client.quote(stock)
    price = quote.get('c')
    if (price != 0):
        final_dataframe.loc[len(final_dataframe.index)] = [stock,price,'N/A']


#print(final_dataframe)


#CALCULATING NUMBER OF SHARES TO BUY

portfolio_size = input('Enter the value of your portfolio')
try:
    val = float(portfolio_size)
except ValueError:
    print("That is not a number \n")
    portfolio_size = input('Enter the value of your portfolio')
    val = float(portfolio_size)


position_size = val/len(final_dataframe.index)

for i in range(0, len(final_dataframe.index)):
    #since the csv is outdated we need to check the stock price isn't 0
    #if (final_dataframe.loc[i,'Stock Price'] != 0):
    final_dataframe.loc[i, 'Number of Shares to Buy'] = math.floor(position_size/final_dataframe.loc[i,'Stock Price'])

print(final_dataframe)


#SAVE this output into EXCEL
# UNCOMMENT IF WANT TO EXPORT TO EXCEL!

##########################################################################

# writer = pd.ExcelWriter('recommended trades.xlsx', engine='xlsxwriter')
# final_dataframe.to_excel(writer, 'recommended trades', index= False)
# #Formatting
# bg_color = '#0a0a23'
# font_color = '#ffffff'
# string_format = writer.book.add_format(
#     {
#         'font_color': font_color,
#         'bg_color': bg_color,
#         'border': 1
#     }
# )
# dollar_format = writer.book.add_format(
#     {
#         'num_format': '$0.00',
#         'font_color': font_color,
#         'bg_color': bg_color,
#         'border': 1
#     }
# )
# integer_format = writer.book.add_format(
#     {
#         'num_format': '0',
#         'font_color': font_color,
#         'bg_color': bg_color,
#         'border': 1
#     }
# )
# column_formats = {
#     'A': ['Ticker', string_format],
#     'B': ['Stock Price', dollar_format],
#     'C':['Number of Shares to Buy', integer_format]
# }
# for column in column_formats.keys():
#     writer.sheets['recommended trades'].set_column(f'{column}:{column}', 18, column_formats[column][1])
#     writer.sheets['recommended trades'].write(f'{column}1', column_formats[column][0], string_format)
    
# writer.close()





