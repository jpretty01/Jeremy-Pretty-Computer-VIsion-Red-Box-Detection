import cv2
import numpy as np
import pyautogui
from PIL import Image
from PIL import ImageDraw
import time
import os

def detect_blue(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([100, 150, 50])
    upper_blue = np.array([130, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rects = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        rects.append((x, y, w, h))

    return rects

def save_screenshot_with_box(image, rects):
    img = Image.fromarray(image)
    draw = ImageDraw.Draw(img)

    for rect in rects:
        x, y, w, h = rect
        draw.rectangle([x, y, x + w, y + h], outline='red', width=2)

    timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
    save_path = os.path.join("screenshots", f"{timestamp}.png") 

    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    img.save(save_path)

while True:
    screenshot = pyautogui.screenshot()
    image = np.array(screenshot)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    rects = detect_blue(image)

    if rects:
        save_screenshot_with_box(image, rects)
        print("Screenshot saved.")

        user_input = input("Press 'q' to quit or any other key to continue monitoring: ")

        if user_input.lower() == 'q':
            break

    time.sleep(1)  # Adjust the time interval between consecutive screenshots (in seconds)
