import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool
import math

class Stop(Node):
    def __init__(self):
        super().__init__("stop")

        self.sub_ = self.create_subscription(
            LaserScan,
            "scan",
            self.laser_callback,
            rclpy.qos.qos_profile_sensor_data
        )
        self.sub_

        self.pub_ = self.create_publisher(
            Bool,
            "stop",
            10
        )
    def laser_callback(self, msg):
        stop_flag = Bool()
        stop_flag.data = False
        
        for i, data in enumerate(msg.ranges):
            angle = msg.angle_min + i * msg.angle_increment
            cx = data * math.cos(angle)
            cy = data * math.sin(angle)
            if 0.01 < cx < 0.2 and -0.1 < cy < 0.1:
                stop_flag.data = True
                break

        self.pub_.publish(stop_flag)

def main(args = None):
    rclpy.init(args=args)
    stop = Stop()

    rclpy.spin(stop)
    stop.destroy_node()
    rclpy.shutdown()
if __name__ == "__main__":
    main()