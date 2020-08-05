import rclpy
from rclpy.node import Node

from rclpy.action import ActionClient
from custom_interfaces.action import MoveTo, Tune


class PositionLoopClient(Node):
    """
    Creates a series of action clients
    for sequenced goal seeking positions

    Client requests must be accepted by relevant Action Server
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


def goal_seek(x, y):
    """
    Send request to goal seek position x, y
    """
    rclpy.init(args=None)
    action_client = PositionLoopClient()

    # currently setup to take no PID parameters
    linear = [0.0, 0.0, 0.0]
    angular = [0.0, 0.0, 0.0]

    action_client.send_goal(x, y, linear, angular)
    rclpy.spin(action_client)


def main(args=None):
    for x in range(3):
        goal_seek(.5, .5)
        goal_seek(1.0, 1.0)


if __name__ == '__main__':
    main()
