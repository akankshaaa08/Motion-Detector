import cv2 as cv
import  time, pandas
from datetime import datetime

vid = cv.VideoCapture(0)

first_frame = None
status_list=[None,None]
time =[]
df = pandas.DataFrame(columns=["START","END"])

while True :
    check,frame = vid.read()
    status=0
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray,(21,21),0)      #making the frame blur for more accuracy
    
    if first_frame is None :
        first_frame = gray          # Making the first frame of the video static for reference
        continue                # will not execute the following lines

    delta_frame = cv.absdiff(first_frame,gray)      # Comparing the two frames

    thresh_frame = cv.threshold(delta_frame , 30 , 255 , cv.THRESH_BINARY)[1]
                            # assigning color to different frames
    thresh_frame = cv.dilate(thresh_frame,None,iterations=2)    #Smoothening the edges

    (cnts,_) = cv.findContours(thresh_frame.copy(), cv.RETR_EXTERNAL , cv.CHAIN_APPROX_SIMPLE)

    for contour in cnts :
        if cv.contourArea(contour) < 10000 :
            continue
        status = 1

        (x,y,w,h) = cv.boundingRect(contour)
        cv.rectangle(frame, (x,y) , (x+w , y+h) , (0,255,0) , 3)
    
    status_list.append(status)

    status_list = status_list[-2:]
    
    if status_list[-1] == 1 and status_list[-2] == 0 :
        time.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1 :
        time.append(datetime.now())
    
    #Types of frames: Gray, Delta, Thresh, Color
    #cv.imshow("current_frame",gray)
    #cv.imshow("delta_frame",delta_frame)
    #cv.imshow("thresh_frame",thresh_frame)
    cv.imshow("color_frame",frame)

    k = cv.waitKey(1)
    if k==ord('q') :
        if status == 1 :
            time.append(datetime.now())    
        break
    

#print(status_list)
#print(time)

for t in range (0,len(time),2) :
    df=df.append({"START":time[t] , "END":time[t+1] } , ignore_index=True )

df.to_csv("Times.csv")
print("video working : ",check)
vid.release()
cv.destroyAllWindows()

