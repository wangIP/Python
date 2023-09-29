import smtplib

def send_gmail(email_id,email_pw,to_address,msg):
    smtp_gmail = smtplib.SMTP('smtp.gmail.com',587)
    print(smtp_gmail.ehlo())
    print(smtp_gmail.starttls())
    print(smtp_gmail.login(email_id,email_pw))
    status = smtp_gmail.sendmail(email_id,to_address,msg)
    if not status:
        print('send ok')
    else:
        print('send err',status)
    smtp_gmail.quit()
email_id = 'あなたのメールアドレス'
email_pw = '発行されたpw'
to_address = '宛先のメールアドレス'
send_gmail(email_id,email_pw,to_address,'Subject:Hello\nTesting')