import rclpy
from rclpy.node import Node


class CoverageMapper(Node):
    def __init__(self):
        super().__init__('coverage_mapper')


def main(args=None):
    rclpy.init(args=args)
    node = CoverageMapper()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
