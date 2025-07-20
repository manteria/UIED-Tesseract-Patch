import cv2
import os
import requests
import json
from base64 import b64encode
import time
from PIL import Image
import pytesseract

def Google_OCR_makeImageData(imgpath):
    with open(imgpath, 'rb') as f:
        ctxt = b64encode(f.read()).decode()
        img_req = {
            'image': {
                'content': ctxt
            },
            'features': [{
                'type': 'DOCUMENT_TEXT_DETECTION',
                # 'type': 'TEXT_DETECTION',
                'maxResults': 1
            }]
        }
    return json.dumps({"requests": img_req}).encode()


def ocr_detection_google(imgpath):
    start = time.perf_counter()
    url = 'https://vision.googleapis.com/v1/images:annotate'
    api_key = 'AIzaSyDUc4iOUASJQYkVwSomIArTKhE2C6bHK8U'             # *** Replace with your own Key ***
    imgdata = Google_OCR_makeImageData(imgpath)
    response = requests.post(url,
                             data=imgdata,
                             params={'key': api_key},
                             headers={'Content_Type': 'application/json'})
    # print('*** Text Detection Time Taken:%.3fs ***' % (time.clock() - start))
    print("*** Please replace the Google OCR key at detect_text/ocr.py line 28 with your own (apply in https://cloud.google.com/vision) ***")
    if 'responses' not in response.json():
        raise Exception(response.json())
    if response.json()['responses'] == [{}]:
        # No Text
        return None
    else:
        return response.json()['responses'][0]['textAnnotations'][1:]

def ocr_detection_tesseract(input_file):
    print("*** Detect Text through Tesseract OCR ***")
    image = Image.open(input_file)
    raw_result = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    result = []
    n_boxes = len(raw_result['text'])
    for i in range(n_boxes):
        text = raw_result['text'][i].strip()
        if text != "":
            x = raw_result['left'][i]
            y = raw_result['top'][i]
            w = raw_result['width'][i]
            h = raw_result['height'][i]
            result.append({
                "position": [x, y, x + w, y + h],
                "text": text
            })

    return result