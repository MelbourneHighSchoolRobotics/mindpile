from mindpile.Mapping.utils import MethodCall

@MethodCall(target="Comparison_Equal.vix", x=float, y=float, Result=bool)
def equal():
    return '''
        Result = x == y
    '''

@MethodCall(target="Comparison_NotEqual.vix", x=float, y=float, Result=bool)
def notEqual():
    return '''
        Result = x != y
    '''

@MethodCall(target="Comparison_Greater.vix", x=float, y=float, Result=bool)
def greater():
    return '''
        Result = x > y
    '''

@MethodCall(target="Comparison_GreaterEqual.vix", x=float, y=float, Result=bool)
def greaterEqual():
    return '''
        Result = x >= y
    '''

@MethodCall(target="Comparison_Less.vix", x=float, y=float, Result=bool)
def less():
    return '''
        Result = x < y
    '''

@MethodCall(target="Comparison_LessEqual.vix", x=float, y=float, Result=bool)
def lessEqual():
    return '''
        Result = x <= y
    '''
