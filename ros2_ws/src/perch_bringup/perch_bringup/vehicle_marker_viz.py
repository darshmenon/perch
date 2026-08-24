import rclpy
from geometry_msgs.msg import Point
from nav_msgs.msg import Odometry
from rclpy.node import Node
from std_msgs.msg import ColorRGBA
from visualization_msgs.msg import Marker, MarkerArray


class VehicleMarkerViz(Node):
    def __init__(self):
        super().__init__('vehicle_marker_viz')
        self.uav_odom = None
        self.ugv_odom = None

        self.create_subscription(Odometry, 'uav/odom', self.on_uav_odom, 10)
        self.create_subscription(Odometry, 'odom', self.on_ugv_odom, 10)
        self.marker_pub = self.create_publisher(MarkerArray, 'perch/vehicle_markers', 10)
        self.create_timer(0.1, self.publish_markers)

    def on_uav_odom(self, msg):
        self.uav_odom = msg

    def on_ugv_odom(self, msg):
        self.ugv_odom = msg

    def publish_markers(self):
        markers = MarkerArray()
        now = self.get_clock().now().to_msg()

        if self.ugv_odom is not None:
            p = self.ugv_odom.pose.pose.position
            markers.markers.append(self.box_marker(0, 'UGV / AMR', p.x, p.y, 0.35, 2.1, 1.1, 0.45, self.color(0.05, 0.07, 0.08, 1.0), now))
            markers.markers.append(self.box_marker(1, 'UGV deck marker', p.x, p.y, 0.62, 0.75, 0.75, 0.04, self.color(1.0, 1.0, 1.0, 1.0), now))

        if self.uav_odom is not None:
            p = self.uav_odom.pose.pose.position
            markers.markers.append(self.box_marker(10, 'UAV body', p.x, p.y, p.z, 0.45, 0.32, 0.16, self.color(0.2, 0.25, 0.3, 1.0), now))
            markers.markers.append(self.line_marker(11, 'UAV arms', p.x, p.y, p.z, now))

        if markers.markers:
            self.marker_pub.publish(markers)

    def box_marker(self, marker_id, ns, x, y, z, sx, sy, sz, color, stamp):
        marker = Marker()
        marker.header.frame_id = 'odom'
        marker.header.stamp = stamp
        marker.ns = ns
        marker.id = marker_id
        marker.type = Marker.CUBE
        marker.action = Marker.ADD
        marker.pose.position.x = float(x)
        marker.pose.position.y = float(y)
        marker.pose.position.z = float(z)
        marker.pose.orientation.w = 1.0
        marker.scale.x = float(sx)
        marker.scale.y = float(sy)
        marker.scale.z = float(sz)
        marker.color = color
        return marker

    def line_marker(self, marker_id, ns, x, y, z, stamp):
        marker = Marker()
        marker.header.frame_id = 'odom'
        marker.header.stamp = stamp
        marker.ns = ns
        marker.id = marker_id
        marker.type = Marker.LINE_LIST
        marker.action = Marker.ADD
        marker.scale.x = 0.05
        marker.color = self.color(0.1, 0.75, 1.0, 1.0)
        marker.points = [
            self.point(x - 0.65, y, z), self.point(x + 0.65, y, z),
            self.point(x, y - 0.65, z), self.point(x, y + 0.65, z),
        ]
        return marker

    def point(self, x, y, z):
        p = Point()
        p.x = float(x)
        p.y = float(y)
        p.z = float(z)
        return p

    def color(self, r, g, b, a):
        c = ColorRGBA()
        c.r = float(r)
        c.g = float(g)
        c.b = float(b)
        c.a = float(a)
        return c


def main(args=None):
    rclpy.init(args=args)
    node = VehicleMarkerViz()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
