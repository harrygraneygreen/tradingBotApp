###selecting cheapest stocks relative to common business metrics

import numpy as np
import pandas as pd 
import xlsxwriter
from scipy import stats
import math
import finnhub
from statistics import mean
import time


finnhub_client = finnhub.Client(api_key="ciafar1r01qn522c0hc0ciafar1r01qn522c0hcg")
#Importing th elist of stocks
#Change for your path
stocks = pd.read_csv('/Users/harrygraneygreen/Desktop/tradingBot/tradingBotApp/Project 1/sp_500_stocks.csv')

## price to earnings ratio
#test = finnhub_client.company_basic_financials('AAPL', 'all')
#print(test['metric']['peAnnual'])

# my_columns = ['Ticker', 'Price', 'Price-to-Earnings Ratio', 'Number of Shares to Buy']

# quant_dataframe = pd.DataFrame(columns = my_columns)

# for stock in stocks:

#     quote = finnhub_client.quote(stock)
#     current_price = quote.get('c')

#     if (current_price != 0):
#         curr_financials = finnhub_client.company_basic_financials(stock, 'all')
#         curr_peAnnual = curr_financials['metric']['peAnnual']

#         quant_dataframe.loc[len(quant_dataframe.index)] = [stock, current_price, curr_peAnnual, 'N/A']


##Removing glamour stocks (stocks that are the opposite of value stocks)

# quant_dataframe.sort_values('Price-to-Earnings Ratio', ascending=False, inplace=True)
# quant_dataframe = quant_dataframe[quant_dataframe['Price-to-Earnings Ratio'] > 0]
# quant_dataframe = quant_dataframe[:50]
# quant_dataframe.reset_index()

# portfolio_input()

# position_size =float(portfolio_size)/len(quant_dataframe.index)

# for row in quant_dataframe.index:
#     quant_dataframe.loc[row, 'Number of Shares to Buy'] = math.floor(position_size / quant_dataframe.loc[row, 'Price'])



#More realistic value strategy#
#PE ratio, Price to book, price-to-sales, Enterpirse value to (EV/EBITDA), EV/gross profit (EV/GP)

#tags = pbAnnual, peAnnual, psAnnual, ( enterpriseValue, grossMarginAnnual),  ebitdPerShareAnnual


my_columns = [
    'Ticker',
    'Price',
    'Price-to-Earnings Ratio',
    'PE Percentile',
    'Price-to-Book',
    'PB Percentile',
    'Price-to-Sales',
    'PS Percentile',
    'EV/EBITDA',
    'EV/EBITDA Percentile',
    'EV/GP',
    'EV/GP Percentile',
    'RV Score',
    'Number of Shares to Buy'
    ]


quant_dataframe = pd.DataFrame(columns = my_columns)


for stock in stocks['Ticker'][:50]:
    time.sleep(.04)
    quote = finnhub_client.quote(stock)
    current_price = quote.get('c')
    
    if (current_price != 0):

        curr_financials = finnhub_client.company_basic_financials(stock, 'all')
        
        #peAnnual
        pe = curr_financials['metric']['peAnnual']
        pb = curr_financials['metric']['pbAnnual']
        ps = curr_financials['metric']['psAnnual']
        #Enterprise Value
        ev = curr_financials['metric']['enterpriseValue']
        #GP
        try:
            gp = curr_financials['metric']['grossMarginAnnual']
            ev_gp = ev/gp
        except:
            ev_gp = 0
        #editd
        ebitd = curr_financials['metric']['ebitdPerShareAnnual']

        quant_dataframe.loc[len(quant_dataframe.index)] = [stock, current_price, pe/100,'N/A', pb/100,'N/A', ps/100,'N/A', (ev/ebitd) /100 , 'N/A', ev_gp / 100, 'N/A', 'N/A', 'N/A']


metrics = {
    'Price-to-Earnings Ratio':'PE Percentile',
    'Price-to-Book':'PB Percentile',
    'Price-to-Sales':'PS Percentile',
    'EV/EBITDA':'EV/EBITDA Percentile',
    'EV/GP':'EV/GP Percentile'
}

for metric in metrics.keys():
    for row in quant_dataframe.index:
        quant_dataframe.loc[row, metrics[metric]] = stats.percentileofscore(quant_dataframe[metric], quant_dataframe.loc[row, metric]) /100


for row in quant_dataframe.index:
    percentiles = []
    for metric in metrics.keys():
        percentiles.append(quant_dataframe.loc[row, metrics[metric]])
    quant_dataframe.loc[row, 'RV Score'] = mean(percentiles)



quant_dataframe.sort_values('RV Score', ascending=False, inplace=True)

#quant_dataframe = quant_dataframe[:50]
quant_dataframe.reset_index(inplace=True, drop=True)


######Size of [ortfolio and number of shares to buy]

#portfolio_input()
portfolio_size = 10000

position_size = float(portfolio_size)/ len(quant_dataframe.index)
for row in quant_dataframe.index:
    quant_dataframe.loc[row, 'Number of Shares to Buy'] = math.floor(position_size / quant_dataframe.loc[row, 'Price'])


print(quant_dataframe)
## Getting percentiles



##Removing glamour stocks (stocks that are the opposite of value stocks)

# quant_dataframe.sort_values('Price-to-Earnings Ratio', ascending=False, inplace=True)
# quant_dataframe = quant_dataframe[quant_dataframe['Price-to-Earnings Ratio'] > 0]
# # quant_dataframe = quant_dataframe[:50]
#  quant_dataframe.reset_index()



# portfolio_input()

# position_size = float(portfolio_size)/len(quant_dataframe.index)

# for row in quant_dataframe.index:
#     quant_dataframe.loc[row, 'Number of Shares to Buy'] = math.floor(position_size / quant_dataframe.loc[row, 'Price'])
        
def portfolio_input():
    global portfolio_size
    portfolio_size = input('Enter the size of your portfolio')
    try:
        float(portfolio_size)
    except ValueError:
        print("That is not a number! \n Please try again")
        portfolio_size = input('Enter the size of your portfolio')








#SAVE this output into EXCEL
# UNCOMMENT IF WANT TO EXPORT TO EXCEL!

##########################################################################

writer = pd.ExcelWriter('value strategy.xlsx', engine='xlsxwriter')
quant_dataframe.to_excel(writer, 'value strategy', index= False)
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
    'B': ['Price', dollar_format],
    'C': ['Price-to-Earnings Ratio', percent_format],
    'D': ['PE Percentile', percent_format],
    'E': ['Price-to-Book', percent_format],
    'F': ['PB Percentile', percent_format],
    'G': ['Price-to-Sales', percent_format],
    'H': ['PS Percentile', percent_format],
    'I': ['EV/EBITDA', percent_format],
    'J': ['EV/EBITDA Percentile', percent_format],
    'K': ['EV/GP', percent_format],
    'L': ['EV/GP Percentile',percent_format],
    'M': ['RV Score', percent_format],
    'N': ['Number of Shares to Buy', integer_format],
}

    


for column in column_formats.keys():
    writer.sheets['value strategy'].set_column(f'{column}:{column}', 22, column_formats[column][1])
    writer.sheets['value strategy'].write(f'{column}1', column_formats[column][0], string_format)
    
writer.close()

