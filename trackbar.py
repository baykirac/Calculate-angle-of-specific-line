import cv2
import numpy as np
cap = cv2.VideoCapture(0)
frame_counter = 0
def nothing(x):
    pass
cv2.namedWindow("Trackbar")
cv2.resizeWindow("Trackbar",500,500)
cv2.createTrackbar("Lower - H","Trackbar",0,255,nothing)
cv2.createTrackbar("Lower - S","Trackbar",0,255,nothing)
cv2.createTrackbar("Lower - V","Trackbar",0,255,nothing)

cv2.createTrackbar("Upper - H","Trackbar",0,255,nothing)
cv2.createTrackbar("Upper - S","Trackbar",0,255,nothing)
cv2.createTrackbar("Upper - V","Trackbar",0,255,nothing)
cv2.setTrackbarPos("Upper - H","Trackbar",180)
cv2.setTrackbarPos("Upper - S","Trackbar",255)
cv2.setTrackbarPos("Upper - V","Trackbar",255)

while True:
    ret,frame=cap.read()
    frame_counter += 1
    frame = cv2.resize(frame,(640,480))
    frame=cv2.flip(frame,1)
    if frame_counter == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        frame_counter = 0  # Or whatever as long as it is the same as next line
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    frame_hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    lower_h = cv2.getTrackbarPos("Lower - H", "Trackbar")
    lower_s = cv2.getTrackbarPos("Lower - S", "Trackbar")
    lower_v = cv2.getTrackbarPos("Lower - V", "Trackbar")
    upper_h = cv2.getTrackbarPos("Upper - H", "Trackbar")
    upper_s = cv2.getTrackbarPos("Upper - S", "Trackbar")
    upper_v = cv2.getTrackbarPos("Upper - V", "Trackbar")
    lower_color = np.array([lower_h,lower_s,lower_v])
    upper_color = np.array([upper_h, upper_s, upper_v])
    mask = cv2.inRange(frame_hsv,lower_color,upper_color)
    kernel = np.ones((3,3),np.uint8)
    # mask = cv2.erode(mask,kernel)
    # mask = cv2.dilate(mask, kernel, iterations=7)
    cv2.imshow("Original",frame)
    cv2.imshow("Mask",mask)
    if cv2.waitKey(10) & 0xFF==ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
