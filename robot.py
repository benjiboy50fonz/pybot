#!/usr/bin/env python3

from commands2 import TimedCommandRobot
from wpilib._impl.main import run
from wpilib import RobotBase

from custom import driverhud
import controller.layout
import subsystems
import shutil, sys, os, inspect

from commands2 import Subsystem, CommandScheduler

from subsystems.monitor import Monitor as monitor
from subsystems.drivetrain import DriveTrain as drivetrain
from subsystems.chamber import Chamber as chamber
from subsystems.conveyor import Conveyor as conveyor
from subsystems.intake import Intake as intake
from subsystems.shooter import Shooter as shooter
from subsystems.limelight import Limelight as limelight


class KryptonBot(TimedCommandRobot):
    """Implements a Command Based robot design"""

    def robotInit(self):
        """Set up everything we need for a working robot."""

        if RobotBase.isSimulation():
            import mockdata

        self.subsystems()

        controller.layout.init()
        driverhud.init()

        from commands.drivetrain.zerocancoderscommand import ZeroCANCodersCommand
        from commands.startupcommandgroup import StartUpCommandGroup

        StartUpCommandGroup().schedule()

        from commands.drivetrain.drivecommand import DriveCommand

    def autonomousInit(self):
        """This function is called each time autonomous mode starts."""

        # Send field data to the dashboard
        driverhud.showField()

        # Schedule the autonomous command
        auton = driverhud.getAutonomousProgram()
        auton.schedule()
        driverhud.showInfo("Starting %s" % auton)

    def teleopInit(self):
        self.temp.initialize()

    def teleopPeriodic(self):

        print("scheudle")
        self.temp.execute()
        print("done")

    def disabledInit(self):
        pass

    def disabledPeriodic(self):
        pass

    def handleCrash(self, error):
        super().handleCrash()
        driverhud.showAlert("Fatal Error: %s" % error)

    @classmethod
    def subsystems(cls):
        vars = globals()
        module = sys.modules["robot"]
        for key, var in vars.items():
            try:
                if issubclass(var, Subsystem) and var is not Subsystem:
                    try:
                        setattr(module, key, var())
                    except TypeError as e:
                        print("failed " + str(key))
                        raise ValueError(f"Could not instantiate {key}") from e
            except TypeError:
                pass


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "deploy":
        shutil.rmtree("opkg_cache", ignore_errors=True)
        shutil.rmtree("pip_cache", ignore_errors=True)
    run(KryptonBot)
