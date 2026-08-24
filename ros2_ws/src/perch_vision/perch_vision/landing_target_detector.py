import rclpy
from rclpy.node import Node


class LandingTargetDetector(Node):
    def __init__(self):
        super().__init__('landing_target_detector')


def main(args=None):
    rclpy.init(args=args)
    node = LandingTargetDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
