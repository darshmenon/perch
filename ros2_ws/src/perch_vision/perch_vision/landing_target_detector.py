import math

import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from nav_msgs.msg import Odometry
from cv_bridge import CvBridge

from perch_msgs.msg import LandingTarget

TARGET_MARKER_ID = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_HORIZONTAL_FOV = 1.4
FOCAL_PX = (CAMERA_WIDTH / 2.0) / math.tan(CAMERA_HORIZONTAL_FOV / 2.0)


class LandingTargetDetector(Node):
    """Detects the ArUco (DICT_4X4_50, id 0) marker on the UGV deck in the UAV's
    downward camera and estimates the marker's position in the uav/odom frame.

    Pixel->world mapping assumes the camera looks straight down with ~0 yaw, using
    a pinhole approximation with altitude as depth (good enough at survey/landing
    altitudes over a flat deck).
    """

    def __init__(self):
        super().__init__('landing_target_detector')
        self.bridge = CvBridge()
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        self.aruco_params = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.aruco_params)

        self.uav_position = None

        self.create_subscription(Odometry, 'uav/odom', self.on_odom, 10)
        self.create_subscription(Image, 'uav/camera/image_raw', self.on_image, 10)
        self.target_pub = self.create_publisher(LandingTarget, 'perch/landing_target', 10)

    def on_odom(self, msg):
        p = msg.pose.pose.position
        self.uav_position = (p.x, p.y, p.z)

    def on_image(self, msg):
        if self.uav_position is None:
            return

        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = self.detector.detectMarkers(gray)

        target = LandingTarget()
        target.header = msg.header

        if ids is not None and TARGET_MARKER_ID in ids.flatten():
            idx = list(ids.flatten()).index(TARGET_MARKER_ID)
            marker_corners = corners[idx][0]
            center_u = float(np.mean(marker_corners[:, 0]))
            center_v = float(np.mean(marker_corners[:, 1]))

            uav_x, uav_y, altitude = self.uav_position
            meters_per_px = max(altitude, 0.1) / FOCAL_PX
            du = center_u - CAMERA_WIDTH / 2.0
            dv = center_v - CAMERA_HEIGHT / 2.0

            marker_world_x = uav_x - meters_per_px * dv
            marker_world_y = uav_y - meters_per_px * du

            target.detected = True
            target.pose.position.x = marker_world_x
            target.pose.position.y = marker_world_y
            target.pose.position.z = 0.0
            marker_area = cv2.contourArea(marker_corners.astype(np.float32))
            target.confidence = float(min(1.0, marker_area / 400.0))
        else:
            target.detected = False
            target.confidence = 0.0

        self.target_pub.publish(target)


def main(args=None):
    rclpy.init(args=args)
    node = LandingTargetDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
