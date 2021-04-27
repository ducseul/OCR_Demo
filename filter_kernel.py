import cv2
import numpy as np

def unsharp_mask(image, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=0):
    """Return a sharpened version of the image, using an unsharp mask."""
    blurred = cv2.GaussianBlur(image, kernel_size, sigma)
    sharpened = float(amount + 1) * image - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)
    if threshold > 0:
        low_contrast_mask = np.absolute(image - blurred) < threshold
        np.copyto(sharpened, image, where=low_contrast_mask)
    return sharpened

def sharpen_mask(image):
    # filter = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    filter = np.array([[0, -1, 0],[-1, 5, -1],[0, -1, 0]])
# Applying cv2.filter2D function on our Logo image
    sharpen_img_2=cv2.filter2D(image,-1,filter)
    return image

def simpleKernel(roi):
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    roi = cv2.filter2D(roi, -1, kernel)
    return roi

