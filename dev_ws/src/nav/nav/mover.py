# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist

import time
from nav.MotorControllerUSB import MotorControllerUSB


class Mover(Node):

    def __init__(self):
        super().__init__('mover')
        self.subscription = self.create_subscription(
            Twist,
            'key_vel',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        
        power = 80
        self.mc = MotorControllerUSB()
        self.mc.setSpeed(power)

    def listener_callback(self, msg):
        self.get_logger().info('Teleop Command  Linear: %.2f Angular: %.2f' % (msg.linear.x, msg.angular.z)) # CHANGE
        if msg.linear.x:
            self.mc.move(msg.linear.x*.5)
        if msg.angular.z:
            self.mc.turn(msg.angular.z * 10)


def main(args=None):
    rclpy.init(args=args)

    mover = Mover()

    rclpy.spin(mover)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    mover.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()