import ast
from mindpile.Mapping.types import Literal
from mindpile.Mapping.utils import MethodCall, DynamicMethodCall, Requires, Setup, p

@MethodCall(target="Arithmetic_Add.vix", X=float, Y=float, Result=float)
def add():
    return '''
        Result = X + Y
    '''

@MethodCall(target="Arithmetic_Subtract.vix", X=float, Y=float, Result=float)
def sub():
    return '''
        Result = X - Y
    '''

@MethodCall(target="Arithmetic_Divide.vix", X=float, Y=float, Result=float)
def div():
    return '''
        Result = X / Y
    '''

@MethodCall(target="Arithmetic_Multiply.vix", X=float, Y=float, Result=float)
def mul():
    return '''
        Result = X * Y
    '''

@MethodCall(target="Arithmetic_AbsoluteValue.vix", X=float, Result=float)
def absolute():
    return '''
        Result = abs(X)
    '''

@MethodCall(target="Arithmetic_SquareRoot.vix", X=float, Result=float)
def sqrt():
    return '''
        Result = math.sqrt(X)
    '''

@MethodCall(target="Arithmetic_Power.vix", Base=float, Exponent=float, Result=float)
def power():
    return '''
        Result = Base ** Exponent
    '''

@Setup
def advancedMathsSetup():
    return '''
        def sinDeg(x):
            return math.degrees(math.sin(x))
        def cosDeg(x):
            return math.degrees(math.cos(x))
        def tanDeg(x):
            return math.degrees(math.tan(x))
        def asinDeg(x):
            return math.degrees(math.asin(x))
        def acosDeg(x):
            return math.degrees(math.acos(x))
        def atanDeg(x):
            return math.degrees(math.atan(x))
    '''

@DynamicMethodCall(target="X3Placeholder_2A058539-ED76-4476-93FE-CCE8AA559C5A_MathEquation.vix", X=float, Y=float, C=float, D=float, Equation=Literal(str), Result=float)
@Requires(advancedMathsSetup)
def advancedMaths(X, Y, C, D, Equation, Result, **kwargs):
    tree = p(f'''
        Result = {Equation.lower()}
    ''', {
        "Result": Result,
        "a": X,
        "b": Y,
        "c": C,
        "d": D,
        "floor": ast.Attribute(value=ast.Name(id='math', ctx=ast.Load()), attr='floor', ctx=ast.Load()),
        "ceil": ast.Attribute(value=ast.Name(id='math', ctx=ast.Load()), attr='ceil', ctx=ast.Load()),
        "round": ast.Name(id="round", ctx=ast.Load()),
        "abs": ast.Name(id="abs", ctx=ast.Load()),
        # TODO: Check that log() is a log10 function
        "log": ast.Attribute(value=ast.Name(id='math', ctx=ast.Load()), attr='log10', ctx=ast.Load()),
        "ln": ast.Attribute(value=ast.Name(id='math', ctx=ast.Load()), attr='log', ctx=ast.Load()),
        "sin": ast.Name(id="sinDeg", ctx=ast.Load()),
        "cos": ast.Name(id="cosDeg", ctx=ast.Load()),
        "tan": ast.Name(id="tanDeg", ctx=ast.Load()),
        "asin": ast.Name(id="asinDeg", ctx=ast.Load()),
        "acos": ast.Name(id="acosDeg", ctx=ast.Load()),
        "atan": ast.Name(id="atanDeg", ctx=ast.Load()),
        "sqrt": ast.Attribute(value=ast.Name(id='math', ctx=ast.Load()), attr='sqrt', ctx=ast.Load()),
    })

    # Substitute the power (^) symbol with python's (**)
    # TODO: Ensure that power has highest order of operations in EV3 and it's same as python
    class Transformer(ast.NodeTransformer):
        def visit_BitXor(self, node: ast.BitXor):
            return ast.Pow()
    transformer = Transformer()
    transformer.visit(tree)

    return tree
