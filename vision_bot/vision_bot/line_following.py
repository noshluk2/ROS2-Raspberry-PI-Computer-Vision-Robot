#!/usr/bin/python3

import cv2
import numpy as np
cap = cv2.VideoCapture('tapes.avi')

while True:
    _, frame = cap.read()
    ## Get Information about video dimension
    # width = cap. get(cv2. CAP_PROP_FRAME_WIDTH )
    # height = cap. get(cv2. CAP_PROP_FRAME_HEIGHT )

    ## Region of Interest
    f_1=frame
    frame = frame[300:440,100:550]

    ## Extraction of Edges
    blurred_frame = cv2.GaussianBlur(frame, (5, 5), 2)
    edged = cv2.Canny(blurred_frame, 95, 100)

    ## Get image dimension to draw Left and Right Line
    print(edged.shape)

    ## Appending boundary points into a list
    white_inx=[]
    for index,value in enumerate(edged[:][100]):
        if(value == 255):
            white_inx.append(index)
    # print(white_inx)

    ## Drawing circles for better representation of Segmentation
    if(len(white_inx)==2):
        cv2.circle(img=edged, center = (white_inx[0],100), radius =5, color =(255,0,0), thickness=2)
        cv2.circle(img=edged, center = (white_inx[1],100), radius =5, color =(255,0,0), thickness=2)
        ## Generating Reference Point ONLY When boundaries are found
        line_mid_point= int( (white_inx[0] + white_inx[1]) /2 )
        cv2.circle(img=edged, center = (line_mid_point,100), radius =6, color =(255,0,0), thickness=3)
        # print(line_mid_point)

    ## Generating a reference point to calculate Error
    goal_point=[225,100]
    cv2.circle(img=edged, center = (goal_point[0],goal_point[1]), radius =10, color =(255,0,0), thickness=5)
    error = goal_point[0] - line_mid_point
    ## Conclusion
    # Error is positive -> move left ( rotate counter ClockWise)
    # Error is negative -> Move Right ( rotate ClockWise)
    print(error)
    e_1=cv2.Canny(blurred_frame, 95, 100)
    cv2.imshow("Robot Camera", f_1)
    cv2.imshow("Region of Interest", frame)
    cv2.imshow("Edge Extraction", e_1)
    cv2.imshow("Line Following", edged)




    key = cv2.waitKey(1000) ## Increase the waitkey to give a delay
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()