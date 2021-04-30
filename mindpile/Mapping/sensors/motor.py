from mindpile.Mapping.types import OutPort
from mindpile.Mapping.utils import MethodCall

@MethodCall(target="RotationValue.vix", MotorPort=OutPort, Degrees=float)
def motorDegrees():
    return '''
        Degrees = m(MotorPort).position / m(MotorPort).count_per_rot * 360
    '''

@MethodCall(target="RotationValueRotations.vix", MotorPort=OutPort, Rotations=float)
def motorRotations():
    return '''
        Degrees = m(MotorPort).position / m(MotorPort).count_per_rot
    '''

@MethodCall(target="MotorSpeedSensor.vix", MotorPort=OutPort, Speed=float)
def motorPower():
    return '''
        Speed = m(MotorPort).duty_cycle
    '''

@MethodCall(target="RotationDegreesCompare.vix", MotorPort=OutPort, Comparison=int, ThresholdDegrees=float, Result=bool, Degrees=float)
def motorDegreesCompare():
    return '''
        Degrees = m(MotorPort).position / m(MotorPort).count_per_rot * 360
        Result = compare(Comparison, Degrees, ThresholdDegrees)
    '''

@MethodCall(target="RotationRotationsCompare.vix", MotorPort=OutPort, Comparison=int, ThresholdRotations=float, Result=bool, Rotations=float)
def motorDegreesCompare():
    return '''
        Rotations = m(MotorPort).position / m(MotorPort).count_per_rot
        Result = compare(Comparison, Rotations, ThresholdRotations)
    '''

@MethodCall(target="MotorSpeedCompare.vix", MotorPort=OutPort, Comparison=int, ThresholdSpeed=float, Result=bool, Speed=float)
def motorPowerCompare():
    return '''
        Speed = m(MotorPort).duty_cycle
        Result = compare(Comparison, Speed, ThresholdSpeed)
    '''
