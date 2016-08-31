from wpilib.command.subsystem import Subsystem
from wpilib.cantalon import CANTalon
from wpilib.preferences import Preferences
from wpilib.livewindow import LiveWindow
from networktables import NetworkTable

from robotpy_ext.common_drivers.navx.ahrs import AHRS

from commands.drivecommand import DriveCommand
import ports

class BaseDrive(Subsystem):
    '''
    A general case drive train system. It abstracts away shared functionality of
    the various drive types that we can employ. Anything that can be done with
    knowing what type of drive system we have should be implemented here.
    '''

    def __init__(self, name):
        super().__init__(name)

        '''
        Create all motors, disable the watchdog, and turn off neutral braking
        since the PID loops will provide braking.
        '''
        self.motors = [
            CANTalon(ports.drivetrain.frontLeftMotorID),
            CANTalon(ports.drivetrain.frontRightMotorID),
            CANTalon(ports.drivetrain.backLeftMotorID),
            CANTalon(ports.drivetrain.backRightMotorID),
        ]

        for motor in self.motors:
            motor.setSafetyEnabled(False)
            motor.enableBrakeMode(False)

        '''
        Subclasses should configure motors correctly and populate activeMotors.
        '''
        self.activeMotors = []
        self._configureMotors()

        '''Initialize the navX MXP'''
        self.navX = AHRS.create_spi()
        self.resetGyro()

        '''A record of the last arguments to move()'''
        self.lastInputs = None

        self.setUseEncoders()
        self.maxSpeed = Preferences \
            .getInstance() \
            .getInt('DriveTrain/maxSpeed', 1)

        NetworkTable \
            .getTable('Preferences/DriveTrain') \
            .addSubTableListener(self._updateValues)

        '''Add items that can be debugged in Test mode.'''
        LiveWindow.addSensor(self, 'navX', self.navX)

        LiveWindow.addActuator(self, 'Front Left Motor', self.motors[0])
        LiveWindow.addActuator(self, 'Front Right Motor', self.motors[1])
        LiveWindow.addActuator(self, 'Back Left Motor', self.motors[2])
        LiveWindow.addActuator(self, 'Back Right Motor', self.motors[3])


    def initDefaultCommand(self):
        '''
        By default, unless another command is running that requires this
        subsystem, we will drive via joystick using the max speed stored in
        Preferences.
        '''
        self.setDefaultCommand(DriveCommand('DriveTrain/maxSpeed'))


    def move(self, x, y, rotate):
        '''Turns coordinate arguments into motor outputs.'''

        '''
        Short-circuits the rather expensive movement calculations if the
        coordinates have not changed.
        '''
        if [x, y, rotate] == self.lastInputs:
            return

        self.lastInputs = [x, y, rotate]

        speeds = self._calculateSpeeds(x, y, rotate)

        '''Prevent speeds > 0'''
        maxSpeed = 0
        for speed in speeds:
            maxSpeed = max(abs(speed), maxSpeed)

        if maxSpeed > 1:
            speeds = [x / maxSpeed for x in speeds]

        '''Use speeds to feed motor output.'''
        if self.useEncoders:
            if all(abs(x) < 0.1 for x in speeds):
                '''
                When we are trying to stop, clearing the I accumulator can
                reduce overshooting, thereby shortening the time required to
                come to a stop.
                '''
                for motor in self.activeMotors:
                    motor.clearIaccum()

            for motor, speed in zip(self.activeMotors, speeds):
                motor.set(speed * self.speedLimit)

        else:
            for motor, speed in zip(self.activeMotors, speeds):
                motor.set(speed * self.maxPercentVBus)


    def stop(self):
        '''A nice shortcut for calling move with all zeroes.'''

        if self.useEncoders:
            self._setMode(CANTalon.ControlMode.Speed)

        self.move(0, 0, 0)


    def resetGyro(self):
        '''Force the navX to consider the current angle to be zero degrees.'''

        self.navX.reset()
        self.gyroOffset = 0


    def setGyroAngle(self, angle):
        '''Tweak the gyro reading.'''

        heading = self.naxX.getYaw()
        self.gyroOffset = angle - heading


    def getAngle(self):
        '''Current gyro reading'''

        return (self.navX.getYaw() + self.gyroOffset) % 360


    def getSpeeds(self):
        '''Returns the speed of each active motors.'''

        if not self.useEncoders:
            raise RuntimeError('Cannot read speed. Encoders are disabled.')

        return [x.getSpeed() for x in self.activeMotors]


    def getPositions(self):
        '''Returns the position of each active motor.'''

        if not self.useEncoders:
            raise RuntimeError('Cannot read position. Encoders are disabled.')

        return [x.getPosition() for x in self.activeMotors]


    def setUseEncoders(self, useEncoders=True):
        '''
        Turns on and off encoders. As a side effect, if encoders are enabled,
        the motors will be set to speed mode. Disabling encoders should not be
        done lightly, as many commands rely on encoder information.
        '''

        self.useEncoders = useEncoders
        if useEncoders:
            self._setMode(CANTalon.ControlMode.Speed)
        else:
            self._setMode(CANTalon.ControlMode.PercentVBus)


    def setSpeedLimit(self, speed):
        '''
        Updates the max speed of the drive and changes to the appropriate
        mode depending on if encoders are enabled.
        '''

        if speed < 0:
            raise ValueError('DriveTrain speed cannot be less than 0')

        self.speedLimit = speed

        '''If we can't use encoders, attempt to approximate that speed.'''
        self.maxPercentVBus = min(speed / self.maxSpeed, 1)

        if self.useEncoders:
            self._setMode(CANTalon.ControlMode.Speed)
        else:
            self._setMode(CANTalon.ControlMode.PercentVBus)


    def _setMode(self, mode):
        '''
        Sets the control mode of active motors, with some intelligent changes
        depending on the mode.
        '''

        for motor in self.activeMotors:
            if mode == CANTalon.ControlMode.Position:
                motor.setProfile(1)

            elif mode == CANTalon.ControlMode.Speed:
                motor.setProfile(0)
                motor.clearIaccum()

            motor.setControlMode(mode)


    def _updateValues(self, source, key, value, isNew):
        '''
        Listener for changes to Preferences. When a key changes, this function
        tries to do the right thing.
        '''

        if key == 'maxSpeed':
            self.maxSpeed = int(value)
            if value < self.speedLimit:
                self.setSpeedLimit(value)


    def _configureMotors(self):
        '''
        Make any necessary changes to the motors and define self.activeMotors.
        '''

        raise NotImplementedError()


    def _calculateSpeeds(self, x, y, rotate):
        '''Return a speed for each active motor.'''

        raise NotImplementedError()
