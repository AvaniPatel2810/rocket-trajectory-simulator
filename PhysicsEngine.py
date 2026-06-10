import math


class RocketPhysicsEngine:

    def __init__(
        self,
        initialVelocity: float = 100,
        launchAngle: float = 45,
        gravity: float = 9.8
    ):
        self.timeData = []
        self.altitudeData = []
        self.distanceData = []

        self.currentTime = 0
        self.currentAltitude = 0
        self.currentDistance = 0

        self.maxAltitude = 0
        self.maxDistance = 0

        self.isLanded = False

        self.setParameters(
            initialVelocity,
            launchAngle,
            gravity
        )

    def calculateMaxTime(self) -> float:
        if self.gravity > 0:
            return (2 * self.vy) / self.gravity

        return 0

    def calculatePosition(
        self,
        time: float
    ) -> tuple[float, float]:

        distance = self.vx * time

        altitude = (
            self.vy * time
            - (0.5 * self.gravity * time ** 2)
        )

        return distance, max(0, altitude)

    def updateState(
        self,
        timeStep: float
    ) -> bool:

        self.currentTime += timeStep

        if self.currentTime >= self.maxTime:

            self.currentTime = self.maxTime

            (
                self.currentDistance,
                self.currentAltitude
            ) = self.calculatePosition(
                self.currentTime
            )

            self.currentAltitude = 0
            self.isLanded = True

            self.recordData()

            return False

        (
            self.currentDistance,
            self.currentAltitude
        ) = self.calculatePosition(
            self.currentTime
        )

        self.recordData()

        self.maxAltitude = max(
            self.maxAltitude,
            self.currentAltitude
        )

        self.maxDistance = max(
            self.maxDistance,
            self.currentDistance
        )

        if (
            self.currentAltitude <= 0
            and self.currentTime > 0.1
        ):
            self.currentAltitude = 0
            self.isLanded = True

            return False

        return True

    def recordData(self):

        self.timeData.append(
            self.currentTime
        )

        self.distanceData.append(
            self.currentDistance
        )

        self.altitudeData.append(
            self.currentAltitude
        )

    def reset(self):

        self.timeData = []
        self.altitudeData = []
        self.distanceData = []

        self.currentTime = 0
        self.currentAltitude = 0
        self.currentDistance = 0

        self.maxAltitude = 0
        self.maxDistance = 0

        self.isLanded = False

        if hasattr(self, "vy"):
            self.maxTime = (
                self.calculateMaxTime()
            )

    def setParameters(
        self,
        initialVelocity: float,
        launchAngle: float,
        gravity: float
    ):

        self.initialVelocity = (
            initialVelocity
        )

        self.launchAngle = (
            launchAngle
        )

        self.gravity = gravity

        angleRadians = math.radians(
            launchAngle
        )

        self.vx = (
            initialVelocity
            * math.cos(angleRadians)
        )

        self.vy = (
            initialVelocity
            * math.sin(angleRadians)
        )

        self.reset()

    def getMissionSummary(self):

        return {
            "maxAltitude": round(
                self.maxAltitude,
                2
            ),
            "maxDistance": round(
                self.maxDistance,
                2
            ),
            "flightTime": round(
                self.currentTime,
                2
            ),
            "initialVelocity": round(
                self.initialVelocity,
                2
            ),
            "launchAngle": round(
                self.launchAngle,
                2
            ),
            "gravity": round(
                self.gravity,
                2
            )
        }