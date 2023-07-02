# This is an equal weight S&P 500 Index Fund Project

#imports

import finnhub
import numpy as np # this is for speed, actually executes in C 
import pandas as pd  # to handle tabular data well
import requests
import xlsxwriter
import math


#api call to client

finnhub_client = finnhub.Client(api_key="ciafar1r01qn522c0hc0ciafar1r01qn522c0hcg")


#Importing th elist of stocks

stocks = pd.read_csv('sp_500_stocks.csv')

print(stocks)












