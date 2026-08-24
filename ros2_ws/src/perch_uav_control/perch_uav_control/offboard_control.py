import rclpy
from rclpy.node import Node


class OffboardControl(Node):
    def __init__(self):
        super().__init__('offboard_control')


def main(args=None):
    rclpy.init(args=args)
    node = OffboardControl()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
