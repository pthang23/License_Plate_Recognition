import cv2
import torch
import argparse
import numpy as np

import processing_function.read_character as re
import processing_function.rotate_image as ro

# LOAD MODEL
LP_detect = torch.hub.load('ultralytics/yolov5', 'custom', 'model/plate_detection.pt', force_reload=True)
OCR = torch.hub.load('ultralytics/yolov5', 'custom', 'model/optical_character_recognition.pt', force_reload=True)

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help='path to input image')
args = ap.parse_args()

image = cv2.imread(args.image)
image1 = image.copy()

list_crop_image = []
list_rotate_image = []
list_OCR_image = []

# PLATE DETECTION
plates = LP_detect(image)
list_plate = plates.pandas().xyxy[0].values.tolist()
for plate in list_plate:
	x1 = int(plate[0])
	y1 = int(plate[1])
	x2 = int(plate[2])
	y2 = int(plate[3])
	cv2.rectangle(image, (x1, y1), (x2, y2), (36,255,12))
	cv2.rectangle(image1, (x1, y1), (x2, y2), (36,255,12))
	crop_image = image[y1:y2, x1:x2]
	list_crop_image.append(crop_image)

	# PLATE ROTATION
	try:
		rotate_image = ro.rotateImage(crop_image)
		list_rotate_image.append(rotate_image)
	except:
		continue

	# OCR
	try:
		characters = OCR(rotate_image)
		list_character = characters.pandas().xyxy[0].values.tolist()
		OCR_image = rotate_image.copy()

		for character in list_character:
			x1c = int(character[0])
			y1c = int(character[1])
			x2c = int(character[2])
			y2c = int(character[3])
			size = (x2c-x1c)*(y2c-y1c)
			cv2.rectangle(OCR_image, (x1c,y1c), (x2c,y2c), (36,255,12), 2)
		list_OCR_image.append(OCR_image)

		list_character = re.sortCharacter(list_character)
		final_result = re.getPlate(list_character)

		cv2.putText(image, final_result, (x1, y1-8), cv2.FONT_HERSHEY_SIMPLEX, 0.2 + (x2-x1)/250, (36,255,12))
	except:
		continue

# SHOW PLATE DETECTION
while True:
	cv2.imshow('Plate Detection', image1)
	if cv2.waitKey(1) == ord(' '): break
cv2.destroyAllWindows()

try:
	height = list_crop_image[0].shape[0]
	for i in range(len(list_crop_image)):
		new_width = int(height / list_crop_image[i].shape[0] * list_crop_image[i].shape[1])
		list_crop_image[i] = cv2.resize(list_crop_image[i], (new_width, height))
		list_rotate_image[i] = cv2.resize(list_rotate_image[i], (new_width, height))
		list_OCR_image[i] = cv2.resize(list_OCR_image[i], (new_width, height))

	# SHOW CROP IMAGE
	crop_images = np.concatenate(list_crop_image, axis=1)
	while True:
		cv2.imshow('Crop Plate', crop_images)
		if cv2.waitKey(1) == ord(' '): break
	cv2.destroyAllWindows()

	# SHOW ROTATE IMAGE
	rotate_images = np.concatenate(list_rotate_image, axis=1)
	while True:
		cv2.imshow('Rotate Image', rotate_images)
		if cv2.waitKey(1) == ord(' '): break
	cv2.destroyAllWindows()

	# SHOW OCR IMAGE
	OCR_images = np.concatenate(list_OCR_image, axis=1)
	while True:
		cv2.imshow('OCR', OCR_images)
		if cv2.waitKey(1) == ord(' '): break
	cv2.destroyAllWindows()
except:
	pass

# SHOW FINAL RESULT
while True:
	cv2.imshow('Final Result', image)
	if cv2.waitKey(1) == ord(' '): break
cv2.destroyAllWindows()
