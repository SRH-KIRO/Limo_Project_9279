import rclpy
from rclpy.node import Node

import cv2
import numpy as np
from cv_bridge import CvBridge


from std_msgs.msg import Int32
from sensor_msgs.msg import Image



class LaneDetect(Node):
    def __init__(self):
        super().__init__("lane_detect")

        self.sub_ = self.create_subscription(
            Image,
            "/camera/color/image_raw",
            self.image_callback,
            10
        )
        self.sub_
        self.br = CvBridge()

        self.yellow_lane_low = np.array([0, 90, 100])
        self.yellow_lane_high = np.array([60, 220, 255])
        
        self.ref_x = 170

        self.debug_image_pub_ = self.create_publisher(
            Image,
            'debug_image',
            10
        )
        self.error_pub_ = self.create_publisher(
            Int32,
            'distance_x',
            10
        )

        
    def image_callback(self, msg):
        error = Int32()
        error.data = 0

        cv_image = self.br.imgmsg_to_cv2(msg, "bgr8")

        roi_image = cv_image[400: 480, 0: 320]
        his = cv2.cvtColor(roi_image, cv2.COLOR_BGR2HLS)

        mask_yellow = cv2.inRange(his, self.yellow_lane_low, self.yellow_lane_high)

        debug_image = cv2.line(cv_image, (self.ref_x, 0), (self.ref_x, 480), (0, 255, 0), 5)

        M = cv2.moments(mask_yellow)
        if M["m00"] > 0:
            cx = int(M["m10"]/M["m00"])
            cy = int(M["m01"]/M["m00"])
            cy = cy + 400
            debug_image = cv2.circle(debug_image, (cx, cy), 10, (255, 0, 0,), -1)
            error.data = self.ref_x - cx
        else:
            error.data = 0

        self.error_pub_.publish(error)
        self.debug_image_pub_.publish(self.br.cv2_to_imgmsg(debug_image, "bgr8"))

        # cv2.imshow('orig image', cv_image)
        # cv2.imshow('roi_img', roi_image)
        # cv2.imshow('mask img', mask_yellow)
        # cv2.imshow('debug img', debug_image)
        
        # cv2.waitKey(1)

def main(args = None):
    rclpy.init(args=args)
    lane_detect = LaneDetect()

    rclpy.spin(lane_detect)
    lane_detect.destroy_node()
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()