from setuptools import find_packages, setup

package_name = 'perch_ugv_nav'

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
    description='Independent navigation and SLAM for the PERCH UGV, plus landing platform coordination',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'landing_platform_coordinator = perch_ugv_nav.landing_platform_coordinator:main',
        ],
    },
)
