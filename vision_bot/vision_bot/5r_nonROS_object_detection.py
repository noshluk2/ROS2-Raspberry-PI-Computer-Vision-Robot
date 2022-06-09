
# -*- coding: utf-8 -*-
from cProfile import label
import cv2
from tflite_runtime.interpreter import Interpreter
import numpy as np
import os
# https://www.tensorflow.org/lite/guide/hosted_models
# http://storage.googleapis.com/download.tensorflow.org/models/tflite/coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip


def detect_from_camera():
	main_dir_path=os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
	model_path = os.path.join(main_dir_path,'data','ssd_mobilenet_v1_1_metadata.tflite')
	labels_path = os.path.join(main_dir_path,'data','labelmap.txt')
	extracted_images = os.path.join(main_dir_path,'extracted_images')

	text_file = open(labels_path, "r")
	labels_array = text_file.readlines()

	interpreter = Interpreter(model_path=model_path)

	interpreter.allocate_tensors()
	input_details = interpreter.get_input_details()
	output_details = interpreter.get_output_details()

	cap = cv2.VideoCapture(0)
	while True:
		ret, cam_img = cap.read()
		key = cv2.waitKey(1)
		if key == 27: # ESC
			break
		img = cv2.cvtColor(cam_img, cv2.COLOR_BGR2RGB)
		img = cv2.resize(img, (300, 300))
		img = img.reshape(1, img.shape[0], img.shape[1], img.shape[2]) # (1, 300, 300, 3)
		img = img.astype(np.uint8)
		interpreter.set_tensor(input_details[0]['index'], img)
		interpreter.invoke()
		boxes = interpreter.get_tensor(output_details[0]['index'])
		labels = interpreter.get_tensor(output_details[1]['index'])
		scores = interpreter.get_tensor(output_details[2]['index'])
		num = interpreter.get_tensor(output_details[3]['index']);
		# print(scores[0][0])
		top_prediction_label=str(labels_array[int(labels[0][0])+1])
		# print(labels_path[labels[0]])

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
					cv2.imwrite(os.path.join(extracted_images ,top_prediction_label+str(scores[0, i]) +'.jpg'), cam_img)
		cv2.imshow('image', cam_img)

	cap.release()
	cv2.destroyAllWindows()


def detect_from_image():
	# prepara input image
	cam_img = cv2.imread('input1.jpg')
#	cv2.imshow('image', img)
	img = cv2.cvtColor(cam_img, cv2.COLOR_BGR2RGB)
	img = cv2.resize(img, (300, 300))
	img = img.reshape(1, img.shape[0], img.shape[1], img.shape[2]) # (1, 300, 300, 3)
	img = img.astype(np.uint8)

	# load model
	interpreter = tf.lite.Interpreter(model_path="ssd_mobilenet_v1_1_metadata.tflite")
	interpreter.allocate_tensors()
	input_details = interpreter.get_input_details()
	output_details = interpreter.get_output_details()

	# set input tensor
	interpreter.set_tensor(input_details[0]['index'], img)

	# run
	interpreter.invoke()

	# get outpu tensor
	boxes = interpreter.get_tensor(output_details[0]['index'])
	labels = interpreter.get_tensor(output_details[1]['index'])
	scores = interpreter.get_tensor(output_details[2]['index'])
	num = interpreter.get_tensor(output_details[3]['index'])

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
			cv2.putText(cam_img,str(int(labels[0, i])),(x0, y0),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 255, 255),2)

#	cv2.imwrite('output.jpg', cam_img)
	cv2.imshow('image', cam_img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


if __name__ == '__main__':
	detect_from_camera()
	# detect_from_image()