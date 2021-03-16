from Mapping.types import InPort, OutPort, List
from Mapping.utils import MethodCall, Requires, Setup

@Setup
def motorSetup():
    return '''
        class MotorDict(dict):
            def __init__(self):
                self.motors = {}

            def __getitem__(self, key):
                motor =  self.motors.get(key)
                if motor is not None:
                    return motor
                motor = ev3dev2.motor.Motor(address=key)
                self.motors[key] = motor
                return motor
        __motors = MotorDict()
    '''

@MethodCall(target="MediumMotorUnlimited.vix", MotorPort=OutPort, Speed=float)
@Requires(motorSetup)
def mediumMotorUnlimited():
    return '''
        __motors[MotorPort].on(speed=Speed)
    '''

@MethodCall(target="MediumMotorDistanceRotations.vix", MotorPort=OutPort, Speed=float, Rotations=float, BrakeAtEnd=bool)
@Requires(motorSetup)
def mediumMotorDistanceRotations():
    return '''
        __motors[MotorPort].on_for_rotations(speed=Speed, rotations=Rotations, brake=BrakeAtEnd)
    '''


