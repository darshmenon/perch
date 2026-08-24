from setuptools import find_packages, setup

package_name = 'perch_uav_control'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='darshmenon',
    maintainer_email='darshmenon02@gmail.com',
    description='PX4 offboard control, survey missions, and landing behavior for the PERCH UAV',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'offboard_control = perch_uav_control.offboard_control:main',
            'survey_mission = perch_uav_control.survey_mission:main',
            'precision_landing = perch_uav_control.precision_landing:main',
        ],
    },
)
