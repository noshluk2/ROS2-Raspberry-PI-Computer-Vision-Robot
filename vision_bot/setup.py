from setuptools import setup
import os
from glob import glob
package_name = 'vision_bot'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name,'launch'), glob('launch/*')),
        (os.path.join('share', package_name,'urdf'), glob('urdf/*')),
        (os.path.join('share', package_name,'meshes'), glob('meshes/*')),
        (os.path.join('share', package_name,'models'), glob('models/*')),

    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='luqman',
    maintainer_email='noshluk2@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'line_following_node = vision_bot.4r_line_following_real:main',
            'camera_node = vision_bot.2r_video_publisher:main',
            'drive_node = vision_bot.1_driver:main',
            'sdfSpawner_node = vision_bot.1_sdf_spawner:main',
            'qr_detection_node = vision_bot.6_qr_detect_sim:main',
            'test_node = vision_bot.test:main',
            'car_drive_node = vision_bot.r_cmd_vel_to_motors:main',
        ],
    },
)
