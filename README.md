# Upcoming Course Repository -> ROS2 Raspberry PI Computer Vision Robot

### Installations
- Ubuntu 22.04
- ROS Humble
- Packages
    - pip install opencv-python
    - sudo pip install RPi.GPIO
    - sudo apt-get install ros-foxy-cv-bridge
    - sudo apt-get install v4l-utils



## Projects
- line Following Robot
- AI Survellance Robot
-


### Running
- ### GPIO
-  sudo chown ubuntu /dev/gpiomem
-  sudo chmod g+rw /dev/gpiomem
## Camera Publishing
    - #### Raspberry pi ( publisher)
        - ros2 run image_tools cam2image --ros-args -p burger_mode:=false -p frequency:=5. -p reliability:=best_effort
    - #### PC ( Subscriber )
        - ros2 run image_tools showimage --ros-args -p show_image:=true -p reliability:=best_effort

- ### Camera on Ubuntu

    - v4l2-ctl --list-devices
    - follow (https://wesleych3n.medium.com/enable-camera-in-raspberry-pi-4-with-64-bit-ubuntu-21-04-d97ce728db9d)
    - Differnet approach from previous versions
