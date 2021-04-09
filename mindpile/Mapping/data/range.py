from mindpile.Mapping.types import InPort, OutPort, List
from mindpile.Mapping.utils import MethodCall, Requires, Setup

@MethodCall(target="InsideRange.vix", TestValue=float, LowerBound=float, UpperBound=float, Result=bool)
def insideRange():
    return '''
        Result = TestValue >= LowerBound and TestValue <= UpperBound
    '''

@MethodCall(target="OutsideRange.vix", TestValue=float, LowerBound=float, UpperBound=float, Result=bool)
def outsideRange():
    return '''
        Result = TestValue < LowerBound and TestValue > UpperBound
    '''
