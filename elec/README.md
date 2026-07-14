# Electrical Design Process

This section outlines the electrical systems used in our WRO Future Engineers robot. The electronics were designed to provide reliable motor control, accurate sensor data, and efficient communication between the different systems.

---

# 1. Motorization & Power System Design

Before designing the electrical system, we analyzed the power requirements of each component to ensure reliable operation. The motorization system was designed to provide enough torque, precise control, and efficient power usage for autonomous driving.

---

## 1.1 DC Motor Selection

The DC motor was selected based on the required balance between speed and torque for our robot. The motor provides enough power to accelerate the robot while maintaining precise control during turns and obstacle avoidance.

Key considerations:
- Sufficient torque for acceleration
- Reliable performance under load
- Compact size to fit within the chassis
- Efficient power consumption

<img width="350" alt="dc_motor" src="IMAGE">

---

## 1.2 Motor Driver - DRV8871

We chose the **DRV8871 motor driver** because it provides reliable control of our DC motor while handling the higher current requirements that cannot be supplied directly by the ESP32. Its compact size, built-in protection features, and efficient PWM control make it suitable for our robot's limited space and precise autonomous movement.

The motor driver provides:
- High current output for the DC motor
- PWM-based speed control
- Direction control for forward and reverse movement
- Overcurrent and thermal protection for improved reliability

<img width="215" height="215" alt="motordriver" src="https://github.com/user-attachments/assets/bf276066-4841-47e8-8bfa-23230064cd28" />

---

## 1.3 Steering Servo

A servo motor was used for the front Ackermann steering system because it provides accurate position control and allows precise steering adjustments during autonomous driving.

The servo was selected for:
- Precise angle control
- Fast response time
- Compatibility with the steering mechanism
- Reliable operation during repeated turns

<img width="350" alt="servo" src="IMAGE">

---

## 1.4 Battery & Voltage Regulation

Our robot uses a **12.8V battery pack** as the main power source. Since the electrical components require different operating voltages, a **buck converter** was implemented to step down the battery voltage to appropriate levels.

The voltage requirements of each component were calculated to ensure safe and stable operation.

The buck converter helps:
- Provide correct voltage to each component
- Prevent electrical damage
- Improve power efficiency
- Maintain consistent performance during operation

<img width="450" alt="buck_converter" src="IMAGE">

---

## 2. Electrical Components

### 2.1 Main Controller — Raspberry Pi

The Raspberry Pi was selected as the main controller because it provides enough processing power for real-time image processing, computer vision, and autonomous decision making.

It handles:
- Camera processing
- Object and line detection
- Navigation calculations
- Communication with the motor controller

<img width="218.3" height="156" alt="raspberrypi4bimg" src="https://github.com/user-attachments/assets/0de325c4-8aff-4621-ba53-301a315b03ae" />

---

### 2.2 Motor Controller — ESP32

An ESP32 was used as a dedicated motor controller to handle low-level hardware control. Separating motor control from the Raspberry Pi allows smoother operation and prevents delays caused by intensive image processing.

The ESP32 is responsible for:
- DC motor speed control
- Servo steering control
- Receiving commands from the Raspberry Pi through serial communication

<img width="210" height="168" alt="esp32img" src="https://github.com/user-attachments/assets/75667778-47bf-4933-977f-898c77f49e07" />

---

### 2.3 Custom PCB

A custom PCB was designed to organize and simplify the wiring between the different electrical components.

The PCB provides:
- Cleaner cable management
- Reliable connections
- Compact placement inside the chassis
- Easier debugging and maintenance

<img width="450" alt="custom_pcb" src="IMAGE">

---

## 3. Electrical Integration

All electrical components were integrated into the final chassis design to create a compact and reliable system. The Raspberry Pi handles high-level decision making, while the ESP32 manages real-time motor and steering control.

<img width="600" alt="final_electronics" src="IMAGE">
