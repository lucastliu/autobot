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


class PositionPID(Node):

    def __init__(self):
        super().__init__('position_pid')
        
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
            qos_profile=4,
            callback_group=self.group)

        self.publisher = self.create_publisher(Twist, 'auto_vel', 1)
        



        self.x_dest = 0.0
        self.y_dest = 0.0
        self.x = 0.0
        self.y = 0.0
        self.angle = 0.0
        self.r = 1.0
        self.angle_diff = 10

        self.twist = Twist()
        
        self.get_logger().info('PID Node Live')
    def pose_callback(self, pose):
        #self.get_logger().info('Pose: %s' % (pose))  # CHANGE
        self.x = pose.x
        self.y = pose.y
        self.angle = math.radians(pose.theta % 360.0) #carefully consider trig options
        
        if self.angle > math.pi:
            self.angle = self.angle - 2*math.pi

    def move_to_callback(self, goal_handle):
        self.get_logger().info('Executing Move To...')
        L = goal_handle.request.linear
        A = goal_handle.request.angular
        self.angle_pid = PID(kp=A[0], ki=A[1], kd=A[2])  # 6 0 0
        self.distance_pid = PID(kp=L[0], ki=L[1], kd=L[2])  # 1.5 0 0
        self.x_dest = goal_handle.request.x_dest
        self.y_dest = goal_handle.request.y_dest
        self.r = self.get_distance()
        self.get_logger().info('Start r: {0}'.format(self.r))

        # return x,y during each cycle
        # return final position
        feedback_msg = Tune.Feedback()

        while self.r > 0.4:

            # calculate
            self.linear_correction()
            

            self.angular_correction()

            # publish velocity updates
            self.publisher.publish(self.twist)
            
            # give feedback
            feedback_msg.x_curr = self.x
            feedback_msg.y_curr = self.y
            goal_handle.publish_feedback(feedback_msg)
            #print(feedback_msg)

            # update while condition
            self.r = self.get_distance()

        #stop motors
        self.twist.linear.x = 0.0
        self.twist.angular.z = 0.0
        self.publisher.publish(self.twist)
        
        goal_handle.succeed()

        result = Tune.Result()
        result.x_final = self.x
        result.y_final = self.y
        

        
        self.get_logger().info('Finish Move To')


        return result

    def get_distance(self):
        return math.sqrt(
            math.pow(self.x_dest - self.x, 2)
            + math.pow(self.y_dest - self.y, 2)
            )

    def linear_correction(self):
        pid_dist = self.distance_pid.update(self.r)
        #self.get_logger().info('PID r: {0}'.format(pid_dist))
        self.twist.linear.x = pid_dist

    def angular_correction(self):
        self.angle_diff = self.angle - self.steering_angle()
        
        if self.angle_diff > math.pi:
            self.angle_diff = self.angle_diff - 2*math.pi

        if self.angle_diff < -1*math.pi:
            self.angle_diff = self.angle_diff + 2*math.pi
            
        pid_angle = self.angle_pid.update(self.angle_diff)
        self.twist.angular.z = pid_angle
        
    def steering_angle(self):
        return math.atan2(self.y_dest - self.y, self.x_dest - self.x)


def main(args=None):
    rclpy.init(args=args)
    
    try:
        server = PositionPID()
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
