import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry
from std_msgs.msg import Bool, String

from perch_msgs.srv import DropPayload

SURVEY_ALTITUDE = 5.0
WAYPOINT_TIMEOUT_SEC = 20.0


def _lawnmower_waypoints(altitude):
    legs = [-8, -4, 0, 4, 8]
    waypoints = [(0.0, 0.0, altitude)]
    for i, y in enumerate(legs):
        x_start, x_end = (-8.0, 8.0) if i % 2 == 0 else (8.0, -8.0)
        waypoints.append((x_start, y, altitude))
        waypoints.append((x_end, y, altitude))
    return waypoints


class SurveyMission(Node):
    def __init__(self):
        super().__init__('survey_mission')
        self.waypoints = _lawnmower_waypoints(SURVEY_ALTITUDE)
        self.drop_waypoint_index = len(self.waypoints) // 2
        self.waypoint_index = 0
        self.at_goal = False
        self.mission_complete = False
        self.ugv_position = None
        self.wait_start_time = None

        self.goal_pub = self.create_publisher(PoseStamped, 'uav/goal_pose', 10)
        self.mode_pub = self.create_publisher(String, 'uav/mode', 10)
        self.create_subscription(Bool, 'uav/at_goal', self.on_at_goal, 10)
        self.create_subscription(Odometry, 'odom', self.on_ugv_odom, 10)

        self.drop_client = self.create_client(DropPayload, 'drop_payload')

        self.publish_goal(self.waypoints[0])
        self.wait_start_time = self.get_clock().now()
        self.create_timer(0.5, self.tick)

    def on_at_goal(self, msg):
        self.at_goal = msg.data

    def on_ugv_odom(self, msg):
        p = msg.pose.pose.position
        self.ugv_position = (p.x, p.y)

    def publish_goal(self, waypoint):
        msg = PoseStamped()
        msg.header.frame_id = 'uav/odom'
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.pose.position.x = float(waypoint[0])
        msg.pose.position.y = float(waypoint[1])
        msg.pose.position.z = float(waypoint[2])
        self.goal_pub.publish(msg)

    def tick(self):
        if self.mission_complete:
            return

        elapsed = (self.get_clock().now() - self.wait_start_time).nanoseconds / 1e9
        if not (self.at_goal or elapsed > WAYPOINT_TIMEOUT_SEC):
            return

        if self.waypoint_index == self.drop_waypoint_index:
            self.request_drop()

        self.waypoint_index += 1
        if self.waypoint_index >= len(self.waypoints):
            self.begin_landing_approach()
            return

        self.at_goal = False
        self.wait_start_time = self.get_clock().now()
        self.publish_goal(self.waypoints[self.waypoint_index])

    def request_drop(self):
        if self.drop_client.service_is_ready():
            self.drop_client.call_async(DropPayload.Request())
            self.get_logger().info('Payload drop requested')

    def begin_landing_approach(self):
        target = self.ugv_position if self.ugv_position is not None else (3.0, 0.0)
        self.publish_goal((target[0], target[1], 2.0))
        self.mode_pub.publish(String(data='land'))
        self.mission_complete = True
        self.get_logger().info('Survey complete, handing off to precision landing')


def main(args=None):
    rclpy.init(args=args)
    node = SurveyMission()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
