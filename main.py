import imp
from pandas_datareader import data, wb
import pandas as pd
import numpy as np
import datetime
import seaborn as sns
from matplotlib import pyplot as plt

import cufflinks as cf
cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)

###########Finance Project##################
#1. Get the data for five companies, each of their stock price will be stored in a dataframe
#   We will have data from 1st Jan 2010 to 1st Jan 2020 :
#       * Google
#       * Facebook
#       * Netflix
#       * Microsoft
#       * Amazon
#       * Alibaba
#

# Read data from data source
start= datetime.datetime(2010,1,1)
end=datetime.datetime(2020,1,1)
GOOG=data.DataReader('GOOG','yahoo',start,end)
FB=data.DataReader('FB2A.BE','yahoo',start,end)
NFLX=data.DataReader('NFLX','yahoo',start,end)
AMZN=data.DataReader('AMZN','yahoo',start,end)
MSFT=data.DataReader('MSFT','yahoo',start,end)
BABA=data.DataReader('BABA','yahoo',start,end)

# Create Tickers
tickers=['GOOG','FB','NFLX','AMZN','MSFT','BABA']
tech_stocks = pd.concat([GOOG,FB,NFLX,AMZN,MSFT,BABA],axis=1,keys=tickers)
# tech_stocks.head()
tech_stocks.columns.names = ['Bak Ticker','Stock Info']


####### What is the max close price of each stock?########
# for tick in tickers:
#     tech_stocks[tick]['Close'].max()
tech_stocks.xs(key='Close',axis=1,level='Stock Info')


####### What is the return of each stock?########
returns = pd.DataFrame()
for tick in tickers:
    returns[tick+' Return'] = tech_stocks[tick]['Close'].pct_change()
sns.pairplot(returns)

##### Identify the best and worst day return######
# min return for a stock
returns.idxmin()
# max return for a stock
returns.idxmax()
#standard deviation for the return
returns.std()

#standard deviation for a period of time
returns.loc['2020-01-01':'2020-12-31'].std()

#create a distplot using seaborn of the 2020 returns for Google
sns.displot(returns.loc['2020-01-01':'2020-12-31']['GOOG Return'],color='green',bins=50)
sns.displot(returns.loc['2019-01-01':'2019-12-31']['NFLX Return'],color='purple',bins=50)


######plot close price for all the stocks ########
for tick in tickers:
    tech_stocks[tick]['Close'].plot(label=tick,figsize=(12,4))
plt.legend()
#fancy plots
tech_stocks.xs(key='Close',axis=1,level='Stock Info').iplot()


#####Moving Averages######
GOOG['Close'].loc['2019-01-01':'2009-01-01'].rolling(window=30).mean().plot(label='30 day moving average')
GOOG['Close'].loc['2019-01-01':'2009-01-01'].plot(label='GOOG Close')
plt.legend()


####Heatmap of the correlation between the stock close prices#####
sns.heatmap(tech_stocks.xs(key='Close',axis=1,level='Stock Info').corr(),annot=True)

close_corr= tech_stocks.xs(key='Close',axis=1,level='Stock Info').corr()
close_corr.iplot(kind='heatmap')

#candlestick plot
GOOG15=GOOG[['Open','High','Low','Close']].loc['2019-01-01':'2020-12-01']
GOOG15.iplot(kind='candle')

#simple Moving Averages
FB['Close'].loc['2019-01-01':'2020-12-31'].ta_plot(study='sma',periods=[12,21,55])

#Bollinnger Band Plot for GOOG
GOOG['Close'].loc['2019-01-01':'2020-12-01'].ta_plot(study='boll')