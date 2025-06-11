import cv2
import numpy as np

# Load images
template = cv2.imread("./static/elixir-cart-cropped.png", 0)
# img2 = cv2.imread('./static/whole_empty_partial-2.png', 0)
scene = cv2.imread("./static/whole_empty_partial-1.png", 0)

sift = cv2.SIFT_create()
kp1, des1 = sift.detectAndCompute(template, None)
kp2, des2 = sift.detectAndCompute(scene, None)

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

    # Draw polygon
    scene_color = cv2.cvtColor(scene, cv2.COLOR_GRAY2BGR)
    cv2.polylines(scene_color, [np.int32(projected)], True, (0, 255, 0), 3, cv2.LINE_AA)

    # Get center of the detected object
    center_x = int(np.mean(projected[:, 0, 0]))
    center_y = int(np.mean(projected[:, 0, 1]))
    print(f"Object center: ({center_x}, {center_y})")

    # Optional: mark center
    cv2.circle(scene_color, (center_x, center_y), 5, (0, 0, 255), -1)

    # Show result
    cv2.imshow("Detected", scene_color)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

else:
    print("Not enough good matches found.")
