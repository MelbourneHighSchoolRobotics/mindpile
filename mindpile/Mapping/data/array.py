from mindpile.Mapping.types import List
from mindpile.Mapping.utils import MethodCall

@MethodCall(target="ArrayBuild.vix", arrayInNumeric=List(float), valueIn=float, arrayOutNumeric=List(float))
def arrayAppendNumeric():
    return '''
        arrayOutNumeric = [*arrayInNumeric, valueIn]
    '''

@MethodCall(target="ArrayBuildBoolean.vix", arrayInBoolean=List(bool), valueIn=bool, arrayOutBoolean=List(bool))
def arrayAppendBoolean():
    return '''
        arrayOutBoolean = [*arrayInBoolean, valueIn]
    '''

@MethodCall(target="ArrayReadAtIndex.vix", arrayInNumeric=List(float), Index=int, valueOut=float)
def arrayReadNumeric():
    return '''
        valueOut = arrayInNumeric[Index]
    '''

@MethodCall(target="ArrayReadAtIndexBoolean.vix", arrayInBoolean=List(bool), Index=int, valueOut=bool)
def arrayReadBoolean():
    return '''
        valueOut = arrayInBoolean[Index]
    '''

@MethodCall(target="ArrayWriteAtIndex.vix", arrayInNumeric=List(float), Index=int, valueIn=float, arrayOutNumeric=List(float))
def arrayWriteNumeric():
    return '''
        arrayOutNumeric = list(arrayInNumeric)
        arrayOutNumeric[Index] = valueIn
    '''

@MethodCall(target="ArrayWriteAtIndexBoolean.vix", arrayInBoolean=List(bool), Index=int, valueIn=bool, arrayOutBoolean=List(bool))
def arrayWriteBoolean():
    return '''
        arrayOutBoolean = list(arrayInBoolean)
        arrayOutBoolean[Index] = valueIn
    '''

@MethodCall(target="ArrayGetSize.vix", arrayInNumeric=List(float), Size=int)
def arrayLengthNumeric():
    return '''
        Size = len(arrayInNumeric)
    '''

@MethodCall(target="ArrayGetSizeBoolean.vix", arrayInBoolean=List(bool), Size=int)
def arrayLengthBoolean():
    return '''
        Size = len(arrayInBoolean)
    '''
