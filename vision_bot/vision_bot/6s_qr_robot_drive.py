#!/usr/bin/env python3

from unittest import case
import rclpy
import cv2
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16

class Video_get(Node):
  def __init__(self):
    super().__init__('video_subscriber')# node name
    ## Created a subscriber

    self.vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
    self.img_sub = self.create_subscription(Image,'/frontCam/image_raw',self.video_feed_in,10)
    self.lidar_sub=self.create_subscription(LaserScan,'/scan',self.scan_in,40)
    self.bridge = CvBridge()
    self.line_mid_point=0
    self.linear_vel = 0.2

    self.velocity=Twist()
    self.frame=0

  def scan_in(self,scan_data):
        ## We have 360 data points so we divide them in 3 region
        ## we say if there is something in the region get the smallest distance value of a point in the area
      #Accesing directly through indexes
      right_ray = min( scan_data.ranges[0]  , 100 )
      left_ray  = min( scan_data.ranges[359], 100 )
      front_ray = min( scan_data.ranges[179], 100 )
      print("Front Ray ",round(front_ray,3))
      if (front_ray <= 0.7):
        self.qr_decorder()


  def video_feed_in(self, data):
    self.frame = self.bridge.imgmsg_to_cv2(data,'bgr8')
    cv2.imshow("Frame",  self.frame)
    cv2.waitKey(1)

  def qr_decorder(self):
    decoder = cv2.QRCodeDetector()
    data, points, _ = decoder.detectAndDecode( self.frame)
    if points is not None:
        print('Decoded data: ' + data)

def main(args=None):
  rclpy.init(args=args)
  image_subscriber = Video_get()
  rclpy.spin(image_subscriber)
  rclpy.shutdown()

if __name__ == '__main__':
  main()