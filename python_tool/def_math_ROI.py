def math_ROI(etf_id):
    """計算股票的每日回報率的函數"""    
    yfin.pdr_override()
    # 獲取股票的歷史數據
    start_date = date.today()-timedelta(days=730)
    end_date = date.today()
    #start = '2021-08-01' #移動平均の計算をするために描画する期間よりも前からデータを取得しておく
    #end = '2023-09-26'
    data = yfin.download(tickers=etf_id, start=start_date, end=end_date, interval='1d')
    close_px = data['Adj Close']
    '''
    計算股票的每日回報率。
    data / data.shift(1)是將每天的收盤價除以前一天的收盤價，從而計算出每天價格變化的比例（即回報率）。
    最後，- 1將回報率從百分比轉換為實際變化量（例如，0.01表示增加了1%）。
    '''
    rets = close_px / close_px.shift(1) - 1
    plt.figure(figsize=(12,4))
    plt.plot(rets)
    plt.title(etf_id)
    plt.show()