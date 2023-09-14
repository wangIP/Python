import requests
import cv2
import time
import re

base = 'エンドポイント'
recog_url = f'{base}/recognizeText?mode=Printed'
key = 'key'
headers = {'Ocp-Apim-Subscription-Key':key}
headers_stream = {'Ocp-Apim-Subscription-Key' : key,
                  'Content-Type':'application/octet-stream'}
def get_license(img):
    img_encode = cv2.imencode('.jpg',img)[1]
    
    img_bytes = img_encode.tobytes()
    r1 = requests.post(recog_url,
                       headers=headers_stream,
                       data=img_bytes)
    if r1.status_code != 202:
        print(r1.json)  
        return '請求失敗'
    result_url = r1.headers['Operation-Location']
    r2 = requests.get(result_url,headers=headers)
    while r2.status_code == 200 and r2.json()['status'] != 'Succeeded':
        r2 = requests.get(result_url,headers=headers)
        time.sleep(0.5)
        print('status:',r2.json()['status'])
    carcard = ''
    lines = r2.json()['recognitionResult']['lines']
    for i in range(len(lines)):
        text = lines[i]['text']
        m = re.match(r'^[\w]{2,4}[-. ][\w]{2,4}$',text)
        carcard = m.group()
        return carcard
    if carcard == '':
        return 'can not find car code'