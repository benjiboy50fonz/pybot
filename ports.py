"""
This is the place where we store port numbers for all subsystems. It is based on
the RobotMap concept from WPILib. Each subsystem should have its own ports list.
Values other than port numbers should be stored in Config.
"""


class PortsList:
    """Dummy class used to store variables on an object."""

    pass


drivetrain = PortsList()

"""CAN IDs for motors"""
drivetrain.frontLeftDriveID = 1
drivetrain.frontRightDriveID = 43
drivetrain.backLeftDriveID = 42
drivetrain.backRightDriveID = 4

drivetrain.frontLeftTurnID = 2
drivetrain.frontRightTurnID = 6
drivetrain.backLeftTurnID = 7
drivetrain.backRightTurnID = 8

drivetrain.frontLeftCANCoder = 3
drivetrain.frontRightCANCoder = 10
drivetrain.backLeftCANCoder = 11
drivetrain.backRightCANCoder = 12
