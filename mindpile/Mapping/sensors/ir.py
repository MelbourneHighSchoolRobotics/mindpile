from mindpile.Mapping.types import InPort, List, Local
from mindpile.Mapping.utils import MethodCall, Requires, Setup

@Setup
def irSetup():
    return '''
        from ev3dev2.sensor.lego import InfraredSensor
    '''

@MethodCall(target="IRProximity.vix", Port=InPort, Proximity=int)
@Requires(irSetup)
def irProximity():
    return '''
        Proximity = s(Port, InfraredSensor).proximity
    '''

@MethodCall(target="IRSeeker.vix", Port=InPort, Channel=int, Heading=int, Proximity=int, Valid=bool)
@Requires(irSetup)
def irSeeker():
    return '''
        Heading, Proximity = s(Port, InfraredSensor).heading_and_distance(Channel)
        Valid = Proximity is not None
        if not Valid:
            Proximity = 100
    '''

@MethodCall(target="IRRemote.vix", Port=InPort, Channel=int, Button=int)
@Requires(irSetup)
def irRemote():
    return '''
        temp = s(Port, InfraredSensor)
        temp._ensure_mode(InfraredSensor.MODE_IR_REMOTE)
        Button = temp.value(Channel - 1)
    '''

@MethodCall(target="IRProximityCompare.vix", Port=InPort, Comparison=int, Threshold=int, Result=bool, Proximity=int)
@Requires(irSetup)
def irProximityCompare():
    return '''
        Proximity = s(Port, InfraredSensor).proximity
        Result = compare(Comparison, Proximity, Threshold)
    '''

@MethodCall(target="IRTrackerCompareHeading.vix", Port=InPort, Channel=int, Comparison=int, HeadingThreshold=int, Result=bool, Heading=int)
@Requires(irSetup)
def irSeekerCompareHeading():
    return '''
        Heading = s(Port, InfraredSensor).heading(Channel)
        Result = compare(Comparison, Heading, HeadingThreshold)
    '''

@MethodCall(target="IRTrackerCompareProximity.vix", Port=InPort, Channel=int, Comparison=int, Threshold=int, Result=bool, Proximity=int)
@Requires(irSetup)
def irSeekerCompareDistance():
    return '''
        Proximity = s(Port, InfraredSensor).distance(Channel)
        if Proximity is None:
            Proximity = 100
            Result = False
        else:
            Result = compare(Comparison, Proximity, Threshold)
    '''

@MethodCall(target="IRRemoteCompare.vix", Port=InPort, Channel=int, SetofremotebuttonIDs=List(int), Result=bool, Button=int)
@Requires(irSetup)
def irRemote():
    return '''
        temp = s(Port, InfraredSensor)
        temp._ensure_mode(InfraredSensor.MODE_IR_REMOTE)
        Button = temp.value(Channel - 1)
        Result = Button in SetofremotebuttonIDs
    '''

@MethodCall(target="IRProximityChange.vix", Port=InPort, Direction=int, Amount=int, Result=bool, Proximity=int, initValue=Local(None))
@Requires(irSetup)
def irProximityChange():
    return '''
        Proximity = s(Port, InfraredSensor).proximity
        if initValue is None:
            initValue = Proximity
        Result = compareDirection(Direction, Amount, initValue, Proximity)
        if Result:
            initValue = None
    '''

@MethodCall(target="IRTrackerChangeHeading.vix", Port=InPort, Direction=int, HeadingAmount=int, Result=bool, Heading=int, initValue=Local(None))
@Requires(irSetup)
def irSeekerChangeHeading():
    return '''
        Heading = s(Port, InfraredSensor).heading(Channel)
        if initValue is None:
            initValue = Heading
        Result = compareDirection(Direction, Amount, initValue, Heading)
        if Result:
            initValue = None
    '''

@MethodCall(target="IRTrackerChangeProximity.vix", Port=InPort, Direction=int, Amount=int, Result=bool, Proximity=int, initValue=Local(None))
@Requires(irSetup)
def irSeekerChangeDistance():
    return '''
        Proximity = s(Port, InfraredSensor).distance(Channel)
        if Proximity is None:
            Proximity = 100
        if initValue is None:
            initValue = Proximity
        Result = compareDirection(Direction, Amount, initValue, Proximity)
        if Result:
            initValue = None
    '''

@MethodCall(target="IRRemoteChange.vix", Port=InPort, Channel=int, Result=bool, Button=int, initValue=Local(None))
@Requires(irSetup)
def irProximityChange():
    return '''
        temp = s(Port, InfraredSensor)
        temp._ensure_mode(InfraredSensor.MODE_IR_REMOTE)
        Button = temp.value(Channel - 1)
        if Button is None:
            initValue = Button
        Result = Button != initValue
        if Result:
            initValue = None
    '''
