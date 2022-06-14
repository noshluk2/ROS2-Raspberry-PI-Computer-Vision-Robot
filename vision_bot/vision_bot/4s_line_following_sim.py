#!/usr/bin/env python3

'''
> Purpose :
This Node is going to save video feed from the upper camera from the simulation .
Which is going to be utilized for furthur image processing to solve the maze .


> Usage :
You need to write below command in terminal where your pacakge is sourced
- ros2 run maze_bot video_recorder

Note : name of the node is actually name of executable file described in setup.py file of our package and not the name of python file

> Inputs:
This node is a Subscriber of '/upper_camera/image_raw' topic which is 30 fps video from camera above the maze
and image is of the size 1280x720 ( RGB )

> Outputs:
This node is just a scriber so output is is not in terms of ROS topic but a video is going to be saved on the disk.


> Instructor Comments :
I wish , students make below changes into the code
- Remove Opencv Dependency
- Resize images and save different sized video
- - Use proper names for the class,node, call back functions and variables
- Add ROS2 logging functionality
- Add comments into functions

Author :
M.Luqman

Date :
16/03/22
'''

import rclpy
import cv2
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
import os
import numpy as np
class Video_get(Node):
  def __init__(self):
    super().__init__('video_subscriber')# node name
    ## Created a subscriber
    self.subscriber = self.create_subscription(Image,'/frontCam/image_raw',self.process_data,10)
    self.bridge = CvBridge() # converting ros images to opencv data
    self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
    self.msg = Twist()
    self.line_mid_point=0
  def process_data(self, data):
    frame = self.bridge.imgmsg_to_cv2(data,'bgr8') # performing conversion
    frame = frame[170:360,100:470] ## first is Y then its X
    blurred_frame = cv2.GaussianBlur(frame, (5, 5), 2)
    edged = cv2.Canny(blurred_frame, 95, 100)
    # print(edged.shape)
    ## Appending boundary points into a list
    white_inx=[]
    for index,value in enumerate(edged[:][170]):
        if(value == 255):
            white_inx.append(index)
    #  print(white_inx)
    ## Drawing circles for better representation of Segmentation
    if(len(white_inx)==2):
        cv2.circle(img=edged, center = (white_inx[0],170), radius = 2 , color = (255,0,0), thickness=1)
        cv2.circle(img=edged, center = (white_inx[1],170), radius = 2 , color = (255,225,0), thickness=1)
        ## Generating Reference Point ONLY When boundaries are found
        self.line_mid_point= int( (white_inx[0] + white_inx[1]) /2 )
        cv2.circle(img=edged, center = (self.line_mid_point,170), radius =3, color =(255,0,0), thickness=2)
        ## print(self.line_mid_point)

    ## Generating a reference point to calculate Error
    # frame_mid_point = [50,50]
    goal_point      = [110,170]
    cv2.circle(img=edged, center = (goal_point[0],goal_point[1]), radius =5, color =(255,0,225), thickness=2)
    error = goal_point[0] - self.line_mid_point
    print(error)

    ## Setting up velocity
    if(error > 0):
        self.msg.angular.z=0.5
    else:
        self.msg.angular.z=-0.5
    self.msg.linear.x=0.5

    self.publisher_.publish(self.msg)

    cv2.imshow("Edge", edged)
    cv2.imshow("Frame", frame)
    cv2.waitKey(1)


def main(args=None):
  rclpy.init(args=args)
  image_subscriber = Video_get()
  rclpy.spin(image_subscriber)
  rclpy.shutdown()

if __name__ == '__main__':
  main()