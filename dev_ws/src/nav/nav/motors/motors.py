import RPi.GPIO as GPIO
import time

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data, QoSProfile

from std_msgs.msg import String
from geometry_msgs.msg import Twist

from nav.motors.SerialMotor import SerialMotor
from nav.motors.motor_constants import *


class Motors(Node):

    def __init__(self):
        super().__init__('motors')

        p = qos_profile_sensor_data
        p.depth = 1

        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.listener_callback,
            p)
        self.subscription  # prevent unused variable warning

        self.sm = SerialMotor("/dev/ttyACM1")
        self.get_logger().info('Motors Node Live')

    def convert_velocity_to_power(self, vel):
        """
        pseudo regression to convert wheel velocities
        to power commands
        """
        if vel == 0:
            return 0

        neg = False
        if vel < 0:
            vel = -1 * vel
            neg = True

        power = 1.3375 * vel - 0.5473

        if power > .8:
            power = .8
            self.get_logger().info('Exceeded maximum wheel power')
        if power <= .4:
            self.get_logger().info('Low wheel power')
            power = .4
        if neg:
            power = -1 * power

        return power

    def listener_callback(self, twist):
        self.get_logger().info('Twist  Linear: %.6f Angular: %.6f' %
                               (twist.linear.x, twist.angular.z))
        WHEEL_BASE = .15  # distance between wheels, meters
        RADIUS = .035  # wheel radius, meters
        right_vel = (twist.linear.x - twist.angular.z * WHEEL_BASE / 2.0) / RADIUS
        left_vel = (twist.linear.x + twist.angular.z * WHEEL_BASE / 2.0) / RADIUS
        self.get_logger().info('Velocity  Right: %.6f Left: %.6f' %
                               (right_vel, left_vel))
        right_power = self.convert_velocity_to_power(right_vel)
        left_power = self.convert_velocity_to_power(left_vel)
        self.get_logger().info('Power Right: %.3f Left: %.3f' %
                               (right_power, left_power))

        self.sm.set_motor(3, right_power)
        self.sm.set_motor(4, left_power)


def main(args=None):
    rclpy.init(args=args)

    motors = Motors()

    rclpy.spin(motors)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    motors.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
