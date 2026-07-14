# Mechanical Design Process

This section outlines the main mechanical decisions made during the development of our WRO Future Engineers robot. Each component was designed and tested to improve reliability, stability, and performance.

---

## 1. Mechanical Design Choices

### 1.1 Wheel Selection

We chose **SPIKE Prime wheels (56mm diameter, 14mm thickness)** because their size provides the ideal balance between speed, torque, and stability. They are compact enough to maintain a lightweight design while still providing sufficient grip and clearance for reliable movement on the WRO mat.

<img width="280" height="187" alt="spike_wheels" src="https://github.com/user-attachments/assets/873b32bb-68e5-45ca-adc8-cf2fd2dda6f8" />

---
### 1.2 Steering System

We experimented with different steering mechanisms to improve turning accuracy and reduce drifting.

<table>
<tr>
<td align="center">
<b>Previous Design — Parallel Beam Steering</b>
<br><br>
<img width="220" src="https://github.com/user-attachments/assets/73cccba8-f506-4c5d-ad07-ef9bd6d4d4c9">
<br><br>
Both wheels turned at the same angle, causing drifting because the inner and outer wheels followed different turning paths.
</td>

<td align="center">
<b>Final Design — Ackermann Steering</b>
<br><br>
<img width="220" src="https://github.com/user-attachments/assets/56d586ea-e4fe-49f3-8ea5-3422533bf388">
<br><br>
Each wheel follows its own turning radius, reducing wheel slip and improving cornering accuracy.
</td>
</tr>
</table>

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
