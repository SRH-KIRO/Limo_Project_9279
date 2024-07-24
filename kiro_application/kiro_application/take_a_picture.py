import rclpy
from rclpy.node import Node

from kiro_msgs.srv import Chalkak
from sensor_msgs.msg import Image

import os
import cv2
from cv_bridge import CvBridge
from datetime import datetime

class LestTakePicture(Node):
    def __init__(self):
        super().__init__("lets_take_a_picture")
        self.br = CvBridge()

        self.image_sub_ = self.create_subscription(
            Image,
            "camera/color/image_raw",
            self.image_callback,
            10
        )
        self.flag = False

        self.srv = self.create_service(Chalkak, 'say_kimchi', self.save_image)
        self.dataset_directory = '/home/wego/resources/dataset'
        self.yolo_directory = '/home/wego/resources/yolo_dateset'

    def image_callback(self, msg):
        self.cv_image = self.br.imgmsg_to_cv2(msg, "bgr8")
        self.flag = True
    
    def save_image(self, req, res):
        if self.flag:
            res.kimchi = True
            current_time_sec = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
            if req.smile:
                image_name = os.path.join(
                    self.dataset_directory,
                    f'img_{current_time_sec}.jpg')
                    
                image = cv2.resize(self.cv_image, (300, 300))
            else :
                image_name = os.path.join(
                    self.yolo_directory,
                    f'img_{current_time_sec}.jpg')
                    
                image = self.cv_image
            cv2.imwrite(image_name, image)

        else:
            res.kimchi = False
        return res

def main(args = None):
    rclpy.init(args = args)
    ltp = LestTakePicture()

    rclpy.spin(ltp)
    ltp.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()