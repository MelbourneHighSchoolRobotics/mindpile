from mindpile.Mapping.types import InPort, OutPort, List
from mindpile.Mapping.utils import MethodCall, Requires, Setup

@MethodCall(target="ConcatenateStrings.vix", A=str, B=str, C=str, Result=str)
def concatenate():
    return '''
        Result = f"{A}{B}{C}"
    '''
