#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import os
from sklearn.preprocessing import MinMaxScaler
import AlexandreScraper
import ta
from PIL import Image


# In[2]:


def fetch_csv(directory='/home/',ticker='AMZN'):
    try:
        data = pd.read_csv('data-'+ticker+'.csv',sep='\t') 
    except Exception:
        print('Reading csv for ticker %s failed' %ticker)
        try:
            AlexandreScraper.somethingScraper(directory=directory, ticker=ticker)
        except Exception:
            print('Scrapping failed for ticker %s ' %ticker)
            data = pd.dataframe()
        else:
            data = pd.read_csv('data-'+ticker+'.csv',sep='\t')
    else:
        print('Read csv for ticker %s successful' %ticker)
    
    return data

def scale_0_1(df):
    df = df.copy()
    scaler = MinMaxScaler()
    df[df.select_dtypes(exclude='object').columns]=scaler.fit_transform(df[df.select_dtypes(exclude='object').columns])
    return df


# In[4]:


def set_up_down(df):
    df = df.copy()
    df['Up'] = df['Close'] > df['Open']
    df['NextDayUp'] = df.Up.shift(periods=-1)
    return df

def preprocess_dataset(df,indicators=['trend_sma_fast','trend_ema_fast','trend_macd','momentum_roc','volatility_bbh','volatility_bbl','volatility_bbp','momentum_stoch','momentum_stoch_signal']):
    data = df.copy()
    tmp = df.copy()
    
    data = set_up_down(data)
    #tmp = ta.add_all_ta_features(tmp, open="Open", high="High", low="Low", close="Close", volume="Volume",fillna=True)
    
    data = ta.add_all_ta_features(data, open="Open", high="High", low="Low", close="Close", volume="Volume",fillna=True)
    
    #data=data[['Date','Close','NextDayUp']]
    #data[indicators] = tmp[indicators]
  
    data = data.drop(df.head(30).index)
    
    return  data


# In[6]:


def plot_window_multi(df,path,indicators,dpi=64):
    df.drop('NextDayUp',axis=1,inplace=True)
    fig, ax = plt.subplots(figsize=(1, 1),dpi=dpi, facecolor='w', edgecolor='k')
    plt.axis('off')
    ax.plot(df,linewidth = 1)
    fig.savefig(fname=path,pad_inches=0,quality=100,format='png')#0
    plt.close(fig)
    img = Image.open(path)
    img = img.convert('RGB')
    img.save(path)


# In[7]:


def make_directory(paths=['dataset/Up','dataset/Down']):
    current_path = os.getcwd()
    for path in paths:
        try:
            dir_path=current_path +'/'+ path
            os.makedirs(dir_path)
        except OSError:
            print ("Creation of the directory %s failed" % dir_path)
        else:
            print ("Successfully created the directory : %s" % dir_path)


# In[8]:


def make_dataset(directory='dataset_scaled_2/train',tickers=['AMZN']):
    #tickersi =['AAPL','AMZN','FB','MSFT','FB','GOOG','GE','NIO','F','BAC','M','PFE']
    #tickersi =['GE','NIO','F','BAC','M','PFE']
    #tickersi =['AAPL','AMZN','FB','MSFT','FB','GOOG']
    make_directory(paths=['dataset_scaled_2/train/Up','dataset_scaled_2/train/Down','dataset_scaled_2/val/Up','dataset_scaled_2/val/Down'])
    indicators=['trend_sma_fast','trend_ema_fast','trend_macd','momentum_roc','volatility_bbh','volatility_bbl','volatility_bbp','momentum_stoch','momentum_stoch_signal']
    
    for ticker in tickers:
        data = fetch_csv(directory='/home/',ticker=ticker)
        data = preprocess_dataset(data,indicators=indicators)
        for row in data.itertuples():
                index = row.Index
                if(index >= 30):
                    tmp=data.loc[index-30:index,:].copy()
                    tmp=scale_0_1(tmp)
                    if row.NextDayUp == True:
                        path = os.path.abspath(directory + '/Up/' + row.Date + ticker +'.png')
                    else:
                        path = os.path.abspath(directory + '/Down/'+ row.Date + ticker+'.png')
                    tmp.set_index('Date',inplace=True)
                    #try:
                    tmp.index = pd.to_datetime(tmp.index)
                    plot_window_multi(tmp,path,indicators,dpi=64)
                    """
                    except Exception:
                        print('dateTime conversion failed for ticker ' + ticker +' index : %d ' %row.Index)
                        print(tmp.head(5))
                    """
                    

        print("Done " + directory +" "+ ticker)

if __name__ == '__main__':
    make_dataset()


# In[ ]:




