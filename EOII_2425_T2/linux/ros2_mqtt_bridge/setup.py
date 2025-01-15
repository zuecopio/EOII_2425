from setuptools import find_packages, setup

package_name = 'ros2_mqtt_bridge'

setup(
    name = package_name,
    version = '0.0.0',
    packages = find_packages(exclude=['test']),
    data_files = [
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires = ['setuptools'],
    zip_safe = True,
    maintainer = 'Marcos Belda Martinez',
    maintainer_email = 'mbelmar@etsinf.upv.es',
    description = 'Bridge between ROS2 Turtlesim and MQTT broker',
    license = 'No license declared',
    tests_require = ['pytest'],
    entry_points  = {
        'console_scripts': [
            "pattern_controller_node = "
            + package_name + ".turtlesim_pattern_controller:main", # Needed
            
            "communication_node = "
             + package_name + ".communication_node:main" # Needed
        ],
    },
)
