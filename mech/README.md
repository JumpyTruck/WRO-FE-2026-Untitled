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

### 1.4 Design Inspiration & Chassis Dimensions

Before designing our chassis, we explored different vehicle layouts and proportions through sketches and concept drawings. We took inspiration from Formula One cars, focusing on a longer and narrower body design to improve stability and create smoother, more controlled turning.

The overall dimensions were chosen to maintain a compact design while providing enough space for essential components such as the Raspberry Pi, custom PCB, DC motor, battery, and sensors. This layout helped us achieve a balanced centre of gravity while keeping the robot agile and stable.

<img width="252" height="336" alt="IMG_1527" src="https://github.com/user-attachments/assets/17898f3a-5b99-4380-ab8f-eba7226495c5" />

---

# 2. Structural Design Process

After finalizing the main mechanical choices, we developed multiple chassis iterations to optimize component placement, structural strength, and weight distribution. Each version addressed limitations found during testing and gradually improved the overall robot design.

---

## 2.1 Chassis Iteration 1 — Initial Frame Design

The first chassis prototype focused on creating a basic structural frame with mounting points for the main drivetrain components, including the DC motor and servo motor.

However, this design did not include mounting points for the second plate, making it difficult to securely attach additional components such as the Raspberry Pi, custom PCB, and camera.

**Issue Identified:**
- No space for standoffs between chassis plates
- Limited room for future component expansion

<img width="336" height="252" alt="IMG_2297" src="https://github.com/user-attachments/assets/c09e16ee-0dce-4a40-99b6-c4569ce3b0a5" />

---

## 2.2 Chassis Iteration 2 — Expanded Frame Design

The second chassis iteration increased the overall size and added mounting holes for standoffs, allowing a second plate to be attached for electronics mounting.

However, after adding the upper plate, we discovered that there was insufficient space for the battery pack, which affected component placement and weight distribution.

**Issue Identified:**
- Improved structural support
- Insufficient space for battery placement
- Uneven weight distribution due to limited battery positioning

<img width="336" height="252" alt="IMG_2298" src="https://github.com/user-attachments/assets/b72d6ca1-537b-4b37-b571-bb60e22433d7" />

---

## 2.3 Chassis Iteration 3 — Final Optimized Chassis

The final chassis iteration integrated all required components while improving the overall layout and weight distribution.

The motor mount was redesigned with a top opening, allowing the motor to slide into place like a "hat" mount. This simplified assembly while providing a secure connection. The battery pack was positioned in the center of the chassis to evenly distribute weight and maintain a balanced centre of gravity.

**Final Improvements:**
- Space for all electronics and structural components
- Improved motor mounting system
- Centered battery placement for balanced weight distribution
- Increased stability during acceleration and turning

<img width="336" height="252" alt="IMG_2299" src="https://github.com/user-attachments/assets/d65b5031-916f-4674-9e84-d1f3296ae2f0" />

---

## 2.4 Final Robot Assembly

The final robot combines all mechanical improvements from previous iterations, including the optimized chassis, Ackermann steering system, rear differential, SPIKE Prime wheels, and integrated electronics mounting.

The final design focuses on reliability, balanced weight distribution, and precise movement to perform consistently during the WRO Future Engineers challenge.

<img width="252" height="336" alt="IMG_1967" src="https://github.com/user-attachments/assets/0cca0d85-2654-46ef-bd2c-4e263146fa95" />
