import customtkinter as ctk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import Image

import threading
import time
import os

from PhysicsEngine import RocketPhysicsEngine
from DataManager import DataManager


# -----------------------------
# APP CONFIG
# -----------------------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class RocketLaunchApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Flight Dynamics Simulator")
        self.geometry("1600x900")
        self.minsize(1400, 800)

        self.physics = RocketPhysicsEngine()
        self.dataManager = DataManager()

        self.simulationRunning = False

        self.configure(fg_color="#050816")

        self.create_ui()
        self.load_history()

    # ------------------------------------------------
    # UI
    # ------------------------------------------------

    def create_ui(self):

        # HEADER
        self.header = ctk.CTkFrame(
            self,
            height=70,
            fg_color="#0b1220",
            corner_radius=20
        )
        self.header.pack(fill="x", padx=15, pady=15)

        title = ctk.CTkLabel(
            self.header,
            text="FLIGHT DYNAMICS SIMULATOR",
            font=("Arial", 20, "bold"),
            text_color="#00D9FF"
        )
        title.pack(side="left", padx=20, pady=15)

        self.statusLabel = ctk.CTkLabel(
            self.header,
            text="READY",
            font=("Arial", 18, "bold"),
            text_color="lime"
        )
        self.statusLabel.pack(side="right", padx=20)

        # MAIN BODY

        self.mainFrame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.mainFrame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.create_left_panel()
        self.create_center_panel()
        self.create_right_panel()

    # ------------------------------------------------
    # LEFT PANEL
    # ------------------------------------------------

    def create_left_panel(self):

        self.leftPanel = ctk.CTkFrame(
            self.mainFrame,
            width=330,
            fg_color="#101827",
            corner_radius=25
        )

        self.leftPanel.pack(
            side="left",
            fill="y",
            padx=10
        )

        ctk.CTkLabel(
            self.leftPanel,
            text="LAUNCH CONFIGURATION",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        # Velocity

        ctk.CTkLabel(
            self.leftPanel,
            text="Launch Velocity (m/s)"
        ).pack()

        self.velocitySlider = ctk.CTkSlider(
            self.leftPanel,
            from_=50,
            to=500
        )

        self.velocitySlider.set(150)
        self.velocitySlider.pack(
            fill="x",
            padx=20,
            pady=10
        )

        # Angle

        ctk.CTkLabel(
            self.leftPanel,
            text="Flight Path Angle"
        ).pack()

        self.angleSlider = ctk.CTkSlider(
            self.leftPanel,
            from_=10,
            to=90
        )

        self.angleSlider.set(45)

        self.angleSlider.pack(
            fill="x",
            padx=20,
            pady=10
        )

        # PLANET

        ctk.CTkLabel(
            self.leftPanel,
            text="Target Environment"
        ).pack(pady=5)

        self.planetMenu = ctk.CTkOptionMenu(
            self.leftPanel,
            values=[
                "Earth",
                "Moon",
                "Mars"
            ]
        )

        self.planetMenu.pack(
            pady=10
        )

        # Launch Button

        self.launchBtn = ctk.CTkButton(
            self.leftPanel,
            text="EXECUTE MISSION",
            height=40,
            font=("Arial", 16, "bold"),
            fg_color="#00D9FF",
            text_color="black",
            command=self.start_countdown
        )

        self.launchBtn.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.countdownLabel = ctk.CTkLabel(
            self.leftPanel,
            text="READY",
            font=("Arial", 20, "bold"),
            text_color="#00D9FF"
        )

        self.countdownLabel.pack(
            pady=10
        )

        # TELEMETRY

        ctk.CTkLabel(
            self.leftPanel,
            text="FLIGHT TELEMETRY",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        self.altitudeLabel = ctk.CTkLabel(
            self.leftPanel,
            text="Current Altitude : 0 m"
        )
        self.altitudeLabel.pack()

        self.distanceLabel = ctk.CTkLabel(
            self.leftPanel,
            text="Distance : 0 m"
        )
        self.distanceLabel.pack()

        self.timeLabel = ctk.CTkLabel(
            self.leftPanel,
            text="Time : 0 s"
        )
        self.timeLabel.pack()

        self.velocityLabel = ctk.CTkLabel(
            self.leftPanel,
            text="Velocity : 0 m/s"
        )
        self.velocityLabel.pack()

        # ------------------------------------------------
    # CENTER PANEL
    # ------------------------------------------------

    def create_center_panel(self):

        self.centerPanel = ctk.CTkFrame(
            self.mainFrame,
            fg_color="#101827",
            corner_radius=25
        )

        self.centerPanel.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10
        )

        ctk.CTkLabel(
            self.centerPanel,
            text="TRAJECTORY VISUALIZATION",
            font=("Arial", 20, "bold")
        ).pack(pady=10)

        # STATS CARDS

        cardsFrame = ctk.CTkFrame(
            self.centerPanel,
            fg_color="transparent"
        )

        cardsFrame.pack(
            fill="x",
            padx=15,
            pady=10
        )

        self.altCard = self.create_stat_card(
            cardsFrame,
            "MAX ALTITUDE",
            "0 m"
        )

        self.distCard = self.create_stat_card(
            cardsFrame,
            "MAX DISTANCE",
            "0 m"
        )

        self.timeCard = self.create_stat_card(
            cardsFrame,
            "FLIGHT TIME",
            "0 s"
        )

        # GRAPH

        self.figure = Figure(
            figsize=(8, 5),
            dpi=100
        )

        self.ax = self.figure.add_subplot(111)

        self.ax.set_facecolor("#101827")
        self.figure.patch.set_facecolor("#101827")

        self.ax.set_title(
            "Flight Profile",
            color="white",
            fontsize=16
        )

        self.ax.set_xlabel(
            "Distance (m)",
            color="white"
        )

        self.ax.set_ylabel(
            "Altitude (m)",
            color="white"
        )

        self.ax.tick_params(
            colors="white"
        )

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=self.centerPanel
        )

        self.canvas.draw()

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    # ------------------------------------------------
    # RIGHT PANEL
    # ------------------------------------------------

    def create_right_panel(self):

        self.rightPanel = ctk.CTkFrame(
            self.mainFrame,
            width=450,
            fg_color="#101827",
            corner_radius=25
        )

        self.rightPanel.pack(
            side="right",
            fill="y",
            padx=10
        )

        ctk.CTkLabel(
            self.rightPanel,
            text="MISSION HISTORY",
            font=("Arial", 22, "bold")
        ).pack(pady=15)

        columns = (
            "Mission",
            "Velocity",
            "Altitude",
            "Distance",
            "Time"
        )

        self.historyTree = ttk.Treeview(
            self.rightPanel,
            columns=columns,
            show="headings",
            height=25
        )

        for col in columns:

            self.historyTree.heading(
                col,
                text=col
            )

            self.historyTree.column(
                col,
                width=80
            )

        self.historyTree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.clearBtn = ctk.CTkButton(
            self.rightPanel,
            text="🗑 Clear History",
            fg_color="red",
            command=self.clear_history
        )

        self.clearBtn.pack(
            fill="x",
            padx=15,
            pady=10
        )

    # ------------------------------------------------
    # STAT CARD
    # ------------------------------------------------

    def create_stat_card(
        self,
        parent,
        title,
        value
    ):

        frame = ctk.CTkFrame(
            parent,
            width=180,
            height=90,
            fg_color="#0b1220",
            corner_radius=20
        )

        frame.pack(
            side="left",
            padx=10,
            pady=10,
            fill="x",
            expand=True
        )

        ctk.CTkLabel(
            frame,
            text=title,
            font=("Arial", 12)
        ).pack(pady=5)

        label = ctk.CTkLabel(
            frame,
            text=value,
            font=("Arial", 22, "bold"),
            text_color="#00D9FF"
        )

        label.pack()

        return label

    # ------------------------------------------------
    # PLANET GRAVITY
    # ------------------------------------------------

    def get_gravity(self):

        planet = self.planetMenu.get()

        if planet == "Moon":
            return 1.62

        if planet == "Mars":
            return 3.71

        return 9.81

    # ------------------------------------------------
    # COUNTDOWN
    # ------------------------------------------------

    def start_countdown(self):

        if self.simulationRunning:
            return

        threading.Thread(
            target=self.countdown_thread,
            daemon=True
        ).start()

    def countdown_thread(self):

        self.statusLabel.configure(
            text="COUNTDOWN",
            text_color="orange"
        )

        for i in range(5, 0, -1):

            self.countdownLabel.configure(
                text=f"{i}"
            )

            time.sleep(1)

        self.countdownLabel.configure(
            text="LAUNCH"
        )

        self.launch_mission()

    # ------------------------------------------------
    # LAUNCH
    # ------------------------------------------------

    def launch_mission(self):

        velocity = self.velocitySlider.get()

        angle = self.angleSlider.get()

        gravity = self.get_gravity()

        self.physics.setParameters(
            velocity,
            angle,
            gravity
        )

        self.simulationRunning = True

        self.statusLabel.configure(
            text="MISSION ACTIVE",
            text_color="lime"
        )

        threading.Thread(
            target=self.run_simulation,
            daemon=True
        ).start()
    
        # ------------------------------------------------
    # SIMULATION LOOP
    # ------------------------------------------------

    def run_simulation(self):

        while self.physics.updateState(0.1):

            self.update_telemetry()

            self.update_graph()

            time.sleep(0.05)

        self.mission_complete()

    # ------------------------------------------------
    # UPDATE TELEMETRY
    # ------------------------------------------------

    def update_telemetry(self):

        altitude = self.physics.currentAltitude
        distance = self.physics.currentDistance
        flightTime = self.physics.currentTime

        self.altitudeLabel.configure(
            text=f"Altitude : {altitude:.2f} m"
        )

        self.distanceLabel.configure(
            text=f"Distance : {distance:.2f} m"
        )

        self.timeLabel.configure(
            text=f"Time : {flightTime:.2f} s"
        )

        self.velocityLabel.configure(
            text=f"Velocity : {self.physics.initialVelocity:.2f} m/s"
        )

        self.altCard.configure(
            text=f"{self.physics.maxAltitude:.2f} m"
        )

        self.distCard.configure(
            text=f"{self.physics.maxDistance:.2f} m"
        )

        self.timeCard.configure(
            text=f"{flightTime:.2f} s"
        )

    # ------------------------------------------------
    # UPDATE GRAPH
    # ------------------------------------------------

    def update_graph(self):

        self.ax.clear()

        self.ax.set_facecolor("#101827")

        self.ax.set_title(
            "Rocket Trajectory",
            color="white"
        )

        self.ax.set_xlabel(
            "Distance (m)",
            color="white"
        )

        self.ax.set_ylabel(
            "Altitude (m)",
            color="white"
        )

        self.ax.tick_params(
            colors="white"
        )

        self.ax.grid(
            True,
            alpha=0.3
        )

        self.ax.plot(
            self.physics.distanceData,
            self.physics.altitudeData,
            linewidth=3,
            color="#00D9FF"
        )

        if len(self.physics.distanceData) > 0:

            self.ax.scatter(
                self.physics.distanceData[-1],
                self.physics.altitudeData[-1],
                s=120,
                color="red"
            )

        self.canvas.draw()

    # ------------------------------------------------
    # MISSION COMPLETE
    # ------------------------------------------------

    def mission_complete(self):

        self.statusLabel.configure(
            text="MISSION COMPLETE",
            text_color="lime"
        )

        summary = self.physics.getMissionSummary()

        missionId = (
            self.dataManager.getMissionCount() + 1
        )

        self.dataManager.saveLaunchRecord(
            missionId,
            summary["initialVelocity"],
            summary["launchAngle"],
            summary["gravity"],
            summary["maxAltitude"],
            summary["maxDistance"],
            summary["flightTime"]
        )

        self.load_history()

        self.simulationRunning = False

        messagebox.showinfo(
            "Mission Complete",
            f"""
Mission ID : {missionId}

Max Altitude :
{summary['maxAltitude']} m

Max Distance :
{summary['maxDistance']} m

Flight Time :
{summary['flightTime']} s
"""
        )

    # ------------------------------------------------
    # LOAD HISTORY
    # ------------------------------------------------

    def load_history(self):

        for item in self.historyTree.get_children():

            self.historyTree.delete(item)

        history = self.dataManager.getLaunchHistory()

        for row in history:

            self.historyTree.insert(
                "",
                "end",
                values=(
                    row["MissionID"],
                    row["Velocity"],
                    row["MaxAltitude"],
                    row["MaxDistance"],
                    row["FlightTime"]
                )
            )

    # ------------------------------------------------
    # CLEAR HISTORY
    # ------------------------------------------------

    def clear_history(self):

        answer = messagebox.askyesno(
            "Confirm",
            "Delete all mission history?"
        )

        if not answer:
            return

        self.dataManager.clearHistory()

        self.load_history()

        messagebox.showinfo(
            "Success",
            "History Cleared"
        )

    # ------------------------------------------------
    # RESET MISSION
    # ------------------------------------------------

    def reset_dashboard(self):

        self.altitudeLabel.configure(
            text="Altitude : 0 m"
        )

        self.distanceLabel.configure(
            text="Distance : 0 m"
        )

        self.timeLabel.configure(
            text="Time : 0 s"
        )

        self.velocityLabel.configure(
            text="Velocity : 0 m/s"
        )

        self.altCard.configure(
            text="0 m"
        )

        self.distCard.configure(
            text="0 m"
        )

        self.timeCard.configure(
            text="0 s"
        )

        self.countdownLabel.configure(
            text="READY"
        )

        self.statusLabel.configure(
            text="READY",
            text_color="lime"
        )

        self.ax.clear()

        self.ax.set_facecolor("#101827")

        self.canvas.draw()