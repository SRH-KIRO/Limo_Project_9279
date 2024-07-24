from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'kiro_application'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='wego',
    maintainer_email='changmin@wego-robotics.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'move_limo = kiro_application.move_limo:main',
            'turn_absolute = kiro_application.turn_absolute:main',
            'stop = kiro_application.stop:main',
            'lane_detect = kiro_application.lane_detect:main',
            'limo_control = kiro_application.limo_control:main',
            'take_a_picture = kiro_application.take_a_picture:main',
        ],
    },
)
