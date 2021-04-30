from mindpile.Mapping.utils import MethodCall

@MethodCall(target="Boolean_And.vix", A=bool, B=bool, Result=bool)
def booleanAnd():
    return '''
        Result = A and B
    '''

@MethodCall(target="Boolean_Or.vix", A=bool, B=bool, Result=bool)
def booleanOr():
    return '''
        Result = A or B
    '''

@MethodCall(target="Boolean_XOr.vix", A=bool, B=bool, Result=bool)
def booleanXOR():
    return '''
        Result = A != B
    '''

@MethodCall(target="Boolean_Not.vix", A=bool, Result=bool)
def booleanNot():
    return '''
        Result = not A
    '''
