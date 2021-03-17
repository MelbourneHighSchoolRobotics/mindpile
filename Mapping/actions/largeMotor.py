from Mapping.types import InPort, OutPort, List
from Mapping.utils import MethodCall, Requires, Setup

@Setup
def largeMotorSetup():
    return '''
        from ev3dev2.motor import LargeMotor
    '''

@MethodCall(target="MotorStop.vix", MotorPort=OutPort, BrakeAtEnd=bool)
@Requires(largeMotorSetup)
def largeMotorStop():
    return '''
        d(MotorPort, LargeMotor).stop(stop_action=("hold" if BrakeAtEnd else "coast"))
    '''

@MethodCall(target="MotorUnlimited.vix", MotorPort=OutPort, Speed=float)
@Requires(largeMotorSetup)
def largeMotorUnlimited():
    return '''
        d(MotorPort, LargeMotor).on(speed=Speed)
    '''

@MethodCall(target="MotorTime.vix", MotorPort=OutPort, Speed=float, Seconds=float, BrakeAtEnd=bool)
@Requires(largeMotorSetup)
def largeMotorSeconds():
    return '''
        d(MotorPort, LargeMotor).on_for_seconds(speed=Speed, seconds=Seconds, brake=BrakeAtEnd)
    '''

@MethodCall(target="MotorDistance.vix", MotorPort=OutPort, Speed=float, Degrees=float, BrakeAtEnd=bool)
@Requires(largeMotorSetup)
def largeMotorDegrees():
    return '''
        d(MotorPort, LargeMotor).on_for_degrees(speed=Speed, degrees=Degrees, brake=BrakeAtEnd)
    '''

@MethodCall(target="MotorDistanceRotations.vix", MotorPort=OutPort, Speed=float, Rotations=float, BrakeAtEnd=bool)
@Requires(largeMotorSetup)
def largeMotorRotations():
    return '''
        d(MotorPort, LargeMotor).on_for_rotations(speed=Speed, rotations=Rotations, brake=BrakeAtEnd)
    '''
