from Mapping.types import InPort, OutPort, List
from Mapping.utils import MethodCall, Requires, Setup

@MethodCall(target="X3.Lib:GlobalConstBoolean", valueIn=bool, valueOut=bool)
def constBoolean():
    return '''
        valueOut = valueIn
    '''

@MethodCall(target="X3.Lib:GlobalConstBooleanArray", valueIn=List(bool), valueOut=List(bool))
def constBooleanArray():
    return '''
        valueOut = valueIn
    '''

@MethodCall(target="X3.Lib:GlobalConstSingle", valueIn=float, valueOut=float)
def constNumber():
    return '''
        valueOut = valueIn
    '''

@MethodCall(target="X3.Lib:GlobalConstNumericArray", valueIn=List(float), valueOut=List(float))
def constNumberArray():
    return '''
        valueOut = valueIn
    '''

@MethodCall(target="X3.Lib:GlobalConstString", valueIn=str, valueOut=str)
def constString():
    return '''
        valueOut = valueIn
    '''
