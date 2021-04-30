from mindpile.Mapping.types import OutPortPair
from mindpile.Mapping.utils import MethodCall, Requires, Setup

@Setup
def tankSetup():
    return '''
        from ev3dev2.motor import MoveTank

        tankControllers = {}
        def tank(port):
            if port is None:
                raise Exception("Tank block does not have a port specified")
            port = int(port)

            controller = tankControllers.get(port)
            if controller is None:
                portLeft = f"out{chr((port // 10) + 64)}"
                portRight = f"out{chr((port % 10) + 64)}"
                controller = MoveTank(portLeft, portRight)
                tankControllers[port] = controller
            return controller
    '''

@MethodCall(target="MoveTankStop.vix", Ports=OutPortPair, BrakeAtEnd=bool)
@Requires(tankSetup)
def tankStop():
    return '''
        tank(Ports).off(brake=BrakeAtEnd)
    '''

@MethodCall(target="MoveTankMode.vix", Ports=OutPortPair, SpeedLeft=float, SpeedRight=float)
@Requires(tankSetup)
def tankUnlimited():
    return '''
        tank(Ports).on(SpeedLeft, SpeedRight)
    '''

@MethodCall(target="MoveTankTime.vix", Ports=OutPortPair, SpeedLeft=float, SpeedRight=float, Seconds=float, BrakeAtEnd=bool)
@Requires(tankSetup)
def tankSeconds():
    return '''
        tank(Ports).on_for_seconds(SpeedLeft, SpeedRight, seconds=Seconds, brake=BrakeAtEnd)
    '''

@MethodCall(target="MoveTankDistance.vix", Ports=OutPortPair, SpeedLeft=float, SpeedRight=float, Degrees=float, BrakeAtEnd=bool)
@Requires(tankSetup)
def tankDegrees():
    return '''
        tank(Ports).on_for_degrees(SpeedLeft, SpeedRight, degrees=Degrees, brake=BrakeAtEnd)
    '''

@MethodCall(target="MoveTankDistanceRotations.vix", Ports=OutPortPair, SpeedLeft=float, SpeedRight=float, Rotations=float, BrakeAtEnd=bool)
@Requires(tankSetup)
def tankRotations():
    return '''
        tank(Ports).on_for_rotations(SpeedLeft, SpeedRight, rotations=Rotations, brake=BrakeAtEnd)
    '''
