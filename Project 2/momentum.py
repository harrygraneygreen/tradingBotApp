#Momentum is defined as giving emphasis to stocks that have increased in price the most
#Will suggest a protfolio of stocks with the gratest momentums

import finnhub
import numpy as np
import pandas as pd
import math
from scipy import stats
import xlsxwriter
import time
from statistics import mean

finnhub_client = finnhub.Client(api_key="ciafar1r01qn522c0hc0ciafar1r01qn522c0hcg")
#Importing th elist of stocks
#Change for your path
stocks = pd.read_csv('/Users/harrygraneygreen/Desktop/tradingBot/tradingBotApp/Project 1/sp_500_stocks.csv')
#print(stocks)
fins = finnhub_client.company_basic_financials('AAPL', 'all')
#fins['metric']['marketcapitilization']

#BASIC LOGIC FOR 1YR Change
# 1 year ago UNIX timestamp = 1657143847  == Wed Jul 06 2022 17:44:07 

year_ago = 	1657231682
six_months_ago = 1673132826
three_months_ago = 1680905251
one_month_ago = 1686175651

#today = 1688665521
##UPDATE IF NEEDED @ https://www.unixtimestamp.com/

#1 year ago prices
# last_year_candle = finnhub_client.stock_candles('AAPL', 'D', year_ago, year_ago)
# last_year_price = last_year_candle.get('c')[0]
# quote = finnhub_client.quote('AAPL')
# current_price = quote.get('c')
# annual_change_percent = (current_price/last_year_price) - 1
#NOW get top 50 of the 1 year change percent

# my_columns = [ 'Ticker', 'Price', 'One-Year Price Return', 'Number of Shares to Buy']
# final_dataframe = pd.DataFrame(columns = my_columns)

#### change number of things in SP500 or sleep function to ensure not over 30calls/second
### time = 1.9 works

# for stock in stocks['Ticker'][:29]:
#     #time.sleep(1.9)
#     quote = finnhub_client.quote(stock)
#     current_price = quote.get('c')
#     if (current_price != 0):
#         last_year_candle = finnhub_client.stock_candles(f'{stock}', 'D', year_ago, year_ago)
#         last_year_price = last_year_candle.get('c')[0]
#         annual_change_percent = (current_price / last_year_price) - 1
#         final_dataframe.loc[len(final_dataframe.index)] = [stock,current_price, annual_change_percent, 'N/A']


###Now remove the low momentum stocks to get top 50 highest momentum stocks in SP500
#final_dataframe.sort_values('One-Year Price Return', ascending=False, inplace=True)
###final_dataframe = final_dataframe[:50]
#final_dataframe.reset_index(inplace=True)

# portfolio_input()
# position_size = float(portfolio_size)/len(final_dataframe.index)
# for i in range(0, len(final_dataframe.index)):
#     final_dataframe.loc[i, 'Number of Shares to Buy'] = math.floor(position_size/final_dataframe.loc[i, 'Price'])
# print(final_dataframe)


def portfolio_input():
    global portfolio_size
    portfolio_size = input('Enter the size of your portfolio')
    try:
        float(portfolio_size)
    except ValueError:
        print("That is not a number! \n Please try again")
        portfolio_size = input('Enter the size of your portfolio')


################### MORE REALISTIC STRATEGY ##########################


##Differentiate between high quality and low quality momentum stocks
### 1 year, 6 month, 3 month, and 1 month returns

hqm_columns = [
    'Ticker', 
    'Price',
    'Number of Shares to Buy',
    'One-Year Price Return',
    'One-Year Return Percentile',
    'Six-Month Price Return',
    'Six-Month Return Percentile',
    'Three-Month Price Return',
    'Three-Month Return Percentile',
    'One-Month Price Return',
    'One-Month Return Percentile',
    'HQM Score'
]

