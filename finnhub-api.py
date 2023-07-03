
#imports

import finnhub
import numpy as np # this is for speed, actually executes in C 
import pandas as pd  # to handle tabular data well
import requests
import xlsxwriter
import math


#api call to client

finnhub_client = finnhub.Client(api_key="ciafar1r01qn522c0hc0ciafar1r01qn522c0hcg")

#Test for Alle(This is where loop keeps breaking)
recommendDict = finnhub_client.recommendation_trends("ALLE")
recommend = recommendDict[0]["strongBuy"] - recommendDict[0]["strongSell"]
print(recommend)


#Importing the list of stocks

initial = pd.read_csv('sp_500_stocks.csv')

tickerList = []
recommendationList = []
priceList = []
for index, row in initial.iterrows():
        tickerList.append(row["Ticker"])
        recommendDict = finnhub_client.recommendation_trends(row["Ticker"])
        recommend = recommendDict[0]["strongBuy"] - recommendDict[0]["strongSell"]
        recommendationList.append(recommend)
        priceDict = finnhub_client.quote(row["Ticker"])
        price = priceDict["c"]
        priceList.append(price)

dataDict = {
    "Symbol" : tickerList,
    "Net Strong Buy" : recommendationList,
    "Current Price": priceList
}

stocks_data=pd.DataFrame(data = dataDict)




print(stocks_data)