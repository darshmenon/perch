import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from std_msgs.msg import Bool

PATROL_WAYPOINTS = [(5.0, 4.0), (10.0, 4.0), (10.0, -4.0), (5.0, -4.0)]
WAYPOINT_TOLERANCE = 0.6
MAX_LINEAR_SPEED = 0.6
MAX_ANGULAR_SPEED = 0.8
ANGULAR_GAIN = 1.5


def yaw_from_quaternion(q):
    return math.atan2(2.0 * (q.w * q.z + q.x * q.y), 1.0 - 2.0 * (q.y * q.y + q.z * q.z))


class LandingPlatformCoordinator(Node):
    def __init__(self):
        super().__init__('landing_platform_coordinator')
        self.waypoint_index = 0
        self.pose = None
        self.landing_in_progress = False

        self.create_subscription(Odometry, 'ugv/odom', self.on_odom, 10)
        self.create_subscription(Bool, 'perch/landing_in_progress', self.on_landing_status, 10)
        self.cmd_pub = self.create_publisher(Twist, 'ugv/cmd_vel', 10)

        self.create_timer(1.0 / 10.0, self.control_loop)

    def on_odom(self, msg):
        p = msg.pose.pose.position
        yaw = yaw_from_quaternion(msg.pose.pose.orientation)
        self.pose = (p.x, p.y, yaw)

    def on_landing_status(self, msg):
        self.landing_in_progress = msg.data

    def control_loop(self):
        if self.pose is None:
            return

        if self.landing_in_progress:
            self.cmd_pub.publish(Twist())
            return

        goal_x, goal_y = PATROL_WAYPOINTS[self.waypoint_index]
        x, y, yaw = self.pose
        dx, dy = goal_x - x, goal_y - y
        distance = math.hypot(dx, dy)

        if distance <= WAYPOINT_TOLERANCE:
            self.waypoint_index = (self.waypoint_index + 1) % len(PATROL_WAYPOINTS)
            return

        heading_error = math.atan2(dy, dx) - yaw
        heading_error = math.atan2(math.sin(heading_error), math.cos(heading_error))

        twist = Twist()
        twist.angular.z = max(-MAX_ANGULAR_SPEED, min(MAX_ANGULAR_SPEED, ANGULAR_GAIN * heading_error))
        twist.linear.x = max(0.0, MAX_LINEAR_SPEED * math.cos(heading_error))
        self.cmd_pub.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    node = LandingPlatformCoordinator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
