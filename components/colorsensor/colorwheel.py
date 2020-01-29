import wpilib

from rev import ControlType

from rev.color import ColorSensorV3, ColorMatch
from ctre import ControlMode, FeedbackDevice

class ColorWheel:

    colorSensor: object
    colorWheelMotor: object
    colorWheelEncoder: object
    colorWheelController: object

    def setup(self):
        self.colorSensor.configureColorSensor(
            ColorSensorV3.ColorResolution.k18bit,
            ColorSensorV3.ColorMeasurementRate.k50ms
                                              ) # Tune these values as needed.

        self.colorWheelMotor.setInverted(False) # might need to change

        self.colorWheelMotor.setP(0.01, 0) # Dummy values from the falcon tester
        self.colorWheelMotor.setI(0, 0)
        self.colorWheelMotor.setD(0.1, 0)
        self.colorWheelMotor.setIZone(1, 0)
        self.colorWheelMotor.setFF(0.1, 0)

    def getColor(self):
        return self.colorSensor.getColor()

    def spinFour(self):
        #self.colorWheelMotor.set(ControlMode.Position, (self.colorWheelMotor.getSelectedSensorPosition() + )
        self.colorWheelController.setReference(50, ControlType.kPosition, 0, 0)

    def spinClockwise(self):
        self.colorWheelMotor.set(0.9)

    def spinCClockwise(self):
        self.colorWheelMotor.set(-0.9)
