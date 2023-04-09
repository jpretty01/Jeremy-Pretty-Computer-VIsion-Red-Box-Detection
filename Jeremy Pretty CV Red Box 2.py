import cv2
import numpy as np
import pyautogui
from PIL import Image
from PIL import ImageDraw
import time
import os

# Function to detect the gray color and return the coordinates and dimensions of the detected gray area
def detect_gray(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rects = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        rects.append((x, y, w, h))

    return rects

# Function to save the screenshot with a red box around the gray area
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

    rects = detect_gray(image)

    if rects:
        save_screenshot_with_box(image, rects)

    time.sleep(1)  # Adjust the time interval between consecutive screenshots (in seconds)
