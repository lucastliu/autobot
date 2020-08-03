import math
import time

import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from rclpy.callback_groups import ReentrantCallbackGroup, MutuallyExclusiveCallbackGroup
from rclpy.executors import MultiThreadedExecutor

from custom_interfaces.action import MoveTo, Tune
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from nav.pid import PID

from rclpy.qos import qos_profile_sensor_data
from nav.motors.SerialMotor import SerialMotor

class Bang(Node):

    def __init__(self):
        super().__init__('b3')
        
        self.group = MutuallyExclusiveCallbackGroup()

        self._action_server = ActionServer(
            node=self,
            action_type=Tune,
            action_name='move_to',
            execute_callback=self.move_to_callback,
            callback_group=self.group)

        self.subscription = self.create_subscription(
            msg_type=Pose,
            topic='pose',
            callback=self.pose_callback,
            qos_profile=qos_profile_sensor_data,
            callback_group=self.group)

        self.sm = SerialMotor("/dev/ttyACM1")
        

        self.x_dest = 0.0
        self.y_dest = 0.0
        self.x = 0.0
        self.y = 0.0
        self.angle = 0.0
        self.r = 1.0
        self.angle_diff = 10
        self.old = [0.0, 0.0]
        self.old2 = [0.0, 0.0]
        self.curr = [0.0, 0.0]
        self.twist = Twist()
        
        self.get_logger().info('BB Node Live')
    def pose_callback(self, pose):
        #self.get_logger().info('Pose: %s' % (pose))  # CHANGE
        self.x = pose.x
        self.y = pose.y
        self.angle = self.angle_convert(math.radians(pose.theta % 360.0))

    def move_to_callback(self, goal_handle):
        self.get_logger().info('Executing Move To...')
        self.x_dest = goal_handle.request.x_dest
        self.y_dest = goal_handle.request.y_dest
        self.r = self.get_distance()
        self.get_logger().info('Start r: {0}'.format(self.r))
        self.old = [0, 0]
        self.old2 = [0, 0]
        self.curr = [0, 0]

        feedback_msg = Tune.Feedback()


        while self.r > 0.2:

            # calculate errors
            self.calculate_closest_turn()
            self.r = self.get_distance()

            # make adjustments
            self.angular_correction()
            self.linear_correction()
            
            # give feedback
            feedback_msg.x_curr = self.x
            feedback_msg.y_curr = self.y
            goal_handle.publish_feedback(feedback_msg)
            #print(feedback_msg)


        # stop motors
        self.sm.set_motor(3, 0)  # right
        self.sm.set_motor(4, 0)  # left

        # close out ROS action
        goal_handle.succeed()
        result = Tune.Result()
        result.x_final = self.x
        result.y_final = self.y
        self.get_logger().info('Finish Move To')


        return result

    def calculate_closest_turn(self):
        """
        Minimum angle needed to turn is never more than pi radians (180 degrees). 
        No need to turn the long way around.
        """
        
        a = self.angle - self.steering_angle()
        if a > math.pi:
            a -= 2*math.pi

        elif a < -1*math.pi:
            a += 2*math.pi
            
        self.angle_diff = a
        
    def angle_convert(self, a):
        """
        Convert raw angle heading (radians) to proper co-ordinate system
        """
        if a > math.pi:
            a *= -1

        else:
            a = 2*math.pi - a
            
        return a
            
    def get_distance(self):
        return math.sqrt(
            math.pow(self.x_dest - self.x, 2)
            + math.pow(self.y_dest - self.y, 2)
            )
            
    def move(self, T):
        self.smoothing()
        print("Move: {}".format(str(self.curr)))
        self.sm.set_motor(3, self.curr[0])  # left
        self.sm.set_motor(4, self.curr[1])  # right

        time.sleep(T)
        
    def smoothing(self): #prev turning has too much say currently
        self.curr[0] = .05*self.old2[0] + .1*self.old[0] + .85*self.curr[0]
        self.curr[1] = .05*self.old2[1] + .1*self.old[1] + .85*self.curr[1]
        self.old2 = self.old
        self.old = self.curr

    def linear_smooth(self, d):
        if d > 1:
            return 1
        elif d < .6:
            return .6
        else:
            return d
    
    def angular_smooth(self, a):
        return .6
        y = a / math.pi
        if y > .6:
            return .6
        if y < .4:
            return .4
        return y
            
    def linear_correction(self):
        self.r = self.get_distance()
        speed = self.linear_smooth(self.r)
        print("Initial Speed: {}".format(speed))
        self.curr = [speed, speed]
        T = self.r / 4
        if T < .05:
            T = .05
        self.move(T)

    def angular_correction(self):
        while abs(self.angle_diff) > (math.pi / 30):
            self.calculate_closest_turn()
                
            spin = self.angular_smooth(abs(self.angle_diff))
            print("Spin: {}".format(spin))
            if self.angle_diff > 0:
                self.curr[0] = spin
                self.curr[1] = -1*spin

            else:
                self.curr[0] = -1*spin
                self.curr[1] = spin

            self.move(.05)
        
    def steering_angle(self):
        return math.atan2(self.y_dest - self.y, self.x_dest - self.x)


def main(args=None):
    rclpy.init(args=args)
    
    try:
        server = Bang()
        executor = MultiThreadedExecutor()
        executor.add_node(server)
    
        try:
            executor.spin()
            
        finally:
            executor.shutdown()
            server.destroy_node()
    
    finally:
        rclpy.shutdown()
        

if __name__ == '__main__':
    main()
