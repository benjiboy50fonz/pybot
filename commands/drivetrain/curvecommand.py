from wpilib.command import Command

import robot
import math


class CurveCommand(Command):

    def __init__(self, val, num):

        super().__init__('Curve')

        self.requires(robot.drivetrain)

        self.degrees = val
        self.radius = num

    def initialize(self):
        self.distanceL = ( self.degrees / 360 ) * 2 * ( self.radius + 12 ) * math.pi
        self.distanceL = self.distanceL * 10.7* 2048 / (6*math.pi)
        self.distanceR = ( self.degrees / 360 ) * 2 * ( self.radius - 12 ) * math.pi
        self.distanceR = self.distanceR * 10.7 * 2048 / (6*math.pi)
        self.speedRatio = self.distanceL / self.distanceR
        self.startDistanceL = robot.drivetrain.getPositions()[0]
        self.startDistanceR = robot.drivetrain.getPositions()[1] * -1
        self.finishDistanceL = self.startDistanceL - self.distanceL
        self.finishDistanceR = (self.startDistanceR - self.distanceR )

    def execute(self):
        self.currentDistanceL = robot.drivetrain.getPositions()[0]
        self.currentDistanceR = robot.drivetrain.getPositions()[1] * -1
        self.speedL = ( self.finishDistanceL - self.currentDistanceL ) * 1
        self.speedR = ( self.finishDistanceR - self.currentDistanceR ) * 1
        self.maxSpeed = 10000
        self.minSpeed = 0

        if abs(self.speedL) > self.maxSpeed or abs(self.speedR) > self.maxSpeed:
            if abs(self.speedL) > abs(self.speedR):
                self.speedL = math.copysign(self.maxSpeed, self.speedL)
                self.speedR = math.copysign(self.maxSpeed / self.speedRatio, self.speedR)
            else:
                self.speedR = math.copysign(self.maxSpeed, self.speedR)
                self.speedL = math.copysign(self.maxSpeed / self.speedRatio, self.speedL)

        self.speedR = self.speedR * -1
        robot.drivetrain.setSpeeds(self.speedL, self.speedR)

        if self.currentDistanceL > self.finishDistanceL - 50 and self.currentDistanceL < self.finishDistanceL + 50:
            robot.drivetrain.stop()
        if self.currentDistanceR > self.finishDistanceR - 50 and self.currentDistanceR < self.finishDistanceR + 50:
            robot.drivetrain.stop()
