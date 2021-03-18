from Mapping.types import InPort, OutPort, List
from Mapping.utils import MethodCall, Requires, Setup

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