hqm_dataframe = pd.DataFrame(columns = hqm_columns)
#for stock in stocks['Ticker'][:50]:
#sleep for 2 should work
for stock in stocks['Ticker'][:50]:
    time.sleep(5)
    quote = finnhub_client.quote(stock)
    current_price = quote.get('c')
    if (current_price != 0):
        last_year_candle = finnhub_client.stock_candles(f'{stock}', 'D', year_ago, year_ago)
        last_year_price = last_year_candle.get('c')[0]
        annual_change_percent = (current_price / last_year_price) - 1

        six_month_candle = finnhub_client.stock_candles(f'{stock}', 'W', six_months_ago, six_months_ago + 604800)
        six_month_price = six_month_candle.get('c')[0]
        six_month_change_percent = (current_price / six_month_price) - 1

        three_month_candle = finnhub_client.stock_candles(f'{stock}', 'W', three_months_ago, three_months_ago + 604800)
        three_month_price = three_month_candle.get('c')[0]
        three_month_change_percent = (current_price / three_month_price) - 1

        one_month_candle = finnhub_client.stock_candles(f'{stock}', 'W', one_month_ago, one_month_ago + 604800)
        one_month_price = one_month_candle.get('c')[0]
        one_month_change_percent = (current_price / one_month_price) - 1


        hqm_dataframe.loc[len(hqm_dataframe.index)] = [
            stock,
            current_price,
            'N/A',
            annual_change_percent,
            'N/A',
            six_month_change_percent,
            'N/A',
            three_month_change_percent,
            'N/A',
            one_month_change_percent,
            'N/A',
            'N/A'
        ]

#print(hqm_dataframe)

###calculating percentiles

time_periods = [
    'One-Year',
    'Six-Month',
    'Three-Month',
    'One-Month'
]

for row in hqm_dataframe.index:
    for time_period in time_periods:
        perc_col = f'{time_period} Return Percentile'
        ret_col = f'{time_period} Price Return'
        hqm_dataframe.loc[row, perc_col] = stats.percentileofscore(hqm_dataframe[ret_col], hqm_dataframe.loc[row, ret_col]) / 100


for row in hqm_dataframe.index:
    momentum_percentile = []
    for time_period in time_periods:
        momentum_percentile.append(hqm_dataframe.loc[row, f'{time_period} Return Percentile'])
    hqm_dataframe.loc[row, 'HQM Score'] = mean(momentum_percentile)  


hqm_dataframe.sort_values('HQM Score', ascending=False, inplace=True)

###Takes only top number of stocks
#num_stocks = input('How many stocks so you want to invest in?')
#hqm_dataframe = hqm_dataframe[:num_stocks]
hqm_dataframe = hqm_dataframe[:10]

hqm_dataframe.reset_index(inplace=True, drop=True)
##IF YOU WANT TO INPUT YOUR PORTFOLIO SIZE
#portfolio_input()
portfolio_size = 10000 

position_size = float(portfolio_size)/ len(hqm_dataframe.index)
for row in hqm_dataframe.index:
    hqm_dataframe.loc[row, 'Number of Shares to Buy'] = math.floor(position_size / hqm_dataframe.loc[row, 'Price'])

print(hqm_dataframe) 


#SAVE this output into EXCEL
# UNCOMMENT IF WANT TO EXPORT TO EXCEL!

##########################################################################

writer = pd.ExcelWriter('momentum strategy.xlsx', engine='xlsxwriter')
hqm_dataframe.to_excel(writer, 'momentum strategy', index= False)
#Formatting
bg_color = '#0a0a23'
font_color = '#ffffff'
string_format = writer.book.add_format(
    {
        'font_color': font_color,
        'bg_color': bg_color,
        'border': 1
    }
)
dollar_format = writer.book.add_format(
    {
        'num_format': '$0.00',
        'font_color': font_color,
        'bg_color': bg_color,
        'border': 1
    }
)
integer_format = writer.book.add_format(
    {
        'num_format': '0',
        'font_color': font_color,
        'bg_color': bg_color,
        'border': 1
    }
)

percent_format = writer.book.add_format(
    {
        'num_format': '0.0%',
        'font_color': font_color,
        'bg_color': bg_color,
        'border': 1
    }
)

column_formats = {
    'A': ['Ticker', string_format],
    'B': ['Stock Price', dollar_format],
    'C': ['Number of Shares to Buy', integer_format],
    'D': ['One-Year Price Return', percent_format],
    'E': ['One-Year Return Percentile', percent_format],
    'F': ['Six-Month Price Return', percent_format],
    'G': ['Six-Month Return Percentile', percent_format],
    'H': ['Three-Month Price Return', percent_format],
    'I': ['Three-Month Return Percentile', percent_format],
    'J': ['One-Month Price Return', percent_format],
    'K': ['One-Month Return Percentile', percent_format],
    'L': ['HQM Score',percent_format]
}

for column in column_formats.keys():
    writer.sheets['momentum strategy'].set_column(f'{column}:{column}', 22, column_formats[column][1])
    writer.sheets['momentum strategy'].write(f'{column}1', column_formats[column][0], string_format)
    
writer.close()