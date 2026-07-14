# Mechanical Design Process

This section outlines the main mechanical decisions made during the development of our WRO Future Engineers robot. Each component was designed and tested to improve reliability, stability, and performance.

---

## 1. Mechanical Design Choices

### 1.1 Wheel Selection

We chose **SPIKE Prime wheels (56mm diameter, 14mm thickness)** because their size provides the ideal balance between speed, torque, and stability. They are compact enough to maintain a lightweight design while still providing sufficient grip and clearance for reliable movement on the WRO mat.

<img width="280" height="187" alt="spike_wheels" src="https://github.com/user-attachments/assets/873b32bb-68e5-45ca-adc8-cf2fd2dda6f8" />

---

### 1.2 Steering System

**Previous Design — Parallel Beam Steering**

Our previous design used a parallel beam steering mechanism. However, both wheels turned at the same angle, causing drifting because the inner and outer wheels followed different turning paths.

<img width="3024" height="4032" alt="VHRsteering" src="https://github.com/user-attachments/assets/73cccba8-f506-4c5d-ad07-ef9bd6d4d4c9" />

**Final Design — Ackermann Steering**

To improve cornering accuracy, we redesigned the system using Ackermann steering. This allows each front wheel to follow its own turning radius, reducing wheel slip and improving stability.

<img width="3024" height="4032" alt="thisyearsteering" src="https://github.com/user-attachments/assets/56d586ea-e4fe-49f3-8ea5-3422533bf388" />

---

### 1.3 Rear Differential

A metal differential was used for the rear drivetrain to allow both wheels to rotate at different speeds during turns.

This design was chosen because it provides smoother cornering and better durability compared to 3D printed gears, while maintaining a lower centre of gravity compared to LEGO-based alternatives.

<img width="350" alt="differential" src="IMAGE">

---

### 1.4 Chassis Dimensions

Multiple chassis layouts were tested using LEGO prototypes to determine the optimal size for fitting components such as the Raspberry Pi, custom PCB, DC motor, battery, and sensors.

The final chassis was designed to be compact while maintaining balanced weight distribution. Inspired by Formula One cars, we used a larger length-to-width ratio to increase the turning radius, resulting in smoother and more controlled cornering.

<img width="450" alt="chassis_design" src="IMAGE">
