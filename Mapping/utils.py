import ast
from collections import OrderedDict
import copy
import functools
import textwrap
from Utility.memo import memoise
from .types import EV3Type, Local
from .boilerplate import boilerplate

methods = {}
setupCode = OrderedDict()
global_var_count = 0

def newGlobalName():
    global global_var_count
    name = f"var_{global_var_count}"
    global_var_count += 1
    return name

def newTree():
    return ast.parse("")

def boolParser(input: str):
    return input == "True"

def MethodCall(target: str, **parameters):
    def decorator(func):
        # Memoise the heavy lifting of template generation so it is only run once and only if this MethodCall is used
        @memoise
        def memo():
            parsers = {}
            local_variables = {}

            for name, type in parameters.items():
                parser = None
                if type == int:
                    parser = int
                elif type == str:
                    parser = str
                elif type == bool:
                    parser = boolParser
                elif type == float:
                    parser = float
                elif isinstance(type, Local):
                    local_variables[name] = type
                elif issubclass(type, EV3Type):
                    parser = type.parse
                else:
                    raise Exception(f"Mapping parameter {name} is of an unknown type {type}")
                
                if parser is not None:
                    parsers[name] = parser

            # Get the AST template
            stringTemplate = func()
            tree = ast.parse(textwrap.dedent(stringTemplate))

            class Template(ast.NodeTransformer):
                def __init__(self, substitutions):
                    for name in parsers.keys():
                        if substitutions.get(name) is None:
                            raise Exception(f"Couldn't map to parameter {name} for {target}")

                    self.substitutions = substitutions
                    self.local_to_global_map = {}

                def visit_Name(self, node: ast.Name):
                    name = node.id
                    if parsers.get(name) is not None:
                        parser = parsers[name]
                        value = self.substitutions[name]
                        if isinstance(value, ast.AST):
                            return value
                        else:
                            return ast.Constant(parser(value))
                    elif local_variables.get(name) is not None:
                        global_name = self.local_to_global_map.get(name)
                        if global_name is None:
                            global_name = newGlobalName()
                            tree = newTree()
                            tree.body = [
                                ast.Assign(
                                    targets=[ast.Name(id=global_name, ctx=ast.Store())],
                                    value=ast.Constant(type.initial_value)
                                )
                            ]
                            setupCode[global_name] = tree
                            self.local_to_global_map[name] = global_name
                        return ast.Name(id=global_name, ctx=node.ctx)
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
    global global_var_count
    setupCode.clear()
    global_var_count = 0

def generateSetupAST():
    tree = newTree()
    tree.body.append(ast.parse(boilerplate).body)
    for block in setupCode.values():
        tree.body += block.body
    return tree
