from mindpile.Mapping.utils import MethodCall

@MethodCall(target="RandomSingle.vix", Lower=float, Upper=float, Number=float)
def randomNumeric():
    return '''
        Number = random.uniform(Lower, Upper)
    '''

@MethodCall(target="RandomBoolean.vix", PercentTrue=float, Result=bool)
def randomBoolean():
    return '''
        Result = random.random() * 100 <= PercentTrue
    '''
