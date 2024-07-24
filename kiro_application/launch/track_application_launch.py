import launch
import launch_ros.actions

def generate_launch_description():
    return launch.LaunchDescription([
        launch_ros.actions.Node(
            package='kiro_application',
            executable='stop',
            name='stop_node'),
        launch_ros.actions.Node(
            package='kiro_application',
            executable='lane_detect',
            name='lane_detect_node'),
        launch_ros.actions.Node(
            package='kiro_application',
            executable='limo_control',
            name='limo_control_node'),
  ])