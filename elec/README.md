# Electrical Design Process

This section outlines the electrical systems used in our WRO Future Engineers robot. The electronics were designed to provide reliable motor control, accurate sensor data, and efficient communication between the different systems.

---

## 1. Electrical Components

### 1.1 Main Controller — Raspberry Pi

The Raspberry Pi was selected as the main controller because it provides enough processing power for real-time image processing, computer vision, and autonomous decision making.

It handles:
- Camera processing
- Object and line detection
- Navigation calculations
- Communication with the motor controller

<img width="655" height="468" alt="raspberrypi4bimg" src="https://github.com/user-attachments/assets/0de325c4-8aff-4621-ba53-301a315b03ae" />

---

### 1.2 Motor Controller — ESP32

An ESP32 was used as a dedicated motor controller to handle low-level hardware control. Separating motor control from the Raspberry Pi allows smoother operation and prevents delays caused by intensive image processing.

The ESP32 is responsible for:
- DC motor speed control
- Servo steering control
- Receiving commands from the Raspberry Pi through serial communication

<img width="350" height="280" alt="esp32img" src="https://github.com/user-attachments/assets/75667778-47bf-4933-977f-898c77f49e07" />

---

### 1.3 Custom PCB

A custom PCB was designed to organize and simplify the wiring between the different electrical components.

The PCB provides:
- Cleaner cable management
- Reliable connections
- Compact placement inside the chassis
- Easier debugging and maintenance

<img width="450" alt="custom_pcb" src="IMAGE">

---

### 1.4 Power Distribution

The power system was designed to provide stable power delivery to all components while maintaining efficient use of space.

The battery supplies power to:
- DC motors
- ESP32
- Raspberry Pi
- Sensors and peripherals

The power layout was designed to reduce wiring complexity and maintain balanced weight distribution within the chassis.

<img width="450" alt="power_system" src="IMAGE">

---

## 2. Electrical Integration

All electrical components were integrated into the final chassis design to create a compact and reliable system. The Raspberry Pi handles high-level decision making, while the ESP32 manages real-time motor and steering control.

<img width="600" alt="final_electronics" src="IMAGE">
