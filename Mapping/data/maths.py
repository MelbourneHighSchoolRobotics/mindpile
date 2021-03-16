from Mapping.types import InPort, OutPort, List
from Mapping.utils import MethodCall, Requires, Setup

# TODO: implement advanced maths block

@MethodCall(target="Arithmetic_Add.vix", X=float, Y=float, Result=float)
def add():
    return '''
        Result = X + Y
    '''

@MethodCall(target="Arithmetic_Subtract.vix", X=float, Y=float, Result=float)
def sub():
    return '''
        Result = X - Y
    '''

@MethodCall(target="Arithmetic_Divide.vix", X=float, Y=float, Result=float)
def div():
    return '''
        Result = X / Y
    '''

@MethodCall(target="Arithmetic_Multiply.vix", X=float, Y=float, Result=float)
def mul():
    return '''
        Result = X * Y
    '''

@MethodCall(target="Arithmetic_AbsoluteValue.vix", X=float, Result=float)
def absolute():
    return '''
        Result = abs(X)
    '''

@MethodCall(target="Arithmetic_SquareRoot.vix", X=float, Result=float)
def sqrt():
    return '''
        Result = math.sqrt(X)
    '''

@MethodCall(target="Arithmetic_Power.vix", Base=float, Exponent=float, Result=float)
def power():
    return '''
        Result = math.pow(Base, Exponent)
    '''
