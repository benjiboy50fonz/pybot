'''
This is the place where we store port numbers for all subsystems. It is based on
the RobotMap concept from WPILib. Each subsystem should have its own ports list.
Values other than port numbers should be stored in Preferences.
'''

class PortsList:
    '''Dummy class used to store variables on an object.'''
    pass

drivetrain = PortsList()

'''CAN IDs for motors'''
drivetrain.frontLeftMotorID = 1
drivetrain.frontRightMotorID = 3
drivetrain.backLeftMotorID = 2
drivetrain.backRightMotorID = 4


shooter = PortsList()

shooter.motorID = 5


pickup = PortsList()

pickup.motorID = 6


climber = PortsList()

climber.motorID = 7
climber.sensorID = 0

feeder = PortsList()

feeder.motorID = 8
feeder.sensorID = 1

gear = PortsList()

gear.sensorID = 2
