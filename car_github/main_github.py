import cv2
import lincese_module_github as m

capture= cv2.VideoCapture(0)#建立攝影機物件
if capture.isOpened():#攝影機是否正常打開
    while True:
        sucess,img = capture.read()#讀取影像
        if sucess:
            cv2.imshow('Frame',img)#顯示影像
        k = cv2.waitKey(100)#等待按鍵輸入
        if k == ord('s') or k == ord('S'):#ord函數取得按鍵keycode
            cv2.imwrite('shot.jpg',img)#儲存影像
            text = m.get_license(img)
            print('test',text)
        if k == ord('q') or k == ord('Q'):
            print('exit')
            cv2.destroyAllWindows()#關閉視窗
            capture.release()#關閉攝影機
            break
else:
    print('攝影機有問題')
        


















# try:
#     img = cv2.imread('car.jpg')
#     imgSmall = cv2.resize(img,(300,100))
#     cv2.imshow('Frame1',img)
#     cv2.imshow('Frame2',imgSmall)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#     try:
#         cv2.imwrite('small.jpg',imgSmall)
#         print('saved')
#     except:
#         print('Error')

# except:
#     print('Error')