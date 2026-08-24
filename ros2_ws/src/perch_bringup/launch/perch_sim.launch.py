import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, SetEnvironmentVariable
from launch_ros.actions import Node

# realpath resolves the --symlink-install symlink back to the source tree
# (repo/ros2_ws/src/perch_bringup/launch/this_file.py), 4 levels above which
# is the repo root containing sim/.
REPO_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '..', '..', '..', '..'))

WORLD_PATH = os.path.join(REPO_ROOT, 'sim', 'worlds', 'perch_world.sdf')
MODELS_PATH = os.path.join(REPO_ROOT, 'sim', 'models')
BRIDGE_CONFIG = os.path.join(
    get_package_share_directory('perch_bringup'), 'config', 'bridge.yaml')


def generate_launch_description():
    return LaunchDescription([
        SetEnvironmentVariable(
            'GZ_SIM_RESOURCE_PATH',
            MODELS_PATH + ':' + os.environ.get('GZ_SIM_RESOURCE_PATH', '')),

        ExecuteProcess(
            cmd=['gz', 'sim', '-r', WORLD_PATH],
            output='screen',
        ),

        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='perch_bridge',
            output='screen',
            parameters=[{'config_file': BRIDGE_CONFIG}],
        ),

        Node(package='perch_uav_control', executable='offboard_control', name='offboard_control'),
        Node(package='perch_uav_control', executable='survey_mission', name='survey_mission'),
        Node(package='perch_uav_control', executable='precision_landing', name='precision_landing'),
        Node(package='perch_uav_control', executable='payload_drop', name='payload_drop'),

        Node(package='perch_vision', executable='photo_capture', name='photo_capture'),
        Node(package='perch_vision', executable='coverage_mapper', name='coverage_mapper'),
        Node(package='perch_vision', executable='landing_target_detector', name='landing_target_detector'),

        Node(package='perch_ugv_nav', executable='landing_platform_coordinator', name='landing_platform_coordinator'),
    ])
