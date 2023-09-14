import time                # 匯入 time 模組, 會使用其 sleep() 來暫停時間

# import sys

# sys.path.append("module")
import module.stock_module as m   # 匯入自訂模組並改名為 m

slist = m.get_setting()   # 呼叫匯入模組中的函式取得股票設定資料
cnt = len(slist)          # 計算有幾支股票

log1 = []   # 記錄曾經傳送過的股票高或低於期望價的訊息, 以避免重複傳送
log2 = []   # 記錄曾經傳送過符合四大買賣點的訊息, 以避免重複傳送
for i in range(cnt):   #}
    log1.append('')    #} 為每支股票加入一個對應的元素
    log2.append('')    #}

check_cnt = 20    # 指定要檢查幾次 (20*3分鐘 = 60分鐘)
while True:
    for i in range(cnt):   # 走訪每一支股票
        id, low, high = slist[i]   #讀出股票的代號、期望買進價格、期望賣出
        name, price = m.get_price(id)   #回傳股票名稱與即時股價，帶入name,price讀取股票的名稱和即時價格
        print('檢查：',name, '即時股價：',price, '區間：',low,'~',high)
        if price <= low:      #←　即時價格等於或低於期望買進　可買進
            if log1[i] != '買進':  # 檢查前次傳送訊息, 以避免重複傳送
                m.send_ifttt(name, price, '可買進 (即時股價低於 '+str(low)+'期望買進)')
                log1[i]= '買進'    # 記錄傳送訊息, 以避免重複傳送
        elif price >= high:   #←即時價格高於期望賣出　可賣出
            if log1[i] != '賣出':  # 檢查前次傳送訊息, 以避免重複傳送
                m.send_ifttt(name, price, '可賣出 (即時股價高於 '+str(high)+')')
                log1[i]= '賣出'    # 記錄傳送訊息, 以避免重複傳送
        else:   #←在區間內
                m.send_ifttt(name, price, '不賣不買 (即時股價位於 '+str(low)+'~'+str(high)+')')
        #m.send_ifttt('-','-','-')  
        #act, why = m.get_best(id)  # 檢查四大買賣點
        # if why:   #←如果符合四大買賣點
        #     if log1[i] != why:    # 檢查前次傳送訊息, 以避免重複傳送
        #         m.send_ifttt(name, price, act + ' (' +why+ ')')
        #         log1[i] = why     # 記錄傳送訊息, 以避免重複傳送
        # if why :
        #     if log2[i] != why:
        #         m.send_ifttt(name,price,'四大買賣點為基準:'+act+'('+why+')')
        #         log2[i]=why
        # test = input("四大基準?")
        # if test == 'yes':
        #     for i in range(cnt):
        #         id, low, high = slist[i]
        #         name, price = m.get_price(id)
        #         act, why = m.get_best(id)  # 檢查四大買賣點
        #         if why:   #←如果符合四大買賣點
        #             if log2[i] != why:
        #                 m.send_ifttt(name,price,'四大買賣點為基準:'+act+'('+why+')')
        #                 log2[i]=why    
    print('--------------')
    check_cnt -= 1             # 將計數器減 1
    if check_cnt == 0: break   # 檢查計數器為 0 時即離開迴圈、結束程式
    time.sleep(180)            # 每 3 分鐘 (180 秒) 檢查一遍
