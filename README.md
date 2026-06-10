# rocket-trajectory-simulator


# 🚀 NovaLaunch

Physics-based rocket trajectory simulator built with Python, Tkinter, and Matplotlib, featuring real-time trajectory visualization and launch parameter analysis.

Flight Dynamics Simulator is designed to demonstrate the principles of rocket motion and flight dynamics under different gravitational environments.

Users can configure launch parameters, execute missions, visualize trajectories, monitor telemetry, and store mission records for future analysis.


# Screenshots

## Trajectory Visualization

<img width="1920" height="1017" alt="Screenshot (34)" src="https://github.com/user-attachments/assets/1a35a0a0-191c-477e-8e51-7e2ba7dbbbd2" />



<img width="1920" height="1011" alt="Screenshot (35)" src="https://github.com/user-attachments/assets/5a54d6c4-8859-4ff5-afcc-19889f362965" />


---

## Features

### Mission Configuration

* Adjustable Launch Velocity
* Adjustable Flight Path Angle
* Multiple Planet Environments:

  * Earth 
  * Moon 
  * Mars 

### Real-Time Trajectory Simulation

* Physics-based projectile motion
* Live altitude tracking
* Live distance tracking
* Real-time flight updates
* Dynamic trajectory plotting

### Telemetry Dashboard

* Current Altitude
* Horizontal Distance
* Flight Time
* Launch Velocity
* Mission Status Monitoring

### Data Visualization

* Interactive Matplotlib graph
* Live trajectory updates
* Flight path visualization
* Maximum altitude tracking

### Mission History System

* CSV-based mission storage
* Mission statistics logging
* Persistent history records
* History clearing functionality

### Advanced Features

* Multithreaded countdown system
* Real-time simulation engine
* Object-Oriented Architecture

---

## Technologies Used

* Python 3
* CustomTkinter
* Matplotlib
* Pillow (PIL)
* CSV Data Storage
* Object-Oriented Programming (OOP)
* Multithreading

---

## 📂 Project Structure

```text
FlightDynamicsSimulator/
│
├── main.py
├── RocketLaunchApp.py
├── PhysicsEngine.py
├── DataManager.py
├── launchHistory.csv
└── README.md
```

---

## System Architecture

### Physics Engine

Responsible for:

* Projectile motion calculations
* Flight time computation
* Maximum altitude calculation
* Horizontal distance calculation
* Real-time position updates

### Data Manager

Responsible for:

* CSV file creation
* Mission data storage
* Mission retrieval
* History management

### GUI Layer

Responsible for:

* User interaction
* Telemetry dashboard
* Trajectory visualization
* Mission controls

---

## Physics Equations Used

### Horizontal Distance

```math
x = v_x t
```

### Vertical Position

```math
y = v_y t - \frac{1}{2}gt^2
```

### Time of Flight

```math
T = \frac{2v_y}{g}
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/flight-dynamics-simulator.git
```

### Navigate to Project Directory

```bash
cd flight-dynamics-simulator
```

### Install Dependencies

```bash
pip install customtkinter matplotlib pillow
```

### Run the Application

```bash
python main.py
```

---

## Learning Outcomes

This project demonstrates:

* Object-Oriented Programming
* GUI Development
* Physics Simulation
* Aerospace Fundamentals
* Data Visualization
* Multithreading
* File Handling
* Software Architecture Design

---

## Future Enhancements

* Atmospheric Drag Simulation
* Wind Resistance Modeling
* Multi-Stage Rocket Support
* Satellite Deployment Mode
* PDF Mission Reports
* 3D Trajectory Visualization
* Advanced Analytics Dashboard
* Real-Time Velocity Vectors

---

##  Author

**Avani Patel**

Computer Engineering Student

Birla Vishvakarma Mahavidyalaya (BVM)

### Connect With Me

* GitHub: https://github.com/AvaniPatel2810
