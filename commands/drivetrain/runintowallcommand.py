from commands2 import CommandBase

import robot


class RunIntoWallCommand(CommandBase):
    """Drives the robot at a steady speed until it crashes into something."""

    def __init__(self):
        super().__init__()

        self.addRequirements(robot.drivetrain)

    def initialize(self):
        robot.drivetrain.setProfile(0)
        robot.drivetrain.move(0, 1, 0)

    def isFinished(self):
        if self.isTimedOut():
            return True

        return abs(robot.drivetrain.getAcceleration()) > 1

    def end(self, interrupted):
        robot.drivetrain.stop()
