from mindpile.Mapping.utils import MethodCall

@MethodCall(target="Round_Nearest.vix", Input=float, OutputResult=float)
def roundNearest():
    return '''
        OutputResult = round(Input)
    '''

@MethodCall(target="Round_Up.vix", Input=float, OutputResult=float)
def roundUp():
    return '''
        OutputResult = math.ceil(Input)
    '''

@MethodCall(target="Round_Down.vix", Input=float, OutputResult=float)
def roundDown():
    return '''
        OutputResult = math.floor(Input)
    '''

@MethodCall(target="Round_Truncate.vix", Input=float, NumberofDecimals=int, OutputResult=float)
def roundTruncate():
    return '''
        OutputResult = round(Input, NumberofDecimals)
    '''
