from setuptools import find_packages, setup

package_name = 'perch_vision'

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
    description='Photo capture, depth-based coverage mapping, and ArUco landing target detection for PERCH',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'photo_capture = perch_vision.photo_capture:main',
            'coverage_mapper = perch_vision.coverage_mapper:main',
            'landing_target_detector = perch_vision.landing_target_detector:main',
        ],
    },
)
