import cv2
import lincese_module_github as m

img = cv2.imread('自分のパス')
cv2.imshow('Frame',img)#顯示影像
k = cv2.waitKey(100)#等待按鍵輸入

cv2.imwrite('shot2.jpg',img)#儲存影像
text = m.get_license(img)
print('test',text)


        


















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