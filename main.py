import cv2,math
import numpy as np
lower_color_car1 = np.array([0,0,0])#hsv değerleri
upper_color_car1 = np.array([219,255,37])
cap = cv2.VideoCapture(0)

alan = 3000
while True:
    ret,frame=cap.read()
    frame = cv2.flip(frame, 1)#görünütüyü normal hale döndürme
    frame_hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask_car1 = cv2.inRange(frame_hsv,lower_color_car1,upper_color_car1)#maskeleme işlemi
    mask_car1 = cv2.erode(mask_car1,None,iterations=2);mask_car1 = cv2.dilate(mask_car1,None,iterations=2)#gürültü temizliği
    (contours_car1,_) = cv2.findContours(mask_car1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)#kontür çıkarma
    if len(contours_car1) > 0 :#eğer tespit varsa
        cnt_car_1 = max(contours_car1,key=cv2.contourArea)#kontürlerin en büyüğünü alma
        print("Shape Area:"+str(cv2.contourArea(cnt_car_1))) # alan bulmak için
        if int(cv2.contourArea(cnt_car_1)) > alan: # araclar tespit edilirse
            i = 0
            rect_car1 = cv2.minAreaRect(cnt_car_1)#dikdötrgenleri alma
            box_car1 = cv2.boxPoints(rect_car1)#kutu koordinatları oluşturma
            box_car1 = np.int64(box_car1)
            sol_ust_car1 = box_car1[2];sol_alt_car1 = box_car1[1];sag_ust_car1 = box_car1[3];sag_alt_car1 = box_car1[0]
            if abs(box_car1[0][0] - box_car1[1][0]) < abs(box_car1[2][1] - box_car1[1][1]):
                sag_alt_car1 = box_car1[0];sol_alt_car1 = box_car1[1];sol_ust_car1 = box_car1[2];sag_ust_car1 = box_car1[3]
            if abs(box_car1[2][1] - box_car1[1][1]) < abs(box_car1[0][0] - box_car1[1][0]):
                sag_alt_car1 = box_car1[1];sol_alt_car1 = box_car1[2];sol_ust_car1 = box_car1[3];sag_ust_car1 = box_car1[0]
            if abs(box_car1[3][0] - box_car1[2][0]) < abs(box_car1[2][1] - box_car1[1][1]):
                sag_alt_car1 = box_car1[2];sol_alt_car1 = box_car1[3];sol_ust_car1 = box_car1[0];sag_ust_car1 = box_car1[1]
            cv2.drawContours(frame,[box_car1],0,(255,0,0),1)#kontürleri çiz
            cv2.line(frame, (sol_alt_car1[0], sol_alt_car1[1]), (sag_alt_car1[0], sag_alt_car1[1]), (255, 255, 255), 4)
            cv2.putText(frame,'shape',(sol_ust_car1[0],sol_ust_car1[1]),cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,0),2,cv2.LINE_AA)#yazıyı yaz
            try:
                egim_car1 = abs((sol_alt_car1[1]-sag_alt_car1[1])/(sol_alt_car1[0]-sag_alt_car1[0]))#egim ve açı hesabı
                angleR_car1 = math.atan(egim_car1)
                angleD_car1 = round(math.degrees(angleR_car1))
                cv2.putText(frame,str(angleD_car1),(300,50),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),2,cv2.LINE_AA)#açıyı ekrana yaz
            except:
                print("Hata")
    cv2.imshow("orjinal", frame);cv2.imshow("car1",mask_car1)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
