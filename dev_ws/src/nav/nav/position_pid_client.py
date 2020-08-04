import rclpy
from rclpy.node import Node

from rclpy.action import ActionClient
from custom_interfaces.action import MoveTo, Tune


class PositionPIDClient(Node):
    """
    Client script for a position action. Requests a desired heading in degrees.
    Receives current heading feedback during action,
    as well as final angle after action is completed.

    Action request must be processed by a heading server
    """
    def __init__(self):
        super().__init__('position_pid_client')
        self._action_client = ActionClient(self, Tune, 'move_to')

    def send_goal(self, x_dest, y_dest, linear, angular):
        goal_msg = Tune.Goal()
        goal_msg.x_dest = x_dest
        goal_msg.y_dest = y_dest
        goal_msg.linear = linear
        goal_msg.angular = angular
        self._action_client.wait_for_server()

        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback)

        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')
        
        self._get_result_future = goal_handle.get_result_async()

        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info('Final Position: {0},  {1}'
                               .format(result.x_final, result.y_final))
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info('Feedback: {0},  {1}'
                               .format(feedback.x_curr, feedback.y_curr))


def main(args=None):
    rclpy.init(args=args)

    action_client = PositionPIDClient() #TODO: make this recallable
    x, y = [float(item) for item in input("Desired X Y: ").split()]
    linear = [0.0, 0.0, 0.0]  # [float(item) for item in input("Enter linear PID Constants : ").split()] 
    angular = [0.0, 0.0, 0.0]  # [float(item) for item in input("Enter Angular PID Constants : ").split()] 
    action_client.send_goal(x, y, linear, angular)

    rclpy.spin(action_client)


if __name__ == '__main__':
    main()
