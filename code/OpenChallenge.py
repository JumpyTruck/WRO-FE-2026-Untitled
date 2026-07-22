import cv2
import numpy as np
from picamera2 import Picamera2
import serial
import time
from enum import Enum

# =========================
# ARDUINO NANO SERIAL
# =========================
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
time.sleep(2)

# =========================
# MOTOR COMMAND SENTINELS
# =========================
MOTOR_START_CMD = 888
MOTOR_STOP_CMD = 999
LAPS_TARGET = 3  # stop the motor after this many full laps (12 quarter-turns)

# How long (seconds) to keep driving straight AFTER the final turn completes
FINISH_DRIVE_SECONDS = 1.5


def send_motor_start():
    ser.write(f"{MOTOR_START_CMD}\n".encode())
    print("[motor] START sent to ESP32")


def send_motor_stop():
    ser.write(f"{MOTOR_STOP_CMD}\n".encode())
    print("[motor] STOP sent to ESP32")


motor_started = False
race_finished = False

# =========================
# CAMERA  
# =========================
CAMERA_PIC_WIDTH = 640
CAMERA_PIC_HEIGHT = 360
PIC_WIDTH = 640
PIC_HEIGHT = 280

picam2 = Picamera2()

sensor_mode = picam2.sensor_modes[1]
sensor_width, sensor_height = sensor_mode["size"]

config = picam2.create_still_configuration(
    raw={"size": (sensor_width, sensor_height)},
    main={"format": "RGB888", "size": (CAMERA_PIC_WIDTH, CAMERA_PIC_HEIGHT)}
)
picam2.configure(config)
picam2.start()

# small warm-up so the sensor/AWB/AE settle before we trust any frame
# (this is on top of the explicit motor start -- belt and suspenders)
for _ in range(10):
    picam2.capture_array()

# =========================
# PD GAINS
# =========================
Kp = 0.2
Kd = 0.0025
prev_error = 0

# =========================
# TARGET POINT
# =========================
FIRST_TARGET_X = 1
FIRST_TARGET_Y = 220

SECOND_TARGET_X = 1
SECOND_TARGET_Y = 280

ORIGINAL_TARGET_X_LEFT = 70
ORIGINAL_TARGET_X_RIGHT = 570
ORIGINAL_TARGET_Y = PIC_HEIGHT - 1

# =========================
# WALL BRIGHTNESS THRESHOLD 
# =========================
GRAY_THRESHOLD = 100

# =========================
# POLYGON MARGIN
# =========================
POLYGON_MARGIN_PX = 20

# =========================================================================
# COLOR MASKS
# =========================================================================
BLUE_LOWER = np.array([82, 0, 61])
BLUE_UPPER = np.array([118, 255, 255])
ORANGE_LOWER = np.array([0, 18, 92])
ORANGE_UPPER = np.array([19, 255, 255])


def blue_mask_of(hsv_img):
    return cv2.inRange(hsv_img, BLUE_LOWER, BLUE_UPPER)


def orange_mask_of(hsv_img):
    return cv2.inRange(hsv_img, ORANGE_LOWER, ORANGE_UPPER)


# =========================================================================
# DIRECTION DETECTION
# =========================================================================
class Direction(Enum):
    LEFT = -1
    RIGHT = 1


