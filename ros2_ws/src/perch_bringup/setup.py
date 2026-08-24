import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'perch_bringup'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*.rviz')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='darshmenon',
    maintainer_email='darshmenon02@gmail.com',
    description='Top-level launch files bringing up the full PERCH simulation: UAV, UGV, and world',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'vehicle_marker_viz = perch_bringup.vehicle_marker_viz:main',
        ],
    },
)
