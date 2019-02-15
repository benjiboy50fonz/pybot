from wpilib.command.command import Command
from custom.config import Config

import robot

class GoToTapeCommand(Command):

    def __init__(self):
        super().__init__('Go To Tape')
        self.strafe = Config('cameraTable/tapeStrafe', 0)
        self.distance = Config('cameraTable/tapeDistance', 0)
        self.angle = Config('cameraTable/tapeAngle', 0)

        self.x = None
        self.y = None
        self.rotate = None


    def initialize(self):
        if not robot.drivetrain.isFieldOriented:
            robot.drivetrain.toggleFieldOrientation()
        robot.drivetrain.resetGyro()


    def execute(self):
        self.x = self.strafe.getValue() / 50
        self.y = self.distance.getValue() / 36
        self.rotate = self.angle.getValue() / 10

        print('     X: ' + str(self.x))
        print('     Y: ' + str(self.y))
        print('Rotate: ' + str(self.rotate))
        print('')

        robot.drivetrain.move(self.x, self.y, self.rotate)


    def isFinished(self):
        return abs(self.x) <= 0.05 and abs(self.y) <= 0.05 and abs(self.rotate) <= 0.05


    def end(self):
        robot.drivetrain.stop()