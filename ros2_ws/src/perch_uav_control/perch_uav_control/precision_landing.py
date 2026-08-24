import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, Twist
from nav_msgs.msg import Odometry
from std_msgs.msg import Bool, String

from perch_msgs.msg import LandingTarget

DESCENT_STEP = 0.4
FINAL_ALTITUDE = 0.35
CONFIDENCE_THRESHOLD = 0.5


class PrecisionLanding(Node):
    def __init__(self):
        super().__init__('precision_landing')
        self.landing_active = False
        self.touchdown = False
        self.current_altitude = None

        self.create_subscription(String, 'uav/mode', self.on_mode, 10)
        self.create_subscription(LandingTarget, 'perch/landing_target', self.on_target, 10)
        self.create_subscription(Odometry, 'uav/odom', self.on_odom, 10)

        self.goal_pub = self.create_publisher(PoseStamped, 'uav/goal_pose', 10)
        self.cmd_pub = self.create_publisher(Twist, 'uav/cmd_vel', 10)
        self.enable_pub = self.create_publisher(Bool, 'uav/enable', 10)
        self.landing_in_progress_pub = self.create_publisher(Bool, 'perch/landing_in_progress', 10)

        self.create_timer(0.5, self.publish_status)

    def on_mode(self, msg):
        if msg.data == 'land':
            self.landing_active = True
            self.get_logger().info('Precision landing engaged')

    def on_odom(self, msg):
        self.current_altitude = msg.pose.pose.position.z

    def on_target(self, msg):
        if not self.landing_active or self.touchdown:
            return
        if not msg.detected or msg.confidence < CONFIDENCE_THRESHOLD:
            return

        target_altitude = max(FINAL_ALTITUDE, (self.current_altitude or FINAL_ALTITUDE) - DESCENT_STEP)
        goal = PoseStamped()
        goal.header.frame_id = 'uav/odom'
        goal.header.stamp = self.get_clock().now().to_msg()
        goal.pose.position.x = msg.pose.position.x
        goal.pose.position.y = msg.pose.position.y
        goal.pose.position.z = target_altitude
        self.goal_pub.publish(goal)

        if self.current_altitude is not None and self.current_altitude <= FINAL_ALTITUDE + 0.1:
            self.complete_touchdown()

    def complete_touchdown(self):
        self.touchdown = True
        self.cmd_pub.publish(Twist())
        self.enable_pub.publish(Bool(data=False))
        self.get_logger().info('Touchdown on UGV landing platform')

    def publish_status(self):
        self.landing_in_progress_pub.publish(Bool(data=self.landing_active and not self.touchdown))


def main(args=None):
    rclpy.init(args=args)
    node = PrecisionLanding()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
