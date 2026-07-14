### Electrical Design Process

#### 1\. Motorization & Power System

###### **1.1 DC Motor Selection**
The DC motor was chosen for its balance of speed and torque, giving the robot enough power to accelerate while staying controllable through turns and obstacle avoidance. It was selected for sufficient torque under load, a compact size that fits the chassis, and efficient power consumption.

<img width="350" alt="dc_motor" src="IMAGE">

---

###### **1.2 Motor Driver: DRV8871**
The **DRV8871** drives the DC motor with the current the ESP32 can't supply directly. It gives PWM-based speed control, forward/reverse direction control, and built-in overcurrent and thermal protection — all in a small enough package for our limited space.

<img width="215" alt="motordriver" src="https://github.com/user-attachments/assets/bf276066-4841-47e8-8bfa-23230064cd28">

---

###### **1.3 Steering Servo: MG90S**
The **MG90S** metal-gear servo handles our Ackermann steering. It offers precise angle control, fast response, and enough torque for the steering mechanism, and its compact size fit our chassis without issue. We'd also used it in past projects, which sped up integration and tuning.

<img width="215" alt="servoimg" src="https://github.com/user-attachments/assets/c92c68c5-6e68-4848-8911-8e2b599aeef9">

---

###### **1.4 Battery Pack**
Power comes from a **12.8V battery pack**, sized to comfortably run all electrical components for a full run without a significant voltage drop.

<img width="350" alt="battery_pack" src="IMAGE">

---

###### **1.5 Buck Converter**
Since our components run at different voltages, a **buck converter** steps the 12.8V battery voltage down to the level each part needs. This protects components from damage and keeps performance consistent throughout operation.

<img width="350" alt="buck_converter" src="IMAGE">

---

#### 2\. Electrical Components

###### **2.1 Main Controller: Raspberry Pi**
The **Raspberry Pi** is our main controller, handling camera input, object and line detection, navigation calculations, and communication with the motor controller.

<img width="220" alt="raspberrypi4bimg" src="https://github.com/user-attachments/assets/0de325c4-8aff-4621-ba53-301a315b03ae">

---

###### **2.2 Motor Controller: ESP32**
An **ESP32** acts as a dedicated motor controller, handling DC motor speed and servo steering, and receiving commands from the Pi over serial communication — keeping motor control isolated from delays caused by image processing.

<img width="210" alt="esp32img" src="https://github.com/user-attachments/assets/75667778-47bf-4933-977f-898c77f49e07">

---

###### **2.3 Camera: Raspberry Pi Camera Module 3 Wide**
The **Raspberry Pi Camera Module 3 Wide** was chosen for its wider field of view, giving the robot better line and object detection coverage during autonomous navigation.

<img width="220" alt="pi_camera_3_wide" src="IMAGE">

---

###### **2.4 Custom PCB**
A custom-designed PCB organizes wiring between components, giving cleaner cable management, reliable connections, a compact fit inside the chassis, and easier debugging.

<img width="450" alt="custom_pcb" src="IMAGE">

---

#### 3\. Electrical Integration
All components are integrated into the final chassis as a compact, reliable system: the Raspberry Pi handles high-level decision-making, while the ESP32 manages real-time motor and steering control.

<img width="600" alt="final_electronics" src="IMAGE">
