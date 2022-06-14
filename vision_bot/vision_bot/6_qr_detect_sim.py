#!/usr/bin/env python3

import rclpy
import cv2
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

class Video_get(Node):
  def __init__(self):
    super().__init__('video_subscriber')# node name
    ## Created a subscriber
    self.subscriber = self.create_subscription(Image,'/Image',self.process_data,10)
    self.bridge = CvBridge()

    self.line_mid_point=0
  def process_data(self, data):
    frame = self.bridge.imgmsg_to_cv2(data,'bgr8') # performing conversion
    decoder = cv2.QRCodeDetector()
    data, points, _ = decoder.detectAndDecode(frame)


    if points is not None:
        print('Decoded data: ' + data)

        points = points[0]
        for i in range(len(points)):
            pt1 = [int(val) for val in points[i]]
            pt2 = [int(val) for val in points[(i + 1) % 4]]
            cv2.line(frame, pt1, pt2, color=(255, 0, 0), thickness=3)

    cv2.imshow("Frame", frame) # displaying what is being recorded
    cv2.waitKey(1) # will save video until it is interrupted



def main(args=None):
  rclpy.init(args=args)
  image_subscriber = Video_get()
  rclpy.spin(image_subscriber)
  rclpy.shutdown()

if __name__ == '__main__':
  main()