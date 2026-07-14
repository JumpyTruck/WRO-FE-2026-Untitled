# 🛠️ Mechanical Design

This section describes the mechanical design process of our WRO Future Engineers robot. Each component was selected and optimized through testing and iteration to improve reliability, stability, and autonomous performance.

---

# 1. Mechanical Design Choices

## 1.1 Wheel Selection

We chose **LEGO SPIKE Prime wheels (56mm diameter, 14mm thickness)** because they provide excellent grip on the WRO competition mat while maintaining an ideal balance between speed, torque, and stability. Their size is optimized for our robot, as they are compact enough to keep the chassis lightweight while still being large enough to provide smooth movement and sufficient ground clearance.

<p align="center">
<img width="300" src="https://github.com/user-attachments/assets/aed5ae47-584d-46ec-b6de-314e087e4393">
</p>

---

## 1.2 Steering System

### Previous Design: Parallel Beam Steering

Our previous robot used a **parallel beam steering system**, where both front wheels rotated at the same angle. However, this caused drifting during turns because both wheels traveled along the same turning radius, resulting in wheel scrubbing and inaccurate cornering.

<p align="center">
<img width="350" src="https://github.com/user-attachments/assets/1a65af16-12c8-4bed-90fe-fb8c90146218">
</p>

### Current Design: Ackermann Steering

To solve this issue, we implemented an **Ackermann steering system**. This allows the inner and outer wheels to rotate at different angles, allowing each wheel to follow its correct turning radius. This significantly improved turning accuracy and reduced drifting.

<p align="center">
<img width="350" src="https://github.com/user-attachments/assets/48afcbfe-0fe2-42e0-af9d-fb36e7adf2aa">
</p>

---

## 1.3 Rear Differential

The rear drivetrain uses a **metal differential system** to allow the two rear wheels to rotate at different speeds during cornering.

We avoided 3D printed gears because they could wear down or break under repeated testing. We also avoided LEGO differential components because they increased the height of the drivetrain and negatively affected the robot's centre of gravity.

The metal differential provides:
- Improved cornering stability
- Reduced wheel slip
- Better weight distribution
- Increased drivetrain reliability

<p align="center">
<img width="350" src="IMAGE">
</p>

---

## 1.4 Chassis Dimensions

We experimented with different chassis sizes using LEGO prototypes to determine the optimal dimensions required to fit all components, including the Raspberry Pi, custom PCB, DC motor, sensors, and battery.

Our goal was to create the smallest possible chassis while:
- Securely fitting all electronics
- Maintaining a balanced centre of gravity
- Leaving enough space for maintenance and wiring

The design was inspired by **Formula One cars**, using a relatively large length-to-width ratio. This increased the turning radius, allowing smoother and more controlled cornering while improving overall stability.

<p align="center">
<img width="450" src="IMAGE">
</p>

---

# 2. Mechanical Iteration Process

Throughout development, we created multiple prototypes and improved the design based on testing results.

| Version | Changes | Purpose |
|---|---|---|
| V1 | Initial chassis prototype | Tested component placement |
| V2 | Adjusted chassis dimensions | Improved weight distribution |
| V3 | Redesigned steering system | Reduced turning drift |
| V4 | Added differential drivetrain | Improved cornering performance |
| Final | Competition chassis | Reliable and optimized design |

---

# 3. Final Robot Assembly

<p align="center">
<img width="500" src="IMAGE">
</p>

The final mechanical design combines the optimized chassis, Ackermann steering, differential drivetrain, and SPIKE Prime wheels to create a stable and accurate autonomous vehicle.

---

# 4. CAD Design

All mechanical components were designed and tested using CAD software before manufacturing.

Included designs:
- Chassis frame
- Steering assembly
- Motor mount
- Sensor mounts
- PCB mount
- Camera mount

<p align="center">
<img width="500" src="IMAGE">
</p>
