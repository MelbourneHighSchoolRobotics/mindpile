from mindpile.Mapping.utils import MethodCall

@MethodCall(target="ConcatenateStrings.vix", A=str, B=str, C=str, Result=str)
def concatenate():
    return '''
        Result = f"{A}{B}{C}"
    '''
