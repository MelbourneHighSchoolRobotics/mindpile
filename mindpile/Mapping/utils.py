import ast
from collections import OrderedDict
import copy
import functools
import textwrap
from mindpile.Utility.memo import memoise
from .types import Local, Literal, get_parser
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

def substitute_tree(tree):
    class Template(ast.NodeTransformer):
        def __init__(self, substitutions={}) -> None:
            self.substitutions = substitutions

        def visit_Name(self, node: ast.Name):
            name = node.id
            if self.substitutions.get(name) is not None:
                value = self.substitutions[name]
                if isinstance(value, ast.AST):
                    return value
                else:
                    return ast.Constant(value)
            return node
        
        def run(self):
            return self.visit(copy.deepcopy(tree))
    
    def run(substitutions={}):
        template = Template(substitutions)
        return template.run()

    return run

def parse_code(code, substitutions={}):
    tree = ast.parse(textwrap.dedent(code))
    if len(substitutions) == 0:
        return tree
    sub = substitute_tree(tree)
    return sub(substitutions)
p = parse_code

def parse_parameter_types(parameters):
    types = {}
    local_variables = {}
    for name, type in parameters.items():
        if isinstance(type, Local):
            local_variables[name] = type
        else:
            parser = get_parser(type)
            if parser is None:
                raise Exception(f"Mapping parameter {name} is of an unknown type {type}")
            types[name] = type
    return types, local_variables

def create_parameter_substitutions(target, parameters, types, local_variables):
    substitutions = {}

    for name, type in types.items():
        if parameters.get(name) is None:
            raise Exception(f"Couldn't map to parameter {name} for {target}")
        value = parameters[name]
        if isinstance(value, ast.AST) and isinstance(type, Literal):
            raise Exception(f"Expected literal for parameter {name} of {target}, got variable")
        substitutions[name] = parameters[name]
    
    for name, type in local_variables.items():
        global_name = newGlobalName()
        tree = newTree()
        tree.body = [
            ast.Assign(
                targets=[ast.Name(id=global_name, ctx=ast.Store())],
                value=ast.Constant(type.initial_value)
            )
        ]
        setupCode[global_name] = tree
        substitutions[name] = ast.Name(id=global_name)
    
    return substitutions

def create_setup_code(func):
    prereqs = getattr(func, "__MINDPILE_PREREQS", None)
    if prereqs is not None:
        for p in prereqs:
            if setupCode.get(p) is None:
                tree = p()
                setupCode[p] = tree

def MethodCall(target: str, **parameters):
    def decorator(func):
        # Memoise the heavy lifting of template generation so it is only run once and only if this MethodCall is used
        @memoise
        def memo():
            types, local_variables = parse_parameter_types(parameters)

            # Get the AST template
            stringTemplate = func()
            tree = ast.parse(textwrap.dedent(stringTemplate))
            substitute = substitute_tree(tree)

            return substitute, types, local_variables
        
        @functools.wraps(func)
        def wrappedFunc(**kwargs) -> ast.AST:
            create_setup_code(func)

            substitute, types, local_variables = memo()
            substitutions = create_parameter_substitutions(target, kwargs, types, local_variables)

            for name, type in types.items():
                parser = get_parser(type)
                value = substitutions[name]
                if not isinstance(value, ast.AST):
                    substitutions[name] = ast.Constant(parser(value))

            return substitute(substitutions)
        methods[target] = wrappedFunc
        
        return func
    return decorator

def DynamicMethodCall(target: str, **parameters):
    def decorator(func):
        # Memoise the heavy lifting of template generation so it is only run once and only if this MethodCall is used
        @memoise
        def memo():
            types, local_variables = parse_parameter_types(parameters)
            return types, local_variables
    
        @functools.wraps(func)
        def wrappedFunc(**kwargs) -> ast.AST:
            create_setup_code(func)

            types, local_variables = memo()
            substitutions = create_parameter_substitutions(target, kwargs, types, local_variables)

            for name, type in types.items():
                parser = get_parser(type)
                value = substitutions[name]
                if not isinstance(value, ast.AST):
                    substitutions[name] = parser(value)

            return func(**substitutions)
        methods[target] = wrappedFunc

        return func
    return decorator

def Setup(func):
    @functools.wraps(func)
    @memoise
    def wrapped():
        stringTemplate = func()
        tree = p(stringTemplate)
        return tree
    return wrapped

def Requires(prereq):
    def decorator(func):
        prereqs = getattr(func, "__MINDPILE_PREREQS", set())
        prereqs.add(prereq)
        setattr(func, "__MINDPILE_PREREQS", prereqs)
        return func
    return decorator

def startCodeGen():
    global global_var_count
    setupCode.clear()
    global_var_count = 0

def generateSetupAST():
    tree = newTree()
    tree.body.append(p(boilerplate).body)
    for block in setupCode.values():
        tree.body += block.body
    return tree
