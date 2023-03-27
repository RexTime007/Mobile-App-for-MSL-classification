import cv2 as cv

cap = cv.VideoCapture('http://192.168.1.72:8080/video')

while True:
    ret, frame = cap.read()
    if ret == True:
        
        cv.imshow("Tracking", frame)
    
    if cv.waitKey(int(1000/30)) & 0xFF==ord('v'):
        break
    
cap.release()
cv.destroyAllWindows()