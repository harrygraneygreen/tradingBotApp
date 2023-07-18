###selecting cheapest stocks relative to common business metrics

import numpy as np
import pandas as pd 
import xlsxwriter
from scipy import stats
import math
import finnhub
from datetime import date

today = date.today()
finnhub_client = finnhub.Client(api_key="ciafar1r01qn522c0hc0ciafar1r01qn522c0hcg")

stocks = pd.read_csv('/Users/harrygraneygreen/Desktop/tradingBot/tradingBotApp/Project 1/sp_500_stocks.csv')


test = finnhub_client.company_basic_financials('AEE', 'all')

print(test['metric']['grossMarginAnnual'])

# keys = test['metric'].keys()
# for key in keys:
#     print(key)

#ebitdPerShareAnnual
#LOL this is to get gross profit in 2022, not sure if worth it 

# reported = finnhub_client.financials_reported(symbol='ABBV', freq='annual')
# keys = reported['data']
# for key in keys:
#     if key['year'] == 2022:
#         for guy in key['report']['ic']:
#             print(guy)
            #if guy['concept'] == 'us-gaap_GrossProfit':
             #   print(guy['value'])


    #if key['label'] == 'Gross Profit':
        #print(key)

    #tags = pbAnnual, peAnnual, psAnnual, enterpriseValue, grossMarginAnnual, ebitdaCagr5Y
    #beta is volatility

#print(test['metric']['beta'])





##################ALT CODE ################


# reported = finnhub_client.financials_reported(symbol= stock, freq='annual')
#         keys = reported['data']
# for key in keys:
        #     if key['year'] == 2022:
        #         for guy in key['report']['ic']:
        #             if guy['concept'] == 'us-gaap_GrossProfit':
        #                 gp = guy['value']
        #                 print(gp)
        #                 quant_dataframe.loc[len(quant_dataframe.index)] = [stock, current_price, pe,'N/A', pb,'N/A', ps,'N/A', ev/gp,'N/A','N/A','N/A']
        #                 set = 1
        # if set == 0:  
        #     quant_dataframe.loc[len(quant_dataframe.index)] = [stock, current_price, pe,'N/A', pb,'N/A', ps,'N/A', 'N/A','N/A','N/A','N/A']
