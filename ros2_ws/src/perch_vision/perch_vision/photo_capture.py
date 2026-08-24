import os
import time

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

CAPTURE_INTERVAL_SEC = 3.0
DEFAULT_OUTPUT_DIR = os.path.expanduser('~/perch_captures/photos')


class PhotoCapture(Node):
    def __init__(self):
        super().__init__('photo_capture')
        self.declare_parameter('output_dir', DEFAULT_OUTPUT_DIR)
        self.output_dir = self.get_parameter('output_dir').value
        os.makedirs(self.output_dir, exist_ok=True)

        self.bridge = CvBridge()
        self.latest_image = None

        self.create_subscription(Image, 'uav/camera/image_raw', self.on_image, 10)
        self.create_timer(CAPTURE_INTERVAL_SEC, self.save_snapshot)

    def on_image(self, msg):
        self.latest_image = msg

    def save_snapshot(self):
        if self.latest_image is None:
            return
        cv_image = self.bridge.imgmsg_to_cv2(self.latest_image, desired_encoding='bgr8')
        filename = os.path.join(self.output_dir, f'photo_{time.time():.3f}.jpg')
        cv2.imwrite(filename, cv_image)
        self.get_logger().info(f'Saved {filename}')


def main(args=None):
    rclpy.init(args=args)
    node = PhotoCapture()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
