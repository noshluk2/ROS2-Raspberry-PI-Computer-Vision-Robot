
# -*- coding: utf-8 -*-
import cv2
import tensorflow as tf
import numpy as np

# https://www.tensorflow.org/lite/guide/hosted_models
# http://storage.googleapis.com/download.tensorflow.org/models/tflite/coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip


def detect_from_camera():
	# load model
	interpreter = tf.lite.Interpreter(model_path="ssd_mobilenet_v1_1_metadata.tflite")
	interpreter.allocate_tensors()
	input_details = interpreter.get_input_details()
	output_details = interpreter.get_output_details()

	cap = cv2.VideoCapture('test.mp4') # 0はカメラのデバイス番号
	while True:
		# capture image
		ret, img_org = cap.read()
#		cv2.imshow('image', img_org)
		key = cv2.waitKey(1)
		if key == 27: # ESC
			break

		# prepara input image
		img = cv2.cvtColor(img_org, cv2.COLOR_BGR2RGB)
		img = cv2.resize(img, (300, 300))
		img = img.reshape(1, img.shape[0], img.shape[1], img.shape[2]) # (1, 300, 300, 3)
		img = img.astype(np.uint8)
		interpreter.set_tensor(input_details[0]['index'], img)
		interpreter.invoke()
		boxes = interpreter.get_tensor(output_details[0]['index'])
		labels = interpreter.get_tensor(output_details[1]['index'])
		scores = interpreter.get_tensor(output_details[2]['index'])
		num = interpreter.get_tensor(output_details[3]['index']);print(labels[0])
		for i in range(boxes.shape[1]):
			if scores[0, i] > 0.5:
				box = boxes[0, i, :]
				x0 = int(box[1] * img_org.shape[1])
				y0 = int(box[0] * img_org.shape[0])
				x1 = int(box[3] * img_org.shape[1])
				y1 = int(box[2] * img_org.shape[0])
				box = box.astype(np.int)
				cv2.rectangle(img_org, (x0, y0), (x1, y1), (255, 0, 0), 2)
				cv2.rectangle(img_org, (x0, y0), (x0 + 100, y0 - 30), (255, 0, 0), -1)
				cv2.putText(img_org,
					   str(int(labels[0, i])),
					   (x0, y0),
					   cv2.FONT_HERSHEY_SIMPLEX,
					   1,
					   (255, 255, 255),
					   2)

	#	cv2.imwrite('output.jpg', img_org)
		cv2.imshow('image', img_org)

	cap.release()
	cv2.destroyAllWindows()


def detect_from_image():
	# prepara input image
	img_org = cv2.imread('input1.jpg')
#	cv2.imshow('image', img)
	img = cv2.cvtColor(img_org, cv2.COLOR_BGR2RGB)
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
			x0 = int(box[1] * img_org.shape[1])
			y0 = int(box[0] * img_org.shape[0])
			x1 = int(box[3] * img_org.shape[1])
			y1 = int(box[2] * img_org.shape[0])
			box = box.astype(np.int)
			cv2.rectangle(img_org, (x0, y0), (x1, y1), (255, 0, 0), 2)
			cv2.rectangle(img_org, (x0, y0), (x0 + 100, y0 - 30), (255, 0, 0), -1)
			cv2.putText(img_org,
				   str(int(labels[0, i])),
				   (x0, y0),
				   cv2.FONT_HERSHEY_SIMPLEX,
				   1,
				   (255, 255, 255),
				   2)

#	cv2.imwrite('output.jpg', img_org)
	cv2.imshow('image', img_org)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


if __name__ == '__main__':
	detect_from_camera()
	# detect_from_image()