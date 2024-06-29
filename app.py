import numpy as np
import cv2
import torch
from flask import Flask, request

from LP_recognition import get_LP_number

app = Flask(__name__)

# LOAD MODEL
with app.app_context():
    LP_detect = torch.hub.load('ultralytics/yolov5', 'custom', 'checkpoints/plate_detection.pt', force_reload=True)
    OCR = torch.hub.load('ultralytics/yolov5', 'custom', 'checkpoints/optical_character_recognition.pt', force_reload=True)


@app.post('/lp_recognition')
def recognize_lp():
    try:
        file = request.files['file']
    except KeyError:
        return {'message': 'Provide file for recognition!'}, 400

    file_bytes = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    plates_information = get_LP_number(image, LP_detect, OCR)
    plates_information = [{i: {'box': box, 'text': text}} for i, (box, text) in enumerate(plates_information)]

    return plates_information


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')