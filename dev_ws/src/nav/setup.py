from setuptools import setup

import os
from glob import glob


package_name = 'nav'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Lucas Liu',
    maintainer_email='lucas.liu@duke.edu',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'motors = nav.motors:main',
            'imu = nav.imu.imu:main',
            'dwm = nav.dwm.dwm:main',
            'mux = nav.mux:main',
            'posefusion = nav.pose_fusion:main',
            'pid = nav.position_pid:main'
        ],
    },
)
