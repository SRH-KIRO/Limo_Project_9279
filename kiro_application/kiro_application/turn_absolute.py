import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Imu
from geometry_msgs.msg import Twist
import math

class TurnAbsolute(Node):
    def __init__(self):
        super().__init__('turn_absolute')
        
        self.imu_sub_ = self.create_subscription(
            Imu,
            'imu',
            self.imu_callback,
            10
        )
        self.imu_sub_
        self.cmd_pub_ = self.create_publisher(
            Twist,
            'cmd_vel',
            10
        )
        self.currnet_yaw_ = 0.0
        self.goal_yaw_= 0.0

        self.timer_ = self.create_timer(0.1 , self.timer_callback)

    def set_goal(self, angle):
        self.goal_yaw_ = angle

    def imu_callback(self, msg):
        (roll, pitch, yaw) = self.euler_from_quaternion(
                                msg.orientation.x, 
                                msg.orientation.y, 
                                msg.orientation.z, 
                                msg.orientation.w)
        self.currnet_yaw_ = yaw
        
    
    def euler_from_quaternion(self, x, y, z, w):
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = math.atan2(t0, t1)
     
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)
     
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)
     
        return roll_x, pitch_y, yaw_z # in radians
        
    def timer_callback(self):
        cmd = Twist()
        error = self.goal_yaw_ - self.currnet_yaw_
        error = self.normalize_angole(error)
        print(error)
        
        if abs(error) < 0.05:
            self.destroy_node()
            rclpy.shutdown()  
        if error > 0.0:
            cmd.angular.z = 0.3
        else:
            cmd.angular.z = -0.3
        self.cmd_pub_.publish(cmd)
    def normalize_angole(self, angle):
        while angle >= math.pi:
            angle -= 2 * math.pi
        while angle <= -math.pi:
            angle += 2 * math.pi
        return angle

def main(args=None):
    rclpy.init(args=args)
    ta = TurnAbsolute()
    goal = float(input())
    ta.set_goal(goal)

    rclpy.spin(ta)


if __name__ == "__main__":
    main()
