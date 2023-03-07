# from models.emotion import EmotionInference

# ei = EmotionInference.getInstance()

import cv2 
# import numpy as np
# img = cv2.imread("./test/test.png")

# image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# image = cv2.resize(image, (64, 64))

# images = np.expand_dims(image, axis=0)
# list_image = np.array([images, images, images, images, images])
# list_image = list_image.astype(np.float32)
# print(list_image.shape)
# res = ei.predict(list_image)

# print(res)

# Main void

# parser=argparse.ArgumentParser()
# parser.add_argument("-i", "--image", type=str, required=False, help="input image")
# args=parser.parse_args()

img_path = "dependencies/1.jpg"
color = (255, 128, 0)
from models.utralface import LightWeightDetection as lwd

f = lwd.getInstance()

orig_image = cv2.imread(img_path)
import time 
t = time.time()
boxes, labels, probs = f.faceDetector(orig_image)
t2 = time.time()
print(t2 - t)

for box in boxes:
    cv2.rectangle(orig_image, (box[0], box[1]), (box[2], box[3]), color, 4)
    cv2.imshow('img', orig_image)
    cv2.waitKey(1000)
