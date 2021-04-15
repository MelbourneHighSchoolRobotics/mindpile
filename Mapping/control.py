from .types import Literal
from .utils import MethodCall, DynamicMethodCall, p

@MethodCall(target="CaseSelector_Boolean.vix", Boolean=bool, Result=bool)
def caseSelectorBoolean():
    return '''
        Result = Boolean
    '''

@MethodCall(target="CaseSelector_Numeric.vix", Number=int, Result=int)
def caseSelectorNumeric():
    return '''
        Result = Number
    '''

@MethodCall(target="CaseSelector_String.vix", String=str, Result=str)
def caseSelectorString():
    return '''
        Result = String
    '''

@MethodCall(target="LoopIndex.vix", LoopIterationCount=int, LoopIndex=int)
def loopIndex():
    return '''
        LoopIndex = LoopIterationCount - 1
    '''

@DynamicMethodCall(target="ToggleInterrupt.vix", InterruptName=Literal(str), LoopLabel=Literal(str))
def loopInterrupt(InterruptName, LoopLabel):
    if LoopLabel != InterruptName:
        raise Exception(f"Loop Interrupt {InterruptName} only supports breaking a loop it is directly inside")

    return p('''
        break
    ''')

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

@MethodCall(target="TimeCompare.vix", HowLong=float, Result=bool, WaitEnterTime=float)
def timeCompareWait():
    return '''
        Result = time.time() >= WaitEnterTime + HowLong
    '''
