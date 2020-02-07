from .debuggablesubsystem import DebuggableSubsystem

from ctre import ControlMode, WPI_TalonSRX, NeutralMode

import ports


class BallSystem(DebuggableSubsystem):
    '''Describe what this subsystem does.'''

    def __init__(self):
        super().__init__('BallSystem')
        self.indexWheelMotor = WPI_TalonSRX(ports.ballsystem.indexWheel)
        self.lowerConveyorMotor = WPI_TalonSRX(ports.ballsystem.lowerConveyor)
        self.verticalConveyorMotor = WPI_TalonSRX(ports.ballsystem.verticalConveyor)

        self.indexWheelMotor.setNeutralMode(NeutralMode.Brake)
        self.lowerConveyorMotor.setNeutralMode(NeutralMode.Brake)
        self.verticalConveyorMotor.setNeutralMode(NeutralMode.Brake)

        self.indexWheelMotor.setInverted(True)

    def runIndex(self):
        self.indexWheelMotor.set(ControlMode.PercentOutput, 0.8)

    def runLowerConveyor(self):
        self.lowerConveyorMotor.set(ControlMode.PercentOutput, 0.8)

    def runVerticalConveyor(self):
        self.verticalConveyorMotor.set(ControlMode.PercentOutput, 0.8)

    def reverseIndex(self):
        self.indexWheelMotor.set(ControlMode.PercentOutput, -0.5)

    def reverseLowerConveyor(self):
        self.lowerConveyorMotor.set(ControlMode.PercentOutput, -0.5)

    def reverseVerticalConveyor(self):
        self.verticalConveyorMotor.set(ControlMode.PercentOutput, -0.5)

    def stopIndex(self):
        self.indexWheelMotor.stopMotor()

    def stopLowerConveyor(self):
        self.lowerConveyorMotor.stopMotor()

    def stopVerticalConveyor(self):
        self.verticalConveyorMotor.stopMotor()

    def runIndexWithVertical(self):
        self.runIndex()
        self.runVerticalConveyor()

    def reverseIndexWithVertical(self):
        self.reverseIndex()
        self.reverseVerticalConveyor()

    def stopIndexWithVertical(self):
        self.stopIndex()
        self.stopVerticalConveyor()

    def runAll(self):
        self.runIndex()
        self.runLowerConveyor()
        self.runVerticalConveyor()

    def reverseAll(self):
        self.reverseIndex()
        self.reverseLowerConveyor()
        self.reverseVerticalConveyor()

    def stopAll(self):
        self.stopIndex()
        self.stopLowerConveyor()
        self.stopVerticalConveyor()
