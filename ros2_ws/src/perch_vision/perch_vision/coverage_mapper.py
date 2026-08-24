import os
import math

import numpy as np
import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from nav_msgs.msg import Odometry
from cv_bridge import CvBridge

GRID_EXTENT_M = 15.0
GRID_RESOLUTION_M = 0.5
GRID_SIZE = int(2 * GRID_EXTENT_M / GRID_RESOLUTION_M)
CAMERA_HORIZONTAL_FOV = 1.4
WRITE_INTERVAL_SEC = 5.0
DEFAULT_OUTPUT_PATH = os.path.expanduser('~/perch_captures/coverage_heatmap.png')


def world_to_grid(x, y):
    col = int((x + GRID_EXTENT_M) / GRID_RESOLUTION_M)
    row = int((y + GRID_EXTENT_M) / GRID_RESOLUTION_M)
    return row, col


class CoverageMapper(Node):
    def __init__(self):
        super().__init__('coverage_mapper')
        self.declare_parameter('output_path', DEFAULT_OUTPUT_PATH)
        self.output_path = self.get_parameter('output_path').value
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

        self.bridge = CvBridge()
        self.coverage_count = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.float32)
        self.depth_sum = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.float32)
        self.uav_position = None

        self.create_subscription(Odometry, 'uav/odom', self.on_odom, 10)
        self.create_subscription(Image, 'uav/camera/depth/image_raw', self.on_depth, 10)
        self.create_timer(WRITE_INTERVAL_SEC, self.write_heatmap)

    def on_odom(self, msg):
        p = msg.pose.pose.position
        self.uav_position = (p.x, p.y, p.z)

    def on_depth(self, msg):
        if self.uav_position is None:
            return
        x, y, altitude = self.uav_position
        if altitude <= 0.2:
            return

        depth = self.bridge.imgmsg_to_cv2(msg, desired_encoding='32FC1')
        valid = depth[np.isfinite(depth)]
        mean_depth = float(np.mean(valid)) if valid.size else altitude

        footprint_half = altitude * math.tan(CAMERA_HORIZONTAL_FOV / 2.0)
        r0, c0 = world_to_grid(x - footprint_half, y - footprint_half)
        r1, c1 = world_to_grid(x + footprint_half, y + footprint_half)
        r0, c0 = max(0, r0), max(0, c0)
        r1, c1 = min(GRID_SIZE - 1, r1), min(GRID_SIZE - 1, c1)
        if r0 > r1 or c0 > c1:
            return

        self.coverage_count[r0:r1 + 1, c0:c1 + 1] += 1.0
        self.depth_sum[r0:r1 + 1, c0:c1 + 1] += mean_depth

    def write_heatmap(self):
        if not np.any(self.coverage_count > 0):
            return
        with np.errstate(divide='ignore', invalid='ignore'):
            average_depth = np.where(self.coverage_count > 0, self.depth_sum / self.coverage_count, 0)
        normalized = cv2.normalize(average_depth, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        heatmap = cv2.applyColorMap(normalized, cv2.COLORMAP_JET)
        heatmap[self.coverage_count == 0] = (30, 30, 30)
        cv2.imwrite(self.output_path, heatmap)
        self.get_logger().info(f'Wrote coverage heatmap to {self.output_path}')


def main(args=None):
    rclpy.init(args=args)
    node = CoverageMapper()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
