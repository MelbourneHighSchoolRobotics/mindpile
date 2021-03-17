from Mapping.types import InPort, OutPort, List
from Mapping.utils import MethodCall, Requires, Setup

@Setup
def mediumMotorSetup():
    return '''
        from ev3dev2.motor import MediumMotor
    '''

@MethodCall(target="MediumMotorStop.vix", MotorPort=OutPort, BrakeAtEnd=bool)
@Requires(mediumMotorSetup)
def mediumMotorStop():
    return '''
        d(MotorPort, MediumMotor).stop(stop_action=("hold" if BrakeAtEnd else "coast"))
    '''

@MethodCall(target="MediumMotorUnlimited.vix", MotorPort=OutPort, Speed=float)
@Requires(mediumMotorSetup)
def mediumMotorUnlimited():
    return '''
        d(MotorPort, MediumMotor).on(speed=Speed)
    '''

@MethodCall(target="MediumMotorTime.vix", MotorPort=OutPort, Speed=float, Seconds=float, BrakeAtEnd=bool)
@Requires(mediumMotorSetup)
def mediumMotorSeconds():
    return '''
        d(MotorPort, MediumMotor).on_for_seconds(speed=Speed, seconds=Seconds, brake=BrakeAtEnd)
    '''

@MethodCall(target="MediumMotorDistance.vix", MotorPort=OutPort, Speed=float, Degrees=float, BrakeAtEnd=bool)
@Requires(mediumMotorSetup)
def mediumMotorDegrees():
    return '''
        d(MotorPort, MediumMotor).on_for_degrees(speed=Speed, degrees=Degrees, brake=BrakeAtEnd)
    '''

@MethodCall(target="MediumMotorDistanceRotations.vix", MotorPort=OutPort, Speed=float, Rotations=float, BrakeAtEnd=bool)
@Requires(mediumMotorSetup)
def mediumMotorRotations():
    return '''
        d(MotorPort, MediumMotor).on_for_rotations(speed=Speed, rotations=Rotations, brake=BrakeAtEnd)
    '''
