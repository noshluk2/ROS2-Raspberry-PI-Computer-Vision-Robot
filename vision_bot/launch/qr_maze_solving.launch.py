import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    package_share_dir = get_package_share_directory("vision_bot")
    qr_maze_path = os.path.join(package_share_dir, "models","model_qr.sdf")

    return LaunchDescription(
        [
           IncludeLaunchDescription(
            PythonLaunchDescriptionSource( os.path.join(package_share_dir, 'launch', 'gazebo.launch.py') ),
            ),
            Node(
                package="vision_bot",
                executable="sdfSpawner_node",
                arguments=[qr_maze_path,"Maze"],
                output= 'screen'
            ),

        ]
    )