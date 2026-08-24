import rclpy
from rclpy.node import Node
from std_msgs.msg import Empty

from perch_msgs.srv import DropPayload


class PayloadDrop(Node):
    def __init__(self):
        super().__init__('payload_drop')
        self.detach_pub = self.create_publisher(Empty, 'uav/payload/detach', 10)
        self.create_service(DropPayload, 'drop_payload', self.on_drop_request)

    def on_drop_request(self, request, response):
        self.detach_pub.publish(Empty())
        response.success = True
        response.message = 'payload detached'
        self.get_logger().info('Payload dropped')
        return response


def main(args=None):
    rclpy.init(args=args)
    node = PayloadDrop()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
