import cv2
import numpy as np
from picamera2 import Picamera2
import serial
import time

# =========================
# ESP32 SERIAL
# =========================
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
time.sleep(2)

# =========================
# CAMERA 
# =========================
CAMERA_PIC_WIDTH = 640     # output frame width  
CAMERA_PIC_HEIGHT = 360    # output frame height 
PIC_WIDTH = 640            # width AFTER crop 
PIC_HEIGHT = 280           # height AFTER crop 

picam2 = Picamera2()


sensor_mode = picam2.sensor_modes[1]           
sensor_width, sensor_height = sensor_mode["size"]

config = picam2.create_still_configuration(
    raw={"size": (sensor_width, sensor_height)},   
    main={"format": "RGB888", "size": (CAMERA_PIC_WIDTH, CAMERA_PIC_HEIGHT)}
)
picam2.configure(config)
picam2.start()

# =========================
# PD GAINS 
# =========================
Kp = 0.15
Kd = 0
prev_error = 0

# =========================
# TARGET POINT (fixed)
# =========================
target_x = 0
target_y = PIC_HEIGHT - 1

# =========================
# WALL BRIGHTNESS THRESHOLD
# grayscale value below this = wall (dark). Above = floor (bright).
# =========================
GRAY_THRESHOLD = 50

# =========================
# POLYGON MARGIN
# =========================
POLYGON_MARGIN_PX = 20

def send_angle(angle):
    ser.write(f"{angle}\n".encode())


def crop_image(img, x_start, x_end, y_start, y_end):
    # same signature/behavior as the repo's ImageTransformUtils.crop_image
    return img[y_start:y_end, x_start:x_end]


prevang = None

while True:
    raw_frame = picam2.capture_array()

    # =========================
    # CROP TOP OF FRAME (matches repo's transform_image() crop step)
    # crops from y = CAMERA_PIC_HEIGHT - PIC_HEIGHT (80) down to
    # CAMERA_PIC_HEIGHT (360), keeping full width -> drops the top 80px
    # =========================
    frame = crop_image(
        raw_frame,
        0, CAMERA_PIC_WIDTH,
        CAMERA_PIC_HEIGHT - PIC_HEIGHT, CAMERA_PIC_HEIGHT
    )

    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    h, w = frame.shape[:2]   # now (280, 640) instead of (360, 640)

    # =========================
    # STEP 1: GRAYSCALE + BLUR
    # =========================
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)

    # =========================
    # STEP 2: BINARY THRESHOLD
    # =========================
    _, binary = cv2.threshold(blurred, GRAY_THRESHOLD, 255, cv2.THRESH_BINARY)

    # =========================
    # STEP 3: CLEAN UP NOISE
    # =========================
    kernel = np.ones((5, 5), np.uint8)
    clean = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    # =========================
    # STEP 4: DYNAMIC POLYGON MASK
    # =========================
    contours, _ = cv2.findContours(clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    polygon_mask = np.zeros_like(clean)

    if len(contours) > 0:
        largest = max(contours, key=cv2.contourArea)
        epsilon = 0.003 * cv2.arcLength(largest, True)
        polygon_points = cv2.approxPolyDP(largest, epsilon, True)

        cv2.fillPoly(polygon_mask, [polygon_points], 255)

        dilate_kernel = np.ones((POLYGON_MARGIN_PX, POLYGON_MARGIN_PX), np.uint8)
        polygon_mask = cv2.dilate(polygon_mask, dilate_kernel)

        cv2.polylines(frame, [polygon_points], True, (0, 0, 255), 2)

    # =========================
    # STEP 5: APPLY THE POLYGON MASK
    # =========================
    polygon_image = cv2.bitwise_and(clean, clean, mask=polygon_mask)

    # =========================
    # WALL FOLLOW LOGIC
    # =========================
    left_mask_source = np.zeros_like(polygon_image)
    left_mask_source[:, :w // 2] = polygon_image[:, :w // 2]

    left_wall_white = cv2.bitwise_not(left_mask_source)
    left_wall_white = cv2.bitwise_and(left_wall_white, left_wall_white, mask=polygon_mask)
    left_wall_white[:, w // 2:] = 0

    contours2, _ = cv2.findContours(left_wall_white, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    angle = 100  # servo output, default center

    wall_pixel_count = cv2.countNonZero(left_wall_white)

    if len(contours2) > 0:
        points = np.concatenate(contours2)
        xs = points[:, 0, 0]
        ys = points[:, 0, 1]

        valid = xs < w // 2
        xs = xs[valid]
        ys = ys[valid]

        if len(xs) > 0:
            max_y = np.max(ys)
            bottom = ys == max_y
            xs_b = xs[bottom]
            ys_b = ys[bottom]
            idx = np.argmax(xs_b)
            x = xs_b[idx]
            y = ys_b[idx]

            cv2.circle(frame, (x, y), 8, (0, 0, 255), -1)
            cv2.circle(frame, (target_x, target_y), 8, (0, 255, 0), -1)

            error_x = target_x - x
            error_y = target_y - y
            error = error_x + error_y

            derivative = error - prev_error
            control = (Kp * error) + (Kd * derivative)
            prev_error = error

            if y > 130: # if y less than 130, wall follow, else, turn left
                angle = 100 + control
            else:
                angle = 125

            angle = round(angle)
            if prevang is None or abs(angle - prevang) >= 3:
                send_angle(angle)
                time.sleep(0.02)
                prevang = angle

            print(f"X:{x}, Y:{y} | error:{error:.2f} | angle:{angle} | wall_px:{wall_pixel_count}")

    cv2.imshow("frame", frame)
    cv2.imshow("wall mask (left half)", left_wall_white)
    cv2.imshow("polygon mask", polygon_mask)
    cv2.imshow("polygon image (wall=black, floor=white)", polygon_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

picam2.stop()
cv2.destroyAllWindows()
ser.close()
