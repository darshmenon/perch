import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, Twist
from nav_msgs.msg import Odometry
from std_msgs.msg import Bool

MAX_LINEAR_VELOCITY = 1.5
POSITION_TOLERANCE = 0.35
CONTROL_PERIOD = 1.0 / 20.0
PROPORTIONAL_GAIN = 0.8


class OffboardControl(Node):
    """Flies the UAV toward the latest /uav/goal_pose using proportional velocity control.

    MulticopterVelocityControl commands are in the vehicle body frame, but this
    mission never yaws, so body frame and world/odom frame stay aligned and can
    be treated as the same frame here.
    """

    def __init__(self):
        super().__init__('offboard_control')
        self.current_position = None
        self.goal_position = None

        self.create_subscription(Odometry, 'uav/odom', self.on_odom, 10)
        self.create_subscription(PoseStamped, 'uav/goal_pose', self.on_goal, 10)

        self.cmd_pub = self.create_publisher(Twist, 'uav/cmd_vel', 10)
        self.at_goal_pub = self.create_publisher(Bool, 'uav/at_goal', 10)

        self.create_timer(CONTROL_PERIOD, self.control_loop)

    def on_odom(self, msg):
        p = msg.pose.pose.position
        self.current_position = (p.x, p.y, p.z)

    def on_goal(self, msg):
        p = msg.pose.position
        self.goal_position = (p.x, p.y, p.z)

    def control_loop(self):
        if self.current_position is None or self.goal_position is None:
            return

        dx = self.goal_position[0] - self.current_position[0]
        dy = self.goal_position[1] - self.current_position[1]
        dz = self.goal_position[2] - self.current_position[2]
        distance = math.sqrt(dx * dx + dy * dy + dz * dz)

        twist = Twist()
        if distance > POSITION_TOLERANCE:
            twist.linear.x = self._clamp(PROPORTIONAL_GAIN * dx)
            twist.linear.y = self._clamp(PROPORTIONAL_GAIN * dy)
            twist.linear.z = self._clamp(PROPORTIONAL_GAIN * dz)
        self.cmd_pub.publish(twist)
        self.at_goal_pub.publish(Bool(data=distance <= POSITION_TOLERANCE))

    @staticmethod
    def _clamp(value):
        return max(-MAX_LINEAR_VELOCITY, min(MAX_LINEAR_VELOCITY, value))


def main(args=None):
    rclpy.init(args=args)
    node = OffboardControl()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
