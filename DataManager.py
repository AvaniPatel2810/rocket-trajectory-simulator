import csv
import os
from datetime import datetime


class DataManager:

    def __init__(self):
        self.fileName = "launchHistory.csv"
        self.createHistoryFile()

    def createHistoryFile(self):
        if not os.path.exists(self.fileName):
            with open(self.fileName, "w", newline="") as file:
                writer = csv.writer(file)

                writer.writerow([
                    "MissionID",
                    "DateTime",
                    "Velocity",
                    "Angle",
                    "Gravity",
                    "MaxAltitude",
                    "MaxDistance",
                    "FlightTime"
                ])

    def saveLaunchRecord(
        self,
        missionId,
        velocity,
        angle,
        gravity,
        maxAltitude,
        maxDistance,
        flightTime
    ):
        with open(self.fileName, "a", newline="") as file:
            writer = csv.writer(file)

            writer.writerow([
                missionId,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                round(velocity, 2),
                round(angle, 2),
                round(gravity, 2),
                round(maxAltitude, 2),
                round(maxDistance, 2),
                round(flightTime, 2)
            ])

    def getLaunchHistory(self):
        history = []

        if not os.path.exists(self.fileName):
            return history

        with open(self.fileName, "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                history.append(row)

        return history

    def getMissionCount(self):
        history = self.getLaunchHistory()
        return len(history)

    def clearHistory(self):
        with open(self.fileName, "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow([
                "MissionID",
                "DateTime",
                "Velocity",
                "Angle",
                "Gravity",
                "MaxAltitude",
                "MaxDistance",
                "FlightTime"
            ])