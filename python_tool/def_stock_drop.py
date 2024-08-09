import mplfinance as mf
import pandas as pd
import numpy as np
import yfinance as yfin
from datetime import date, timedelta,datetime
#debug的時候要comment掉
#matplotlib.use("TkAgg")
def stock_drop(kabu_id,buy_date_s):   
    """用於繪製股票k線圖函數"""
    yfin.pdr_override()
    # 獲取股票的歷史數據
    start_date = date.today()-timedelta(days=730)
    end_date = date.today()
    #start = '2021-08-01' #移動平均の計算をするために描画する期間よりも前からデータを取得しておく
    #end = '2023-09-26'
    data_m = yfin.download(tickers=kabu_id, start=start_date, end=end_date, interval='1d')
    #last_date = date.today()-timedelta(days=360)
    # 計算20日移動平均線
    #sma20 = data_m["Close"].rolling(window=20).mean()#過去 20 個交易日的收盤價計算的平均值
    # 計算5日移動平均線
    data_m['5ma'] = data_m['Adj Close'].rolling(window=5).mean()
    # 計算20日移動平均線
    data_m['20ma'] = data_m['Adj Close'].rolling(window=20).mean()
    # 計算60日移動平均線
    data_m['60ma'] = data_m['Adj Close'].rolling(window=60).mean()
    data_m=data_m[data_m.index > datetime(2023,7,27)]
    
    #5日均線和20日均線做黃金交叉,死亡交叉
    #創建兩個新的Series來存儲標記
    golden_cross = pd.Series(np.where((data_m['5ma'] > data_m['20ma']) & (data_m['5ma'].shift(1) < data_m['20ma'].shift(1)), data_m['Adj Close'], np.nan), index=data_m.index)
    death_cross = pd.Series(np.where((data_m['5ma'] < data_m['20ma']) & (data_m['5ma'].shift(1) > data_m['20ma'].shift(1)), data_m['Adj Close'], np.nan), index=data_m.index)
    
    # 創建一個addplot對象來添加標記
    ap = [mf.make_addplot(golden_cross, scatter=True, markersize=100, marker='*',color='black'),
      mf.make_addplot(death_cross, scatter=True, markersize=100, marker='v',color='red')]
   

    addplot_20ma = mf.make_addplot(data_m['5ma'], color='blue', label='5MA')
    addplot_50ma = mf.make_addplot(data_m['20ma'], color='orange', label='20MA')
    addplot_60ma = mf.make_addplot(data_m['60ma'], color='green', label='60MA')

    if len(buy_date_s) != 0:
        buy_series = pd.Series(index=data_m.index)      
        for buy_date in buy_date_s:
            buy_price = data_m.loc[buy_date]['Close']
            #print(buy_price)
            buy_series[buy_date] = buy_price
        apdict = mf.make_addplot(buy_series,scatter=True,markersize=100,marker='^')
        addplot =[addplot_20ma, addplot_50ma,addplot_60ma,apdict] + ap
        mf.plot(data_m,title=kabu_id,style='yahoo', type='candle', addplot=addplot, figratio=(12,4),volume=True )
    else:
        addplot =[addplot_20ma, addplot_50ma,addplot_60ma] + ap
        mf.plot(data_m,title=kabu_id,style='yahoo', type='candle', addplot=addplot, figratio=(12,4),volume=True )