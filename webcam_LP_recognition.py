import cv2
import torch

import processing_function.read_character as re
import processing_function.rotate_image as ro

# LOAD MODEL
LP_detect = torch.hub.load('ultralytics/yolov5', 'custom', 'model/plate_detection.pt', force_reload=True)
OCR = torch.hub.load('ultralytics/yolov5', 'custom', 'model/optical_character_recognition.pt', force_reload=True)

video = cv2.VideoCapture(0)
while True:
	success, frame = video.read()
	if not success: break

	# PLATE DETECTION
	plates = LP_detect(frame)
	list_plate = plates.pandas().xyxy[0].values.tolist()
	for plate in list_plate:
		x1 = int(plate[0])
		y1 = int(plate[1])
		x2 = int(plate[2])
		y2 = int(plate[3])
		cv2.rectangle(frame, (x1, y1), (x2, y2), (36,255,12))
		crop_image = frame[y1:y2, x1:x2]

		# PLATE ROTATION
		try:
			rotate_image = ro.rotateImage(crop_image)
		except:
			continue

		# OCR
		try:
			characters = OCR(rotate_image)
			list_character = characters.pandas().xyxy[0].values.tolist()
			list_character = re.sortCharacter(list_character)
			final_result = re.getPlate(list_character)

			cv2.putText(frame, final_result, (x1, y1-8), cv2.FONT_HERSHEY_SIMPLEX, 0.2 + (x2-x1)/250, (36,255,12))
		except:
			continue


	cv2.imshow('LP DETECTION', frame)
	
	# PRESS SPACE BUTTON TO TURN OFF CAMERA
	if cv2.waitKey(1) == ord(' '): break
cv2.destroyAllWindows()
video.release()
