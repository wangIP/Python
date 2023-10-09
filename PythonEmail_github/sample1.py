import sample as m
from email.mime.text import MIMEText


gmail_addr = "自分のメールアドレス"
gmail_pw = "発行されたPW"
to_addr = ['宛先メールアドレス']#ccも追加可能
mine_txt = MIMEText('本文内容','plain','utf-8')
mine_txt['Subject'] = 'タイトル'
mine_txt['From'] = 'testcenter'
mine_txt['To'] = 'johns10166'
mine_txt['Cc'] = 'cc'
mine_txt = mine_txt.as_string()
m.send_gmail(gmail_addr,gmail_pw,to_addr,mine_txt)