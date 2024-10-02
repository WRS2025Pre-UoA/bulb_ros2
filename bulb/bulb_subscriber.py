import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Image
from std_msgs.msg import Int64
import cv2
import numpy as np
from cv_bridge import CvBridge,CvBridgeError
# from bulb import distribute_bulb_task
from bulb import param_bulb

class ImageClickPublisher(Node):
    def __init__(self):
        super().__init__('situation_image')
        # publisher
        # self.image_pubs = [
        #     self.create_publisher(Image, 'bulb_bar_image', 1),
        #     self.create_publisher(Image, 'bulb_round_image', 1),
        #     self.create_publisher(Image, 'bulb_param_image', 1)
        # ]
        self.image_pubs = self.create_publisher(Image, 'bulb_param_image', 1)
        # self.bulb_bar_publisher = self.create_publisher(Int64, 'bulb_bar_result',1)
        # self.bulb_round_publisher = self.create_publisher(Int64, 'bulb_round_result',1)
        self.bulb_param_publisher = self.create_publisher(String, 'bulb_param_result',1)
        
        
        self.bridge = CvBridge()
       
        self.topic_sub = self.create_subscription(
            Image,
            'input_bulb_image',
            self.image_callback,
            10
        )

    def image_callback(self, msg):
        try:
            cv_bridge = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            # values = ["BAR_value","ROUND_Value","OPEN or CLOSE"]
            values = ["OPEN", "CLOSE"]
            # num,txt = distribute_bulb_task.distribute_task(values)
            txt = param_bulb.choose_param(cv_bridge,values)
            
            # if num == 0:
            #     bulb_result_param = Int64()
            #     bulb_result_param.data = txt
            #     self.bulb_bar_publisher.publish(bulb_result_param)

            # elif num == 1:
            #     bulb_result_param = Int64()
            #     bulb_result_param.data = txt
            #     self.bulb_round_publisher.publish(bulb_result_param)
            # else:
            #     bulb_result_param = String()
            #     bulb_result_param.data = txt
            #     self.bulb_param_publisher.publish(bulb_result_param)
            bulb_result_param = String()
            bulb_result_param.data = txt
            self.bulb_param_publisher.publish(bulb_result_param)

            bulb_result_image = msg
            self.image_pubs.publish(bulb_result_image)

        except CvBridgeError as e:
            self.get_logger().error(f'Failed to convert image: {e}')



def main(args=None):
    rclpy.init(args=args)
    node = ImageClickPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
