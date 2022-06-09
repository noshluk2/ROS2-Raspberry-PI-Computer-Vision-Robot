'''
Tell them path setting process is totally different
'''
import cv2
import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from tflite_runtime.interpreter import Interpreter
from ament_index_python.packages import get_package_share_directory
import numpy as np
import os

# https://www.tensorflow.org/lite/guide/hosted_models
# http://storage.googleapis.com/download.tensorflow.org/models/tflite/coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip


class Object_detection(Node):
	def __init__(self):
		super().__init__('video_publisher_node')
		print("Object Detection node Started")
		self.bridge = CvBridge()
		self.img_msg=Image()
		self.sequence=0
		package_share_dir = get_package_share_directory("vision_bot")
		model_path = os.path.join(package_share_dir,'data','ssd_mobilenet_v1_1_metadata.tflite')
		labels_path = os.path.join(package_share_dir,'data','labelmap.txt')
		self.extracted_images = os.path.join(package_share_dir,'extracted_images')
		self.subscriber = self.create_subscription(Image,'/Image',self.detect_objects,10)
		text_file = open(labels_path, "r")
		self.labels_array = text_file.readlines()
		self.interpreter = Interpreter(model_path=model_path)






	def detect_objects(self,data):
		cam_img = self.bridge.imgmsg_to_cv2(data,'bgr8')
		img = cv2.cvtColor(cam_img, cv2.COLOR_BGR2RGB)
		img = cv2.resize(img, (300, 300))
		img = img.reshape(1, img.shape[0], img.shape[1], img.shape[2]) # (1, 300, 300, 3)
		img = img.astype(np.uint8)
		self.interpreter.allocate_tensors()
		self.input_details = self.interpreter.get_input_details()
		self.output_details = self.interpreter.get_output_details()
		self.interpreter.set_tensor(self.input_details[0]['index'], img)
		self.interpreter.invoke()
		boxes  = self.interpreter.get_tensor(self.output_details[0]['index'])
		labels = self.interpreter.get_tensor(self.output_details[1]['index'])
		scores = self.interpreter.get_tensor(self.output_details[2]['index'])
		top_prediction_label=str(self.labels_array[int(labels[0][0])+1])

		for i in range(boxes.shape[1]):
			if scores[0, i] > 0.5:
				box = boxes[0, i, :]
				x0 = int(box[1] * cam_img.shape[1])
				y0 = int(box[0] * cam_img.shape[0])
				x1 = int(box[3] * cam_img.shape[1])
				y1 = int(box[2] * cam_img.shape[0])
				box = box.astype(np.int)
				cv2.rectangle(cam_img, (x0, y0), (x1, y1), (255, 0, 0), 2)
				cv2.rectangle(cam_img, (x0, y0), (x0 + 100, y0 - 30), (255, 0, 0), -1)
				cv2.putText(cam_img,top_prediction_label,(x0, y0),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 255, 255),2)

				if(scores[0][0] > 0.55):
					cv2.imwrite(os.path.join(self.extracted_images ,top_prediction_label+str(scores[0, i]) +'.jpg'), cam_img)
		print(".")
		cv2.imshow('image', cam_img)




def main(args=None):
  rclpy.init(args=args)
  image_subscriber = Object_detection()
  rclpy.spin(image_subscriber)
  rclpy.shutdown()

if __name__ == '__main__':
  main()