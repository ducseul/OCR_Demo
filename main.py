import cv2
import numpy as np
import sys
from ocr_core import img2text
import filter_kernel

def mouse_crop(event, x, y, flags, param):
    global x_start, y_start, x_end, y_end, cropping

    if event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True
    # Mouse is Moving

    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping == True:
            x_end, y_end = x, y
    # if the left mouse button was released

    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates
        x_end, y_end = x, y
        cropping = False  # cropping is finished
        refPoint = [(x_start, y_start), (x_end, y_end)]
        if len(refPoint) == 2:  # when two points were found
            roi = oriImage[refPoint[0][1]:refPoint[1][1], 
                refPoint[0][0]:refPoint[1][0]]
            roi = filter_kernel.sharpen_mask(roi)
            roi = cv2.bilateralFilter(roi,9,75,75)
            cv2.imshow("Cropped", roi)
            # print("height: ", str(roi.shape[0]), " width: ", str(roi.shape[1]))
            txt = img2text(roi)
            # print(txt)


if __name__ == '__main__':
    image_path = "sample.jpg"
    try:
        image_path = sys.argv[1]
    except:
        pass

    cropping = False
    x_start, y_start, x_end, y_end = 0, 0, 0, 0
    image = cv2.imread(image_path)

    oriImage = image.copy()

    #create windows for cropping
    cv2.namedWindow("raw_image")
    cv2.setMouseCallback("raw_image", mouse_crop)
    while True:
        i = image.copy()
        if not cropping:
            cv2.imshow("raw_image", image)
        elif cropping:
            cv2.rectangle(i, (x_start, y_start), (x_end, y_end), (255, 0, 0), 2)
            cv2.imshow("raw_image", i)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # close all open windows
    # image.release()
    cv2.destroyAllWindows()