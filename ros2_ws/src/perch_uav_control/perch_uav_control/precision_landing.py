import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, Twist
from nav_msgs.msg import Odometry
from std_msgs.msg import Bool, String

from perch_msgs.msg import LandingTarget

DESCENT_STEP = 0.4
FINAL_ALTITUDE = 0.35
CONFIDENCE_THRESHOLD = 0.5

# The UGV keeps patrolling (slowly) during landing, so the marker is a moving
# target. LEAD_TIME projects it forward using the UGV's current velocity to
# cancel out the tracking lag of a proportional position controller, and
# ALIGN_TOLERANCE gates descent on actually being over the platform first,
# rather than chasing it down at altitude and missing.
LEAD_TIME = 0.6
ALIGN_TOLERANCE = 0.5
TOUCHDOWN_ALIGN_TOLERANCE = 0.4


class PrecisionLanding(Node):
    def __init__(self):
        super().__init__('precision_landing')
        self.landing_active = False
        self.touchdown = False
        self.current_position = None
        self.ugv_velocity = (0.0, 0.0)

        self.create_subscription(String, 'uav/mode', self.on_mode, 10)
        self.create_subscription(LandingTarget, 'perch/landing_target', self.on_target, 10)
        self.create_subscription(Odometry, 'uav/odom', self.on_odom, 10)
        self.create_subscription(Odometry, 'ugv/odom', self.on_ugv_odom, 10)

        self.goal_pub = self.create_publisher(PoseStamped, 'uav/goal_pose', 10)
        self.velocity_ff_pub = self.create_publisher(Twist, 'uav/goal_velocity', 10)
        self.cmd_pub = self.create_publisher(Twist, 'uav/cmd_vel', 10)
        self.enable_pub = self.create_publisher(Bool, 'uav/enable', 10)
        self.landing_in_progress_pub = self.create_publisher(Bool, 'perch/landing_in_progress', 10)

        self.create_timer(0.5, self.publish_status)

    def on_mode(self, msg):
        if msg.data == 'land':
            self.landing_active = True
            self.get_logger().info('Precision landing engaged')

    def on_odom(self, msg):
        p = msg.pose.pose.position
        self.current_position = (p.x, p.y, p.z)

    def on_ugv_odom(self, msg):
        q = msg.pose.pose.orientation
        yaw = math.atan2(2.0 * (q.w * q.z + q.x * q.y), 1.0 - 2.0 * (q.y * q.y + q.z * q.z))
        vx, vy = msg.twist.twist.linear.x, msg.twist.twist.linear.y
        self.ugv_velocity = (
            vx * math.cos(yaw) - vy * math.sin(yaw),
            vx * math.sin(yaw) + vy * math.cos(yaw),
        )

    def on_target(self, msg):
        if not self.landing_active or self.touchdown or self.current_position is None:
            return
        if not msg.detected or msg.confidence < CONFIDENCE_THRESHOLD:
            return

        vx, vy = self.ugv_velocity
        lead_x = msg.pose.position.x + vx * LEAD_TIME
        lead_y = msg.pose.position.y + vy * LEAD_TIME

        cx, cy, cz = self.current_position
        horizontal_error = math.hypot(lead_x - cx, lead_y - cy)

        # Only step altitude down once roughly over the platform; otherwise hold
        # altitude and close the horizontal gap first so a fast-moving platform
        # doesn't get chased all the way to the ground and missed.
        target_altitude = max(FINAL_ALTITUDE, cz - DESCENT_STEP) if horizontal_error <= ALIGN_TOLERANCE else cz

        goal = PoseStamped()
        goal.header.frame_id = 'uav/odom'
        goal.header.stamp = self.get_clock().now().to_msg()
        goal.pose.position.x = lead_x
        goal.pose.position.y = lead_y
        goal.pose.position.z = target_altitude
        self.goal_pub.publish(goal)

        velocity_ff = Twist()
        velocity_ff.linear.x = vx
        velocity_ff.linear.y = vy
        self.velocity_ff_pub.publish(velocity_ff)

        if cz <= FINAL_ALTITUDE + 0.1 and horizontal_error <= TOUCHDOWN_ALIGN_TOLERANCE:
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
