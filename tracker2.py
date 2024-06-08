# import matplotlib.pyplot as plt
# import numpy as np
# import cv2

# image = cv2.imread('s2.png')
# template = cv2.imread('o.png')
# heat_map = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

# h, w, _ = template.shape
# y, x = np.unravel_index(np.argmax(heat_map), heat_map.shape)
# cv2.rectangle(image, (x,y), (x+w, y+h), (0,0,255), 5)

# plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

import cv2
import numpy as np

img_rgb = cv2.imread('s2.png')
template = cv2.imread('o.png')
w, h = template.shape[:-1]

res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
threshold = .8
loc = np.where(res >= threshold)
for pt in zip(*loc[::-1]):  # Switch columns and rows
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

cv2.imwrite('result.png', img_rgb)

# cv2.waitKey(0)