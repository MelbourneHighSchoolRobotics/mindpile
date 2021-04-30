from mindpile.Mapping.types import InPort, Local, List
from mindpile.Mapping.utils import MethodCall, Requires, Setup

@Setup
def colourSetup():
    return '''
        from ev3dev2.sensor.lego import ColorSensor
    '''

@MethodCall(target="ColorValue.vix", Port=InPort, Color=int)
@Requires(colourSetup)
def colourValue():
    return '''
        Color = s(Port, ColorSensor).color
    '''

@MethodCall(target="ColorReflectedIntensity.vix", Port=InPort, Value=int)
@Requires(colourSetup)
def colourReflected():
    return '''
        Value = s(Port, ColorSensor).reflected_light_intensity
    '''

@MethodCall(target="ColorAmbientIntensity.vix", Port=InPort, Value=int)
@Requires(colourSetup)
def colourAmbient():
    return '''
        Value = s(Port, ColorSensor).ambient_light_intensity
    '''

@MethodCall(target="ColorCompare.vix", Port=InPort, Setofcolors=List(int), Result=bool, Color=int)
@Requires(colourSetup)
def colourCompare():
    return '''
        Color = s(Port, ColorSensor).color
        Result = Color in Setofcolors
    '''

@MethodCall(target="ColorReflectedIntensityCompare.vix", Port=InPort, Comparison=int, Threshold=int, Result=bool, Value=int)
@Requires(colourSetup)
def colourCompare():
    return '''
        Value = s(Port, ColorSensor).reflected_light_intensity
        Result = compare(Comparison, Value, Threshold)
    '''

@MethodCall(target="ColorAmbientIntensityCompare.vix", Port=InPort, Comparison=int, Threshold=int, Result=bool, Value=int)
@Requires(colourSetup)
def colourCompare():
    return '''
        Value = s(Port, ColorSensor).ambient_light_intensity
        Result = compare(Comparison, Value, Threshold)
    '''

@MethodCall(target="ColorChange.vix", Port=InPort, Color=int, Result=bool, initValue=Local(None))
@Requires(colourSetup)
def colourChange():
    return '''
        Color = s(Port, ColorSensor).color
        if initValue is None:
            initValue = Color
        Result = Color != initValue
        if Result:
            initValue = None
    '''

@MethodCall(target="ColorReflectedIntensityChange.vix", Port=InPort, Direction=int, Amount=int, Value=int, Result=bool, initValue=Local(None))
@Requires(colourSetup)
def colourReflectedChange():
    return '''
        Value = s(Port, ColorSensor).reflected_light_intensity
        if initValue is None:
            initValue = Value
        Result = compareDirection(Direction, Amount, initValue, Value)
        if Result:
            initValue = None
    '''

@MethodCall(target="ColorAmbientIntensityChange.vix", Port=InPort, Direction=int, Amount=int, Value=int, Result=bool, initValue=Local(None))
@Requires(colourSetup)
def colourAmbientChange():
    return '''
        Value = s(Port, ColorSensor).ambient_light_intensity
        if initValue is None:
            initValue = Value
        Result = compareDirection(Direction, Amount, initValue, Value)
        if Result:
            initValue = None
    '''
