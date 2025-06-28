import time
import random
from traceback import format_exc

import cv2
import numpy as np
from pyautogui import screenshot as pygui_screenshot
from pynput.mouse import Button as MouseButton
from pynput.keyboard import Key

from human_cursor import SystemCursor
from .pynput_singleton import MouseControllerSingleton, KeyboardControllerSingleton
from .datas import Position, Color

__MOUSE_CONTROLLER = MouseControllerSingleton()
__MOUSE_CURSOR = SystemCursor()
__KEYBOARD = KeyboardControllerSingleton()


def is_mouse_inside_box(pos_x, pos_y, width, height):
    (x, y) = __MOUSE_CONTROLLER.position
    # print(pos_x, pos_y, width, height, x, y)
    return (x >= pos_x and x <= pos_x + width) and (y >= pos_y and y <= pos_y + height)


def click_with_randomization(position: Position, mouse_button: MouseButton) -> None:
    randomized_pos = randomize_position(position)

    move_mouse(randomized_pos)

    __MOUSE_CONTROLLER.press(mouse_button)
    random_sleep(0.1, max_delta=0.2)
    __MOUSE_CONTROLLER.release(mouse_button)


def move_mouse(position: Position) -> None:
    __MOUSE_CURSOR.move_to((position.x, position.y), steady=True)


def randomize_position(
    input: Position, offset_x: int | None = None, offset_y: int | None = None
) -> Position:
    dX = offset_x if offset_x is not None else input.max_dX
    dY = offset_y if offset_y is not None else input.max_dY

    return Position(
        input.x + int(random.uniform(-dX, dX)),
        input.y + int(random.uniform(-dY, dY)),
        input.max_dX,
        input.max_dY,
    )


def press_key_with_randomization(key: Key | str):
    __KEYBOARD.press(key)
    random_sleep(0.1, 0.2)
    __KEYBOARD.release(key)


def get_color_in_position(pos: Position, region_size=3) -> Color:
    half = region_size // 2
    left = pos.x - half
    top = pos.y - half

    # Screenshot only the small region
    screenshot = pygui_screenshot(region=(left, top, region_size, region_size))

    # Convert to OpenCV BGR
    image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    return Color.from_tuple(image[half, half])


def is_object_on_screen(object_template_path: str) -> bool:
    try:
        # Take a screenshot with pyautogui
        screen_shot = pygui_screenshot()

        # Convert to OpenCV format (numpy array with BGR color channels)
        screen_cv = cv2.cvtColor(np.array(screen_shot), cv2.COLOR_RGB2BGR)

        # Convert to grayscale (what SIFT expects)
        screen_gray = cv2.cvtColor(screen_cv, cv2.COLOR_BGR2GRAY)

        template = cv2.imread(object_template_path, 0)

        sift = cv2.SIFT_create()
        kp1, des1 = sift.detectAndCompute(template, None)
        kp2, des2 = sift.detectAndCompute(screen_gray, None)

        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)
        
        if not matches:
            return False

        # Apply ratio test to filter good matches
        good = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good.append(m)

        return len(good) > 10
    
    except cv2.error as ex:
        print(f"{ex}\n{format_exc()}")
        return False


def find_object_on_screen(object_template_path: str) -> Position | None:
    # Take a screenshot with pyautogui
    screen_shot = pygui_screenshot()

    # Convert to OpenCV format (numpy array with BGR color channels)
    screen_cv = cv2.cvtColor(np.array(screen_shot), cv2.COLOR_RGB2BGR)

    # Convert to grayscale (what SIFT expects)
    screen_gray = cv2.cvtColor(screen_cv, cv2.COLOR_BGR2GRAY)

    template = cv2.imread(object_template_path, 0)

    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(template, None)
    kp2, des2 = sift.detectAndCompute(screen_gray, None)

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # Apply ratio test to filter good matches
    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append(m)

    if len(good) > 10:
        # Get matched keypoint positions
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        # Compute homography matrix
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        # Get the corners of the template image
        h, w = template.shape
        corners = np.float32([[0, 0], [w, 0], [w, h], [0, h]]).reshape(-1, 1, 2)

        # Project the corners into the scene
        projected = cv2.perspectiveTransform(corners, M)

        # Get bounding box around projected corners
        x, y, w, h = cv2.boundingRect(projected)

        # Calculate center point
        center_x = x + w // 2
        center_y = y + h // 2

        return Position(center_x, center_y, w // 2, h // 2)

        # # Draw polygon
        # scene_color = cv2.cvtColor(scene, cv2.COLOR_GRAY2BGR)
        # cv2.polylines(scene_color, [np.int32(projected)], True, (0, 255, 0), 3, cv2.LINE_AA)

        # # Get center of the detected object
        # center_x = int(np.mean(projected[:, 0, 0]))
        # center_y = int(np.mean(projected[:, 0, 1]))
        # print(f"Object center: ({center_x}, {center_y})")

        # # Optional: mark center
        # cv2.circle(scene_color, (center_x, center_y), 5, (0, 0, 255), -1)

        # # Show result
        # cv2.imshow("Detected", scene_color)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    else:
        # print("Not enough good matches found.")
        return None


def random_sleep(sleep_time: float, max_delta: float | None = None) -> None:
    if max_delta is None:
        max_delta = sleep_time * 2

    randomize = random.uniform(0, max_delta)
    # print(f"Random offset: {randomize}")

    time.sleep(sleep_time + randomize)
