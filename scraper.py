#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 07:03:31 2019

@author: Nicolas
"""
import os
import re
import time
import requests
import numpy as np
import pandas as pd
from io import StringIO
from datetime import datetime

######################################
DIRECTORY = "/home/jupyter/"# TO CHANGE
######################################

class YahooFinanceHistory:
    timeout = 2
    crumb_link = 'https://finance.yahoo.com/quote/{0}/history?p={0}'
    crumble_regex = r'CrumbStore":{"crumb":"(.*?)"}'
    quote_link = 'https://query1.finance.yahoo.com/v7/finance/download/{quote}?period1={dfrom}&period2={dto}&interval=1d&events=history&crumb={crumb}'

    def __init__(self, ticker, startDate, endDate):
        self.ticker = ticker
        self.session = requests.Session()
        self.startDate = startDate
        self.endDate = endDate

    #Get the cookie and the crumb
    def get_crumb(self):
        response = self.session.get(self.crumb_link.format(self.ticker), timeout=self.timeout)
        response.raise_for_status()
        match = re.search(self.crumble_regex, response.text)
        if not match:
            raise ValueError('Could not get crumb from Yahoo Finance')
        else:
            self.crumb = match.group(1)

    def get_quote(self):
        if not hasattr(self, 'crumb') or len(self.session.cookies) == 0:
            self.get_crumb()
        self.startDate = int(self.startDate.timestamp())
        self.endDate = int(self.endDate.timestamp())
        url = self.quote_link.format(quote=self.ticker, dfrom=self.startDate, dto=self.endDate, crumb=self.crumb)
        response = self.session.get(url)
        response.raise_for_status()
        return pd.read_csv(StringIO(response.text), parse_dates=['Date'])

def getData(ticker):
    startDate = datetime(1980, 1, 1, 0, 0)
    endDate = datetime.utcnow()

    for i in range(0,10):
        try:
            startTime = time.time()
            data = YahooFinanceHistory(ticker, startDate, endDate).get_quote()
            endTime = time.time()
            print("{0} days scraped between {1} and {2} in {3}s, {4} missing value(s) will be deleted.".format(len(data),
                  data.iloc[0,0].strftime("%Y-%m-%d"), data.iloc[-1,0].strftime("%Y-%m-%d"),
                  round(endTime-startTime,2), data.iloc[:,-2].isna().sum()))
            data.set_index('Date', inplace = True)
            data.dropna(inplace = True)
            break
        except Exception:
            print("Could not retrieve data, trying again...")
            time.sleep(2)
    return data

def getDataFromFile(ticker):
    data = pd.read_csv("data-{0}.csv".format(ticker), sep='\t')
    data['Date'] =  pd.to_datetime(data['Date'], format='%Y-%m-%d')
    data = data.set_index('Date')
    return data

def somethingScraper(ticker,directory):
    try:
        DIRECTORY = directory
        getData(ticker).to_csv(f"{DIRECTORY}data-{ticker}.csv", sep='\t', index = True)
    except Exception:
        print("Could not retrieve {0} data".format(ticker))

if __name__ == '__main__':
    somethingScraper('AMZN')
