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
        (os.path.join('share', package_name,'data'), glob('data/*')),
        (os.path.join('share', package_name,'extracted_images'), glob('extracted_images/*')),

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
            'line_segmentation = vision_bot.4ra_line_following_segmentaion:main',
            'line_follow_drive = vision_bot.4rb_line_follow_drive:main',
            'camera_feed_pub = vision_bot.2r_video_publisher:main',
            'cmdvel_to_pwm = vision_bot.1r_cmd_vel_to_motors:main',
            'sdfSpawner = vision_bot.1_sdf_spawner:main',
            'qr_detection = vision_bot.6_qr_detect_sim:main',
            'test_node = vision_bot.test:main',
            'object_detection_node = vision_bot.6r_object_detection_node:main',
        ],
    },
)
