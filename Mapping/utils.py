import ast
from collections import OrderedDict
import copy
import inspect
import functools
import textwrap
from Utility.memo import memoise
from .types import EV3Type

methods = {}
setupCode = OrderedDict()

def boolParser(input: str):
    return input == "True"

def MethodCall(target: str):
    def decorator(func):
        # Memoise the heavy lifting of template generation so it is only run once and only if this MethodCall is used
        @memoise
        def memo():
            parsers = {}
            parameters = inspect.signature(func).parameters
            for param in parameters.values():
                name = param.name
                annotation = param.annotation

                parser = None
                if annotation == inspect.Parameter.empty:
                    raise Exception("Mapping must contain type annotations")
                elif annotation == int:
                    parser = int
                elif annotation == str:
                    parser = str
                elif annotation == bool:
                    parser = boolParser
                elif issubclass(annotation, EV3Type):
                    parser = annotation.parse
                else:
                    raise Exception(f"Mapping parameter {name} is of an unknown type {annotation}")
                
                parsers[name] = parser

            # Get the AST template
            fakeArgs = { k: None for k in parameters.keys() }
            stringTemplate = func(**fakeArgs)
            tree = ast.parse(textwrap.dedent(stringTemplate))

            class Template(ast.NodeTransformer):
                def __init__(self, substitutions):
                    for name in parameters.keys():
                        if substitutions.get(name) is None:
                            raise Exception(f"Couldn't map to parameter {name} for {target}")

                    self.substitutions = substitutions

                def visit_Name(self, node: ast.Name):
                    name = node.id
                    if parsers.get(name) is not None:
                        parser = parsers[name]
                        value = self.substitutions[name]
                        if isinstance(value, ast.AST):
                            return value
                        else:
                            return ast.Constant(parser(value))
                    return node
                
                def run(self):
                    return self.visit(copy.deepcopy(tree))

            return Template
        
        @functools.wraps(func)
        def wrappedFunc(**kwargs) -> ast.AST:
            Template = memo()
            return Template(kwargs).run()

        methods[target] = wrappedFunc
        return wrappedFunc
    return decorator

def Setup(func):
    @functools.wraps(func)
    @memoise
    def wrapped():
        stringTemplate = func()
        tree = ast.parse(textwrap.dedent(stringTemplate))
        return tree
    return wrapped

def Requires(prereq):
    def decorator(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            if setupCode.get(prereq) is None:
                tree = prereq()
                setupCode[prereq] = tree
            return func(*args, **kwargs)
        return wrapped
    return decorator

def startCodeGen():
    setupCode.clear()

def generateSetupAST():
    tree = ast.parse("")
    for block in setupCode.values():
        tree.body += block.body
    return tree
