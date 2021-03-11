from .types import Local
from .utils import MethodCall

@MethodCall(target="LoopIndex.vix", LoopIndex=int, i=Local(0))
def loopIndex():
    return '''
        LoopIndex = i
        i += 1
    '''

@MethodCall(target="StopNever.vix", Result=bool)
def stopNever():
    return '''
        Result = False
    '''
