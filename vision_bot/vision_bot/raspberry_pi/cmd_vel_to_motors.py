#!/usr/bin/env python3


import rclpy
from rclpy.node import Node
import motor_class as motors
from geometry_msgs.msg import Twist


class drive_rpi(Node):

    def __init__(self):
        super().__init__('Visionbot_driver')
        self.subscriber = self.create_subscription(Twist,'/cmd_vel',self.velocity_cb,10)
        self.motor_obj=motors.setup(23,24,25,14,15,4)
    def velocity_cb(self,velocity_msg):

        right_wheel = (velocity_msg.linear.x + velocity_msg.angular.z ) / 2 ;
        left_wheel = (velocity_msg.linear.x - velocity_msg.angular.z ) /2 ;

        self.motor_obj.set(left_wheel,right_wheel)



def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = drive_rpi()

    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()