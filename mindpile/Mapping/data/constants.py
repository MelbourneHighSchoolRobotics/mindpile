from mindpile.Mapping.types import List
from mindpile.Mapping.utils import MethodCall

@MethodCall(target="X3.Lib:GlobalConstBoolean", valueIn=bool, valueOut=bool)
@MethodCall(target="X3.Lib:GlobalConstBooleanArray", valueIn=List(bool), valueOut=List(bool))
@MethodCall(target="X3.Lib:GlobalConstSingle", valueIn=float, valueOut=float)
@MethodCall(target="X3.Lib:GlobalConstNumericArray", valueIn=List(float), valueOut=List(float))
@MethodCall(target="X3.Lib:GlobalConstString", valueIn=str, valueOut=str)
def const():
    return '''
        valueOut = valueIn
    '''
