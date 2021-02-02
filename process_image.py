import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import math
from keras.models import load_model

# loading pre trained model
model = load_model('digit_classifier.h5')

# predicting the digit that we have drawn
def predict_digit(img):
    test_image = img.reshape(-1, 28, 28, 1)
    return np.argmax(model.predict(test_image))


# putting label
def put_label(t_img, label, x, y):
    # https://www.geeksforgeeks.org/python-opencv-cv2-puttext-method/
    # https: // www.geeksforgeeks.org / python - opencv - cv2 - rectangle - method /
    font = cv2.FONT_HERSHEY_TRIPLEX
    l_x = int(x) - 10
    l_y = int(y) + 10
    cv2.rectangle(t_img, (l_x, l_y + 5), (l_x + 35, l_y - 35), (255, 0, 0), -1)
    cv2.putText(t_img, str(label), (l_x, l_y), font, 1.5, (0, 0, 0), 1, cv2.LINE_AA)
    return t_img


# refining each digit
def image_refiner(gray):
    # https://www.pyimagesearch.com/2014/01/20/basic-image-manipulations-in-python-and-opencv-resizing-scaling-rotating-and-cropping/
    org_size = 22
    img_size = 28
    rows, cols = gray.shape
    # mainting the aspect ratio
    if rows > cols:
        factor = org_size / rows
        rows = org_size
        cols = int(round(cols * factor))
    else:
        factor = org_size / cols
        cols = org_size
        rows = int(round(rows * factor))
    gray = cv2.resize(gray, (cols, rows))

    # get padding
    colsPadding = (int(math.ceil((img_size - cols) / 2.0)), int(math.floor((img_size - cols) / 2.0)))
    rowsPadding = (int(math.ceil((img_size - rows) / 2.0)), int(math.floor((img_size - rows) / 2.0)))

    # apply apdding
    # https://www.geeksforgeeks.org/numpy-pad-function-in-python/#:~:text=pad()%20function%20is%20used,will%20increase%20according%20to%20pad_width.
    gray = np.lib.pad(gray, (rowsPadding, colsPadding), 'constant')
    return gray


def get_output_image(path):
    # https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_contours/py_contours_begin/py_contours_begin.html
    # https: // www.geeksforgeeks.org / enumerate - in -python /
    img = cv2.imread(path, 0)

    img_org = cv2.imread(path)

    ret, thresh = cv2.threshold(img, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    # https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_contours/py_contour_features/py_contour_features.html
    for j, cnt in enumerate(contours):

        x, y, w, h = cv2.boundingRect(cnt)
      # not equal tp -1 because we are not interested in outermost countour i.e. the border
        if (hierarchy[0][j][3] != -1 and w > 10 and h > 10):
            # putting boundary on each digit
            cv2.rectangle(img_org, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # cropping each image and process
            roi = img[y:y + h, x:x + w]
            roi = cv2.bitwise_not(roi)

            roi = image_refiner(roi)
           # th, fnl = cv2.threshold(roi, 127, 255, cv2.THRESH_BINARY)

            # getting prediction of cropped image
            pred = predict_digit(roi)
            print(pred)

            # placing label on each digit
           # (x, y), radius = cv2.minEnclosingCircle(cnt)
            img_org = put_label(img_org, pred, x, y)

    return img_org