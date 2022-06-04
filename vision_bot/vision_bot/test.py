#!/usr/bin/env python3


import rclpy
from rclpy.node import Node
import motor_class as motors
from geometry_msgs.msg import Twist


class drive_rpi(Node):

    def __init__(self):
        super().__init__('Visionbot_driver')
        self.subscriber = self.create_subscription(Twist,'/cmd_vel',self.velocity_cb,10)

    def velocity_cb(self,velocity_msg):

        right_wheel = (velocity_msg.linear.x + velocity_msg.angular.z ) / 2 ;
        left_wheel = (velocity_msg.linear.x - velocity_msg.angular.z ) /2 ;

        print(left_wheel, " / ", right_wheel)

        # if( left_wheel >0 ):

    #     digitalWrite(L_BACK,left_wheel < 0)
    #     digitalWrite(R_FORW,right_wheel > 0 )
    #     digitalWrite(R_BACK,right_wheel < 0)
    #     speed();
    # if ( velocity_msg.linear.x ==0.0 & velocity_msg.angular.z ==0.0){
    #     stop();
    # }



def main(args=None):
    rclpy.init(args=args)
    motors.setup(23,24,25,14,15,4)
    minimal_publisher = drive_rpi()

    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()