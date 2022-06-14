#!/usr/bin/python3
'''
This nodes subscribes to Video stream from raspberry pi
performs operations on laptop

publishes motor velocities
'''
import rclpy
import cv2
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from std_msgs.msg import Int16



class Video_get(Node):
  def __init__(self):
    super().__init__('video_subscriber')
    print("Node Started")
    self.subscriber = self.create_subscription(Image,'/Image',self.process_data,10)
    self.bridge = CvBridge() # converting ros images to opencv data
    self.error_value_publisher = self.create_publisher(Int16, '/line_following_error', 10)

    self.error_msg = Int16()
    self.line_mid_point=0

  def process_data(self, data):
    frame = self.bridge.imgmsg_to_cv2(data,'mono8') # performing conversion
    frame=cv2.resize(frame, (640,480), interpolation = cv2.INTER_AREA)
    cv2.imshow("Frame", frame)
    frame = frame[160:475,100:470] ## first is Y then its X
    blurred_frame = cv2.GaussianBlur(frame, (5, 5), 2)
    edged = cv2.Canny(blurred_frame, 0, 75)

    white_inx=[]
    for index,value in enumerate(edged[:][280]): # this value is Y axis of edged frame
        if(value == 255):
            white_inx.append(index)

    # print(white_inx)

    ## Drawing circles for better representation of Segmentation
    if(len(white_inx)==2):
        cv2.circle(img=edged, center = (white_inx[0],280), radius = 2 , color = (255,0,0), thickness=2)
        cv2.circle(img=edged, center = (white_inx[1],280), radius = 2 , color = (255,0,0), thickness=2)
        ## Generating Reference Point ONLY When boundaries are found
        self.line_mid_point= int( (white_inx[0] + white_inx[1]) /2 )
        cv2.circle(img=edged, center = (self.line_mid_point,280), radius =3, color =(255,0,0), thickness=3)
        ## print(self.line_mid_point)

    # ## Generating a reference point to calculate Error
    goal_point  = [185 , 280]
    cv2.circle(img=edged, center = (goal_point[0],goal_point[1]), radius =5, color =(255,0,0), thickness=5)
    self.error_msg.data = int( goal_point[0] - self.line_mid_point )

    ## Conclusion
    # Error is positive -> move left ( rotate counter ClockWise)
    # Error is negative -> Move Right ( rotate ClockWise)
    self.error_value_publisher.publish(self.error_msg)
    print(self.error_msg.data)
    cv2.imshow("Edge", edged)

    cv2.waitKey(1)





def main(args=None):
  rclpy.init(args=args)
  image_subscriber = Video_get()
  rclpy.spin(image_subscriber)
  rclpy.shutdown()

if __name__ == '__main__':
  main()