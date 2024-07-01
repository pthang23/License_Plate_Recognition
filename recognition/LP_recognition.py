import cv2
import torch
import argparse

from processing_function import read_character
from processing_function import rotate_plate


def get_LP_number(image, LP_detect_model, OCR_model):
	# PLATE DETECTION
	plates = LP_detect_model(image)
	list_plate = plates.pandas().xyxy[0].values.tolist()

	list_LP_info = []
	for plate in list_plate:
		x1 = int(plate[0])
		y1 = int(plate[1])
		x2 = int(plate[2])
		y2 = int(plate[3])
		crop_image = image[y1:y2, x1:x2]

		# PLATE ROTATION
		try:
			rotate_image = rotate_plate.rotateImage(crop_image)
		except Exception as e:
			print(e)
			continue

		# OCR
		try:
			characters = OCR_model(rotate_image)
			list_character = characters.pandas().xyxy[0].values.tolist()
			list_character = read_character.sortCharacter(list_character)
			LP_number = read_character.getPlate(list_character)
		except Exception as e:
			print(e)
			continue

		list_LP_info.append(([x1, y1, x2, y2], LP_number))

	return list_LP_info


if __name__ == '__main__':
	# LOAD MODEL
	LP_detect = torch.hub.load('ultralytics/yolov5', 'custom', 'checkpoints/plate_detection.pt', force_reload=True)
	OCR = torch.hub.load('ultralytics/yolov5', 'custom', 'checkpoints/optical_character_recognition.pt', force_reload=True)

	# ADD ARGPARSE
	ap = argparse.ArgumentParser()
	ap.add_argument('-i', '--image', required=True, help='path to input image')
	args = ap.parse_args()

	image = cv2.imread(args.image)
	list_LP_info = get_LP_number(image, LP_detect, OCR)
	for LP_info in list_LP_info:
		box, text = LP_info
		cv2.rectangle(image, box[:2], box[2:], (36, 255, 12))
		cv2.putText(image, text, (box[0], box[1]-8), cv2.FONT_HERSHEY_SIMPLEX, 0.2 + (box[2]-box[0])/250, (36,255,12))

	while True:
		cv2.imshow('Result', image)

		# PRESS SPACE BUTTON TO TURN OFF RESULT IMAGE
		if cv2.waitKey(1) == ord(' '):
			break
	cv2.destroyAllWindows()
