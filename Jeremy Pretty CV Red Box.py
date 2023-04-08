import cv2
import numpy as np
from PIL import ImageGrab
import datetime
import os

red_scalar = 200

# set up folder to store screenshots
if not os.path.exists('screenshots'):
    os.makedirs('screenshots')

while True:
    # capture full screen
    img = ImageGrab.grab()
    img_np = np.array(img)
    frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

    # define color ranges for red
    lower_red = np.array([0, 0, red_scalar])
    upper_red = np.array([100, 100, 255])

    # detect red objects and draw bounding boxes
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    red_mask = cv2.inRange(blurred, lower_red, upper_red)
    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (128, 128, 128), 2)

    # save screenshot with timestamp as filename
    now = datetime.datetime.now()
    filename = 'screenshots/{}.png'.format(now.strftime('%Y-%m-%d_%H-%M-%S'))
    cv2.imwrite(filename, frame)

    # display screenshot
    cv2.imshow('Screenshot', frame)

    # press 'q' to quit
    if cv2.waitKey(1) == ord('q'):
        break


cv2.destroyAllWindows()
