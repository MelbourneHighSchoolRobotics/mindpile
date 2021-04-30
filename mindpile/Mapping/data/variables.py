from mindpile.Mapping.types import List
from mindpile.Mapping.utils import MethodCall, Requires, Setup

@Setup
def variablesSetup():
    return '''
        userVariables = {}
    '''

@MethodCall(target="X3.Lib:GlobalGetBoolean", valueOut=bool, name=str)
@MethodCall(target="X3.Lib:GlobalGetBooleanArray", valueOut=List(bool), name=str)
@MethodCall(target="X3.Lib:GlobalGetNumericArray", valueOut=List(float), name=str)
@MethodCall(target="X3.Lib:GlobalGetSingle", valueOut=float, name=str)
@MethodCall(target="X3.Lib:GlobalGetString", valueOut=str, name=str)
@Requires(variablesSetup)
def getVariable():
    return '''
        valueOut = userVariables[name]
    '''

@MethodCall(target="X3.Lib:GlobalSetBoolean", name=str, valueIn=bool)
@MethodCall(target="X3.Lib:GlobalSetBooleanArray", name=str, valueIn=List(bool))
@MethodCall(target="X3.Lib:GlobalSetNumericArray", name=str, valueIn=List(float))
@MethodCall(target="X3.Lib:GlobalSetSingle", name=str, valueIn=float)
@MethodCall(target="X3.Lib:GlobalSetString", name=str, valueIn=str)
@Requires(variablesSetup)
def setVariable():
    return '''
        userVariables[name] = valueIn
    '''
