import detect_text.ocr as ocr
from detect_text.Text import Text
import numpy as np
import cv2
import json
import time
import os
from os.path import join as pjoin


def save_detection_json(file_path, texts, img_shape):
    f_out = open(file_path, 'w')
    output = {'img_shape': img_shape, 'texts': []}
    for text in texts:
        c = {'id': text.id, 'content': text.content}
        loc = text.location
        c['column_min'], c['row_min'], c['column_max'], c['row_max'] = loc['left'], loc['top'], loc['right'], loc['bottom']
        c['width'] = text.width
        c['height'] = text.height
        output['texts'].append(c)
    json.dump(output, f_out, indent=4)


def visualize_texts(org_img, texts, shown_resize_height=None, show=False, write_path=None):
    img = org_img.copy()
    for text in texts:
        if isinstance(text, dict) and "position" in text:
            x1, y1, x2, y2 = text["position"]
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, text.get("text", ""), (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        else:
            text.visualize_element(img, line=2)

    img_resize = img
    if shown_resize_height is not None:
        img_resize = cv2.resize(img, (int(shown_resize_height * (img.shape[1]/img.shape[0])), shown_resize_height))

    if show:
        cv2.imshow('texts', img_resize)
        cv2.waitKey(0)
        cv2.destroyWindow('texts')
    if write_path is not None:
        cv2.imwrite(write_path, img)


def text_sentences_recognition(texts):
    changed = True
    while changed:
        changed = False
        temp_set = []
        for text_a in texts:
            merged = False
            for text_b in temp_set:
                if text_a.is_on_same_line(text_b, 'h', bias_justify=0.2 * min(text_a.height, text_b.height), bias_gap=2 * max(text_a.word_width, text_b.word_width)):
                    text_b.merge_text(text_a)
                    merged = True
                    changed = True
                    break
            if not merged:
                temp_set.append(text_a)
        texts = temp_set.copy()

    for i, text in enumerate(texts):
        text.id = i
    return texts


def merge_intersected_texts(texts):
    changed = True
    while changed:
        changed = False
        temp_set = []
        for text_a in texts:
            merged = False
            for text_b in temp_set:
                if text_a.is_intersected(text_b, bias=2):
                    text_b.merge_text(text_a)
                    merged = True
                    changed = True
                    break
            if not merged:
                temp_set.append(text_a)
        texts = temp_set.copy()
    return texts


def text_cvt_orc_format(ocr_result):
    texts = []
    if ocr_result is not None:
        for i, result in enumerate(ocr_result):
            error = False
            x_coordinates = []
            y_coordinates = []
            text_location = result['boundingPoly']['vertices']
            content = result['description']
            for loc in text_location:
                if 'x' not in loc or 'y' not in loc:
                    error = True
                    break
                x_coordinates.append(loc['x'])
                y_coordinates.append(loc['y'])
            if error: continue
            location = {'left': min(x_coordinates), 'top': min(y_coordinates),
                        'right': max(x_coordinates), 'bottom': max(y_coordinates)}
            texts.append(Text(i, content, location))
    return texts


def text_cvt_orc_format_paddle(paddle_result):
    texts = []
    for i, line in enumerate(paddle_result):
        points = np.array(line[0])
        location = {'left': int(min(points[:, 0])), 'top': int(min(points[:, 1])), 'right': int(max(points[:, 0])),
                    'bottom': int(max(points[:, 1]))}
        content = line[1][0]
        texts.append(Text(i, content, location))
    return texts


def text_filter_noise(texts):
    valid_texts = []
    for text in texts:
        if len(text.content) <= 1 and text.content.lower() not in ['a', ',', '.', '!', '?', '$', '%', ':', '&', '+']:
            continue
        valid_texts.append(text)
    return valid_texts


def text_detection(input_file='../data/input/30800.jpg', output_file='../data/output', show=False, method='google', paddle_model=None):
    '''
    :param method: google, paddle ou tesseract (patch perso)
    '''
    start = time.perf_counter()
    name = input_file.split('/')[-1][:-4]
    ocr_root = pjoin(output_file, 'ocr')
    os.makedirs(ocr_root, exist_ok=True)
    img = cv2.imread(input_file)

    if method == 'google':
        ocr_result = ocr.ocr_detection_google(input_file)
    elif method == 'paddle':
        ocr_result = ocr.ocr_detection_paddle(input_file)
    elif method == 'tesseract':
        ocr_result = ocr.ocr_detection_tesseract(input_file)
    else:
        raise ValueError('Method has to be "google", "paddle" or "tesseract"')

    # Conversion vers objets Text
    if method == 'tesseract':
        texts = []
        for i, entry in enumerate(ocr_result):
            location = {
                'left': entry['position'][0],
                'top': entry['position'][1],
                'right': entry['position'][2],
                'bottom': entry['position'][3]
            }
            texts.append(Text(i, entry['text'], location))
    else:
        texts = text_cvt_orc_format(ocr_result)

    visualize_texts(img, texts, shown_resize_height=800, show=show, write_path=pjoin(ocr_root, name+'.png'))
    save_detection_json(pjoin(ocr_root, name+'.json'), texts, img.shape)

    duration = time.perf_counter() - start
    print(f"[Text Detection Completed in {duration:.3f} s] Input: {input_file} Output: {pjoin(ocr_root, name+'.json')}")
