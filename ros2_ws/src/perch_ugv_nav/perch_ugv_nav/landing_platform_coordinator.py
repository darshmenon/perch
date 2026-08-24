import rclpy
from rclpy.node import Node


class LandingPlatformCoordinator(Node):
    def __init__(self):
        super().__init__('landing_platform_coordinator')


def main(args=None):
    rclpy.init(args=args)
    node = LandingPlatformCoordinator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
