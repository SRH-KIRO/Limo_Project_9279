import rclpy

from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_msgs.msg import Int32
from std_msgs.msg import Bool



class LimoControl(Node):
    def __init__(self):
        super().__init__("limo_control")

        self.cmd_pub_ = self.create_publisher(
            Twist,
            "cmd_vel",
            10
        )
        self.stop_sub_ = self.create_subscription(
            Bool,
            "stop",
            self.stop_callback,
            10
        )
        self.error_sub_ = self.create_subscription(
            Int32,
            "distance_x",
            self.dis_callback,
            10
        )
        self.stop_flag = True
    
    def stop_callback(self, msg):
        self.stop_flag = msg.data

    def dis_callback(self, msg):
        cmd = Twist()

        cmd.linear.x = 0.3
        cmd.angular.z = msg.data * 0.01

        if self.stop_flag:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0


        self.cmd_pub_.publish(cmd)

    

def main(args = None):
    rclpy.init(args = args)

    lc = LimoControl()

    rclpy.spin(lc)
    lc.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()