import sample as m
from email.mime.image import MIMEImage
import cv2

def get_mine_img(subject,fr,to,img):
    img_encode = cv2.imencode('.jpg',img)[1] #取った写真をjpegに変換します。「1」は返すオブジェクト「0」は成功するかどうか判定
    img_bytes = img_encode.tobytes()#転送するため、imgに変換されたオブジェクトがbytesに変換します。
    mine_img = MIMEImage(img_bytes)#MIMEImageインスタンスを作成します。
    mine_img['Content-type'] = 'application/octet-stream'#MIMEの型を決めます
    mine_img['Content-Disposition'] = 'attachment; filename="pic.jpg"'
    mine_img['Subject'] = subject
    mine_img['From'] = fr
    mine_img['To'] = to
    return mine_img.as_string()#オブジェクトを文字列に変換します。

gmail_addr = 'あなたのメールアドレス'
gmail_pwd = '発行されたpw'
to_addrs = ['宛先のメールアドレス']

cap = cv2.VideoCapture(0)
while cap.isOpened():
    success,img = cap.read()
    if success:
        cv2.imshow('frame',img)
    k = cv2.waitKey(1)
    if k == ord('s'):
        msg = get_mine_img('小偷闖空門','防盜監視器','自己',img)
        m.send_gmail(gmail_addr,gmail_pwd,to_addrs,msg)
        break
    elif k == ord('q'):
        cv2.destroyAllWindows()
        cap.release()
        break