def line_length(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return 0.0
    largest = max(contours, key=cv2.contourArea)
    (_, _), (rw, rh), _ = cv2.minAreaRect(largest)
    return max(rw, rh)


def detect_initial_direction(hsv_img, polygon_mask):
    blue_line = cv2.bitwise_and(blue_mask_of(hsv_img), blue_mask_of(hsv_img), mask=polygon_mask)
    orange_line = cv2.bitwise_and(orange_mask_of(hsv_img), orange_mask_of(hsv_img), mask=polygon_mask)

    blue_len = line_length(blue_line)
    orange_len = line_length(orange_line)
    print(f"[direction calibration] blue_len={blue_len:.1f}  orange_len={orange_len:.1f}")

    # TODO: verify this ternary matches reality on your mat -- flip it if backwards
    return Direction.LEFT if blue_len > orange_len else Direction.RIGHT


direction = None  # set once the first frame's polygon is available


LAP_TURN_DEBOUNCE_SECONDS = 2.0
last_turn_time = 0.0
quarter_lap_count = 0
lap_count = 0

# =========================================================================
# FINAL-LAP FINISH STATE MACHINE
# =========================================================================
final_lap_triggered = False
finishing = False
finish_start_time = None


def register_corner_turn():
    global last_turn_time, quarter_lap_count, lap_count, final_lap_triggered
    now = time.time()

    if now - last_turn_time > LAP_TURN_DEBOUNCE_SECONDS:
        quarter_lap_count += 1
        if quarter_lap_count % 4 == 0:
            lap_count += 1
            print(f"[laps] lap {lap_count} complete")

        if lap_count >= LAPS_TARGET and not final_lap_triggered:
            final_lap_triggered = True
            print("[laps] final corner detected -- will finish this turn, then coast to a stop")

        last_turn_time = now


Y_CORNER_THRESHOLD = 155
Y_DROP_THRESHOLD = 25

prev_y_for_corner = None
in_corner = False


def update_corner_state(y):
    """Returns (corner_active, just_entered, just_exited)."""
    global prev_y_for_corner, in_corner

    if prev_y_for_corner is None:
        prev_y_for_corner = y
        return False, False, False

    dy = prev_y_for_corner - y
    just_entered = False
    just_exited = False

    if not in_corner:

        if y <= Y_CORNER_THRESHOLD and dy > Y_DROP_THRESHOLD:
            in_corner = True
            just_entered = True

    else:

        if y > Y_CORNER_THRESHOLD:
            in_corner = False
            just_exited = True

    prev_y_for_corner = y

    return in_corner, just_entered, just_exited


def send_angle(angle):
    ser.write((str(angle) + "\n").encode())
    ser.flush()


def crop_image(img, x_start, x_end, y_start, y_end):
    return img[y_start:y_end, x_start:x_end]


prevang = None

while True:
    raw_frame = picam2.capture_array()

    frame = crop_image(
        raw_frame,
        0, CAMERA_PIC_WIDTH,
        CAMERA_PIC_HEIGHT - PIC_HEIGHT, CAMERA_PIC_HEIGHT
    )

    #frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    h, w = frame.shape[:2]
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # =========================
    # STEP 1: GRAYSCALE + BLUR 
    # =========================
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)

    # =========================
    # STEP 2: BINARY THRESHOLD 
    # =========================
    _, binary = cv2.threshold(blurred, GRAY_THRESHOLD, 255, cv2.THRESH_BINARY)

    # force blue/orange lines to read as FLOOR (white) before cleanup
    line_mask = cv2.bitwise_or(blue_mask_of(hsv), orange_mask_of(hsv))
    binary[line_mask > 0] = 255

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

    if direction is None:
        direction = detect_initial_direction(hsv, polygon_mask)
        print(f"Direction locked: {direction.name}")

        # camera pipeline is confirmed working and we know which way to
        # steer -- only NOW is it safe to let the motor spin.
        if not motor_started:
            send_motor_start()
            motor_started = True

        continue

    # =========================================================================
    # POINT-TRACKING / PD LOGIC -- direction picks which half of the frame
    # =========================================================================
    if direction == Direction.LEFT:
        side_mask_source = np.zeros_like(polygon_image)
        side_mask_source[:, :w // 2] = polygon_image[:, :w // 2]
        side_wall_white = cv2.bitwise_not(side_mask_source)
        side_wall_white = cv2.bitwise_and(side_wall_white, side_wall_white, mask=polygon_mask)
        side_wall_white[:, w // 2:] = 0
    else:
        side_mask_source = np.zeros_like(polygon_image)
        side_mask_source[:, w // 2:] = polygon_image[:, w // 2:]
        side_wall_white = cv2.bitwise_not(side_mask_source)
        side_wall_white = cv2.bitwise_and(side_wall_white, side_wall_white, mask=polygon_mask)
        side_wall_white[:, :w // 2] = 0

    contours2, _ = cv2.findContours(side_wall_white, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    angle = 100
    wall_pixel_count = cv2.countNonZero(side_wall_white)

    if len(contours2) > 0:
        points = np.concatenate(contours2)
        xs = points[:, 0, 0]
        ys = points[:, 0, 1]

        if direction == Direction.LEFT:
            valid = xs < w // 2
        else:
            valid = xs >= w // 2
        xs = xs[valid]
        ys = ys[valid]

        if len(xs) > 0:
            max_y = np.max(ys)
            bottom = ys == max_y
            xs_b = xs[bottom]
            ys_b = ys[bottom]

            if direction == Direction.LEFT:
                idx = np.argmax(xs_b)   # lowest, leftmost-half point -> as far right as the wall reaches
            else:
                idx = np.argmax(xs_b)   # lowest, rightmost-half point -> as far right as the wall reaches (x max, y max)
            x = xs_b[idx]
            y = ys_b[idx]

            # ---------------------------------------
            # Dynamic target point based on quarter
            # ---------------------------------------
            if quarter_lap_count == 0:
                # Before first turn
                if direction == Direction.LEFT:
                    target_x = FIRST_TARGET_X
                    Kp = 0.1
                    Kd = 0.0015
                else:
                    target_x = w - FIRST_TARGET_X
                target_y_use = FIRST_TARGET_Y

            elif quarter_lap_count == 1:
                # After first turn
                if direction == Direction.LEFT:
                    target_x = SECOND_TARGET_X
                    Kp = 0.13
                    Kd = 0.0015
                else:
                    target_x = w - SECOND_TARGET_X
                target_y_use = SECOND_TARGET_Y

            else:
                # After second turn onwards
                if direction == Direction.LEFT:
                    target_x = ORIGINAL_TARGET_X_LEFT
                    Kp = 0.2
                    Kd = 0.0025
                else:
                    target_x = ORIGINAL_TARGET_X_RIGHT
                target_y_use = ORIGINAL_TARGET_Y

            cv2.circle(frame, (x, y), 8, (0, 0, 255), -1)
            cv2.circle(frame, (target_x, target_y_use), 8, (0, 255, 0), -1)

            if direction == Direction.LEFT:
                error_x = target_x - x
            else:
                error_x = x - target_x

            error_y = target_y_use - y
            error = error_x + error_y

            derivative = error - prev_error
            control = (Kp * error) + (Kd * derivative)
            prev_error = error

            turn_sign = 1 if direction == Direction.LEFT else -1

            corner_active, corner_just_started, corner_just_exited = update_corner_state(y)

            if corner_active:
                angle = 140 if direction == Direction.LEFT else 50

                if corner_just_started:
                    register_corner_turn()

            else:
                angle = 110 + turn_sign * control
         #       angle = max(108, min(112, angle))

            # ---------------------------------------------------------------
            # FINAL-LAP FINISH HANDLING
            # ---------------------------------------------------------------
            if corner_just_exited and final_lap_triggered and not finishing:
                finishing = True
                finish_start_time = time.time()
                print("[laps] final turn complete -- wall-following for a bit before stopping")

            angle = round(angle)
            if prevang is None or prevang != angle:
                send_angle(angle)
                #time.sleep(0.02)
                prevang = angle
            print(
                f"X:{x}, "
                f"Y:{y}, "
                f"error:{error:.2f}, "
                f"angle:{angle}, "
                f"in_corner:{in_corner}, "
                f"quarterlaps:{quarter_lap_count}, "
                f"laps:{lap_count}, "
                f"finishing:{finishing}"
            )

            # once we've finished coasting long enough after the final turn,
            # stop the motor and end the run.
            if finishing and (time.time() - finish_start_time >= FINISH_DRIVE_SECONDS):
                print(f"[race] {LAPS_TARGET} laps complete -- motor stopped, ending run")
                send_motor_stop()
                race_finished = True
                break

    # ---- display lap info on the frame
    cv2.putText(frame, f"Laps: {lap_count}  Quarters: {quarter_lap_count}",
                (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("frame", frame)
    cv2.imshow("wall mask (side)", side_wall_white)
    cv2.imshow("polygon mask", polygon_mask)
    cv2.imshow("polygon image (wall=black, floor=white)", polygon_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# make sure the motor is off no matter how we exited the loop
if not race_finished:
    send_motor_stop()

picam2.stop()
cv2.destroyAllWindows()
ser.close()
