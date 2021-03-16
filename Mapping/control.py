from .utils import MethodCall

@MethodCall(target="LoopIndex.vix", LoopIterationCount=int, LoopIndex=int)
def loopIndex():
    return '''
        LoopIndex = LoopIterationCount - 1
    '''

@MethodCall(target="StopAfterNumberIterations.vix", IterationsToRun=int, LoopIterationCount=int, Result=bool)
def stopAfterNumberIterations():
    return '''
        Result = LoopIterationCount >= IterationsToRun
    '''

@MethodCall(target="StopIfTrue.vix", DoStop=bool, Result=bool)
def stopIfTrue():
    return '''
        Result = DoStop
    '''

@MethodCall(target="StopNever.vix", Result=bool)
def stopNever():
    return '''
        Result = False
    '''

@MethodCall(target="TimeCompareLoop.vix", HowLong=float, Result=bool, LoopEnterTime=float)
def timeCompareLoop():
    return '''
        Result = time.time() >= LoopEnterTime + HowLong
    '''
