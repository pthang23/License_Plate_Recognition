# License Plate Recognition
**VietNam License Plate Recognition**

This repository provides you with a detailed guide on how to build, train and use a Vietnamese License Plate Recognition system. This system can work on all types of plate in Viet Nam

## Data

This repo uses 2 sets of data for 2 stage of license plate recognition problem:

- [License Plate Detection Dataset](https://drive.google.com/drive/folders/1tY4kXbXt2DvV8viALZ01xVOEOefT4LAS?usp=sharing)
- [Optical Character Recognition Dataset](https://drive.google.com/drive/folders/13rMaHOKVlSpJaLdVrj8u1WMIRl0_q2vb?usp=sharing)

Thanks [Mì Ai](https://www.miai.vn/thu-vien-mi-ai/) and [winter2897](https://github.com/winter2897/Real-time-Auto-License-Plate-Recognition-with-Jetson-Nano/blob/main/doc/dataset.md) for sharing a part in this dataset

## Run with docker

```bash
  docker compose up
```
API open on `<host_ip>:5000/lp_recognition`

## Installation

```bash
  git clone https://github.com/pthang23/License_Plate_Recognition.git
  cd License_Plate_Recognition

  # Install Dependencies
  pip install -r ./requirement.txt
```

## Run License Plate Recognition

```bash
  # Run Inference On Webcam (15-20fps if there is 1 license plate in scene)
  python recognition/webcam_LP_recognition.py 

  # Run Inference On Image
  python recognition/LP_recognition.py -i demo/raw/test1.jpg
```

## Open API

```bash
  python app.py 
```
API open on `<host_ip>:5000/lp_recognition`

## Demo Result

<img src="demo/prediction/result4.jpg" alt="Demo1" width="450"/>
<img src="demo/prediction/result5.jpg" alt="Demo2" width="450"/>

## Training

Augment your dataset to help the model be able to recognize license plates from many different perspectives 

```bash
  python processing_function/augmentation.py -d <path/to/dataset>
```

Then you can retrain models using notebook and yaml config in `/training` folder

```bash
  training/plate_detection.ipynb                  #for LP_Detection
  training/optical_character_recognition.ipynb    #for OCR
```

## Reference

YOLOV5 by ultralytics ([YOLOV5](https://github.com/ultralytics/yolov5))
