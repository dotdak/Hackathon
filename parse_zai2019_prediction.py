#!/usr/bin/env python
# coding: utf-8
import os
import glob
import json

# TODO: CHANGING THIS PATH TO YOUR DATABASE
DATABASE_PATH = '/content/drive/My Drive/'
# DATABASE_PATH = 'path/to/your/local/dataset/zai2019_hackaton_*/'
# TODO: CHANGING THIS TO YOUR SET SPLIT
# 'val': public submission
# 'test': private submission
SPLIT = 'val'
IMAGES_PATH = os.path.join(DATABASE_PATH, 'test_images', SPLIT)
NINEDASH_CATEGORY_ID = 1
MAX_DETECTION = 10

image_paths = glob.glob('{}/*.jpg'.format(IMAGES_PATH))

def get_img_id(img_path):
    # Parse image path to image id using for evaluation
    img_name = os.path.basename(img_path)
    return int(img_name.split('.')[0])

def get_img_basename(img_path):
    # Parse image path to image id using for evaluation
    img_name = os.path.basename(img_path)
    return img_name.split('.')[0]

detection_results = {}

# TODO: NEED MODICATION
# generate dummy prediction here
# please modify it with your prediction
def dummy_box_predict(basename):
    prediction = []
    # if no 9dash detected, return empty array
    # for i in range(8):
    with open('/content/drive/My Drive/results/{}.txt'.format(basename), 'r') as f:
        data = f.readlines()
        data = [line.rstrip() for line in data]
        for bounding_rect in data:
            [x, y, w, h, score] = bounding_rect.split(',')
            prediction.append([float(x), float(y), float(w), float(h), float(score)])
    return prediction

def predict(img_path):
    # Get image id
    img_id = get_img_id(img_path)
    
    # Load image and predict
    prediction = dummy_box_predict(get_img_basename(img_path))
    
    # Save prediction with image id
    detection_results[img_id] = prediction
    
def parse_prediction(target_path='results.json'):
    # Parse detection result to COCO-submission format
    # http://cocodataset.org/#format-results
    detections = []
    for img_id, prediction in detection_results.items():
        for bbox in prediction:
            x, y, w, h, score = bbox
            detections.append({
                "image_id": img_id,
                "category_id": NINEDASH_CATEGORY_ID,
                "bbox": [float(x), float(y), float(w), float(h)],
                "score": float(score)
            })
    with open(target_path, 'w') as f:
        json.dump(detections, f)

print('RUNNING PREDICTION...')
for p in image_paths:
    predict(p)
print('RUNNING PREDICTION... DONE')

print('PARSING PREDICTION...')
parse_prediction(target_path='predict.json')
print('PARSING PREDICTION... DONE')




