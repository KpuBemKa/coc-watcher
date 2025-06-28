import pyautogui
import cv2
import time

import numpy as np

from pynput import keyboard
from pynput import mouse

def get_pixel_color_and_position():
    x, y = pyautogui.position()
    screenshot = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    b, g, r = image[y, x]
    print(f"F7 pressed! Mouse at ({x}, {y}) — Pixel color (BGR): ({b}, {g}, {r})")

def on_press(key):
    if key == keyboard.Key.f6:
        mouse_controller = mouse.Controller()
        (x, y) = mouse_controller.position
        mouse_controller.position = (x - 200, y)
        
    if key == keyboard.Key.f7:
        get_pixel_color_and_position()

# Start the listener in a try/except to handle Ctrl+C
print("Listening for F7... Press Ctrl+C to quit.")
keyboard.Listener(on_press=on_press).start()
    
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nExiting on Ctrl+C.")
