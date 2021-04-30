from mindpile.Mapping.types import OutPortPair
from mindpile.Mapping.utils import MethodCall, Requires, Setup

@Setup
def steeringSetup():
    return '''
        from ev3dev2.motor import MoveSteering

        steeringControllers = {}
        def steering(port):
            if port is None:
                raise Exception("Steering block does not have a port specified")
            port = int(port)

            controller = steeringControllers.get(port)
            if controller is None:
                portLeft = f"out{chr((port // 10) + 64)}"
                portRight = f"out{chr((port % 10) + 64)}"
                controller = MoveSteering(portLeft, portRight)
                steeringControllers[port] = controller
            return controller
    '''

@MethodCall(target="MoveStop.vix", Ports=OutPortPair, BrakeAtEnd=bool)
@Requires(steeringSetup)
def steeringStop():
    return '''
        steering(Ports).off(brake=BrakeAtEnd)
    '''

@MethodCall(target="MoveUnlimited.vix", Ports=OutPortPair, Steering=float, Speed=float)
@Requires(steeringSetup)
def steeringUnlimited():
    return '''
        steering(Ports).on(steering=Steering, speed=Speed)
    '''

@MethodCall(target="MoveTime.vix", Ports=OutPortPair, Steering=float, Speed=float, Seconds=float, BrakeAtEnd=bool)
@Requires(steeringSetup)
def steeringSeconds():
    return '''
        steering(Ports).on_for_seconds(steering=Steering, speed=Speed, seconds=Seconds, brake=BrakeAtEnd)
    '''

@MethodCall(target="MoveDistance.vix", Ports=OutPortPair, Steering=float, Speed=float, Degrees=float, BrakeAtEnd=bool)
@Requires(steeringSetup)
def steeringDegrees():
    return '''
        steering(Ports).on_for_degrees(steering=Steering, speed=Speed, degrees=Degrees, brake=BrakeAtEnd)
    '''

@MethodCall(target="MoveDistanceRotations.vix", Ports=OutPortPair, Steering=float, Speed=float, Rotations=float, BrakeAtEnd=bool)
@Requires(steeringSetup)
def steeringRotations():
    return '''
        steering(Ports).on_for_rotations(steering=Steering, speed=Speed, rotations=Rotations, brake=BrakeAtEnd)
    '''
