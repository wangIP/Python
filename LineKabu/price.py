import twstock

stock = twstock.Stock('1301')
print('日付:',stock.date[-1])
print('最高価格:',stock.high[-1])
print('最低価格:',stock.low[-1])