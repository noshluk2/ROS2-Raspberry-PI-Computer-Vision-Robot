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
from std_msgs.msg import Header
import os

class Video_get(Node):
  def __init__(self):
    super().__init__('video_publisher_node')
    self.bridge = CvBridge()
    self.img_msg=Image()
    self.camera = cv2.VideoCapture(0)
    self.sequence=0

    self.video_publisher = self.create_publisher(Image,'/front_cam',10)
    timer_period = 0.5
    self.timer = self.create_timer(timer_period, self.publish_video)


  def publish_video(self):
    _, cv_image = self.camera.read()
    self.img_msg=self.bridge.cv2_to_imgmsg(cv_image, "bgr8")
    self.img_msg.header.frame_id=str(self.sequence)
    self.img_msg.header.stamp = Node.get_clock(self).now().to_msg()
    self.video_publisher.publish(self.img_msg)
    self.sequence +=1
    print(self.img_msg," / ", cv_image)


def main(args=None):
  rclpy.init(args=args)
  image_subscriber = Video_get()
  rclpy.spin(image_subscriber)
  rclpy.shutdown()

if __name__ == '__main__':
  main()