import rclpy
from rclpy.node import Node


class SurveyMission(Node):
    def __init__(self):
        super().__init__('survey_mission')


def main(args=None):
    rclpy.init(args=args)
    node = SurveyMission()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
