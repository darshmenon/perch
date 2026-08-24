import rclpy
from rclpy.node import Node


class PrecisionLanding(Node):
    def __init__(self):
        super().__init__('precision_landing')


def main(args=None):
    rclpy.init(args=args)
    node = PrecisionLanding()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
