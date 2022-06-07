from flask import Flask, request, Response, jsonify
import cv2
import numpy as np
from PIL import Image
from darknet.darknet import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

network, class_names, class_colors = load_network("./darknet/cfg/yolov4-csp.cfg", "./darknet/cfg/coco.data", "./yolov4-csp.weights")
width = network_width(network)
height = network_height(network)

def darknet_helper(img, width, height):
  darknet_image = make_image(width, height, 3)
  img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  img_resized = cv2.resize(img_rgb, (width, height), interpolation=cv2.INTER_LINEAR)

  img_height, img_width, _ = img.shape
  width_ratio = img_width/width
  height_ratio = img_height/height

  copy_image_from_bytes(darknet_image, img_resized.tobytes())
  detections = detect_image(network, class_names, darknet_image)
  free_image(darknet_image)
  return detections, width_ratio, height_ratio

@app.route('/get-bounding-boxes', methods=['POST'])
def get_bounding_boxes():
  if 'image' not in request.files:
    return Response('No image file.', status=400)
  else:
    file = request.files['image']

    # Read the image.
    img = Image.open(file.stream)

    # Convert img so that it could be processed by cv2.
    detections, width_ratio, height_ratio = darknet_helper(np.array(img), img.width, img.height)

    print(detections)

    mapped_detections = []
    # Convert the detections to a dictionary.
    for label, confidence, bbox in detections:
      left, top, right, bottom = bbox2points(bbox)
      mapped_detections.append({
        'class': label,
        'confidence': confidence,
        'left': int(left * width_ratio),
        'top': int(top * height_ratio),
        'right': int(right * width_ratio),
        'bottom': int(bottom * height_ratio)
      })

    return jsonify({ 
      "detections": mapped_detections,
      "width_ratio": width_ratio,
      "height_ratio": height_ratio
    })
    