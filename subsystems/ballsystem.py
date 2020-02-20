from .debuggablesubsystem import DebuggableSubsystem

from networktables import NetworkTables

from wpilib import DigitalInput

from ctre import ControlMode, WPI_TalonSRX, NeutralMode

import ports


class BallSystem(DebuggableSubsystem):
    '''Describe what this subsystem does.'''

    def __init__(self):
        super().__init__('BallSystem')
        self.lowerConveyorMotor = WPI_TalonSRX(ports.ballsystem.lowerConveyor)
        self.verticalConveyorMotor = WPI_TalonSRX(ports.ballsystem.verticalConveyor)

        self.lowerConveyorMotor.setNeutralMode(NeutralMode.Brake)
        self.verticalConveyorMotor.setNeutralMode(NeutralMode.Brake)

        self.shooting = False

        self.table = NetworkTables.getTable('BallSystem')

        self.shooterSensor = DigitalInput(ports.ballsystem.shooterSensor)
        self.horizontalBeltSensor = DigitalInput(ports.ballsystem.horizontalConveyorSensor)

    def runLowerConveyor(self):
        self.lowerConveyorMotor.set(ControlMode.PercentOutput, 0.8)
        self.table.putString('LowerConveyorStatus', 'Forward')

    def runLowerConveyorSlow(self):
        self.lowerConveyorMotor.set(ControlMode.PercentOutput, 0.4) # experiment
        self.table.putString('LowerConveyorStatus', 'Slow')

    def runVerticalConveyor(self):
        self.verticalConveyorMotor.set(ControlMode.PercentOutput, 1)
        self.table.putString('UpperConveyorStatus', 'Forward')

    def reverseLowerConveyor(self):
        self.lowerConveyorMotor.set(ControlMode.PercentOutput, -1)
        self.table.putString('LowerConveyorStatus', 'Reversing')

    def reverseVerticalConveyor(self):
        self.verticalConveyorMotor.set(ControlMode.PercentOutput, -1)
        self.table.putString('UpperConveyorStatus', 'Reversing')

    def stopLowerConveyor(self):
        self.lowerConveyorMotor.stopMotor()

    def stopVerticalConveyor(self):
        self.verticalConveyorMotor.stopMotor()

    def runAll(self):
        self.runLowerConveyor()
        self.runVerticalConveyor()

    def runLowSlowAndVertical(self): # lol that rhymes
        self.lowerConveyorMotor.set(0.1)
        self.runVerticalConveyor()

    def reverseAll(self):
        self.reverseLowerConveyor()
        self.reverseVerticalConveyor()

    def stopAll(self):
        self.stopLowerConveyor()
        self.stopVerticalConveyor()

    def setHorizontalBrake(self):
        self.lowerConveyorMotor.setNeutralMode(NeutralMode.Brake)

    def setHorizontalCoast(self):
        self.lowerConveyorMotor.setNeutralMode(NeutralMode.Coast)

    #def enableSensor(self):
        #self.horizontalBeltSensor.setEnabled(True)

    #def disableSensor(self):
        #self.horizontalBeltSensor.setEnabled(False)

    def updateNetworktables(self):
        self.table.putNumber('BallInChamber', (not self.horizontalBeltSensor.get()))

    def isBallPrimed(self):
        self.updateNetworktables()
        return not self.horizontalBeltSensor.get() # may need to invert

    def monitorBalls(self, startCount):
        if not self.shooterSensor.get() and not self.shooting: # is there something there that was not there last time?
            if startCount != 0:
                startCount -= 1
                self.table.putNumber('BallCount', self.ballCount)
            self.shooting = True
        elif self.shooterSensor.get(): # no ball present
            self.shooting = False # nothing there, spaced out.

        return startCount
