def get_pric_etf(count,etf_id,treeview):    
    yfin.pdr_override()
    start_date = date.today()-timedelta(days=365)
    end_date = date.today()
    data_m = pdr.get_data_yahoo(etf_id, start=start_date,end=end_date)
    #半年最高価額
    high_year_h_price=data_m["High"].max()
    #半年最低価額
    low_year_h_price=data_m["Low"].min()
    # 現在価額を取得
    stock_info = yfin.Ticker(etf_id)
    kabu_mame = stock_info.info["longName"]
    now_price = stock_info.history(period="1d")["Close"].values[0]
    treeview.insert( parent='',index="end",iid=count 
                    ,values=(etf_id,kabu_mame,round(now_price,1)
                             ,round(high_year_h_price,1),round(low_year_h_price,1)))
    #銘柄関連ニュース
    #stock_new = yfin.Ticker(etf_id)  
    return data_m